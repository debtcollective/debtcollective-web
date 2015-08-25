from django.shortcuts import render_to_response, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from proj.arcs.models import DTRUserProfile
from proj.utils import json_response, get_POST_data, send_email
from django.contrib.auth.models import User
from django.contrib import auth
from proj.gather.models import Debt, UserProfile, Point
from proj.collectives.models import UserAction, CollectiveMember, Action, Collective
from boto.exception import S3ResponseError
from boto.s3.key import Key
from proj.utils import get_s3_conn, store_in_s3, generate_pdf
from django.contrib.auth.models import User
from jsonfield import JSONField
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders

import proj.settings as settings

import os
import zipfile
import StringIO
import csv
import json
import datetime
import sys

SENSITIVE_FIELDS = ["ssn_1", "ssn_2", "ssn_3"]


S3_BUCKET_NAME = 'corinthiandtr'
if settings.DEBUG:
  S3_BUCKET_NAME += '.dev'

conn = get_s3_conn()

TMP_FILE_DIR = '/tmp'
basepath = settings.TEMPLATE_DIRS[0]
SOURCE_FILE = os.path.join(basepath, 'debtcollective-wizard/borrower_defense_to_repayment.pdf')
DTR_FIELDS_FILE = os.path.join(os.path.dirname(__file__), 'dtr_fields.json')

with open(DTR_FIELDS_FILE, 'rb') as fp:
  FIELDS = json.loads(fp.read())

def fdf_filename(key):
  return os.path.join(TMP_FILE_DIR, str(key) + '_data.fdf')

def output_filename(key):
  return os.path.join(TMP_FILE_DIR, str(key) + '_output.pdf')

def s3_key(dtr):
  bucket = conn.get_bucket(S3_BUCKET_NAME)
  key = Key(bucket)
  key.key = dtr.id
  return key

def to_json(dtr):
  data = dtr.__dict__.copy()
  del data['_state']
  return data

def pdf_link(dtr, expires_in=3000):
  key = s3_key(dtr)
  url = key.generate_url(expires_in=expires_in, force_http=True)
  return url

def make_a_pdf(dtr, values=None):
  key = dtr.id
  if not values:
    values = dtr.data

  fdf_file = fdf_filename(key)
  output_file = output_filename(key)
  generate_pdf(values, SOURCE_FILE, fdf_file, output_file)

  metadata = {
    'name': values['name'],
    'version': 1
  }
  store_in_s3(conn, S3_BUCKET_NAME, key, output_file, metadata)

  return output_file

def create_dtr_user_action(values, user):
  action = Action.objects.get(name='Defense To Repayment')
  dtr, created = UserAction.objects.get_or_create(user=user, action=action)

  # create a pdf with sensitive data to be stored in s3 and thrown away
  make_a_pdf(dtr, values)

  # throw away sensitive fields
  for field in SENSITIVE_FIELDS:
    if values.get(field):
      del values[field]
  values['key'] = dtr.id

  # store only non-sensitive fields on disk
  dtr.data = values
  dtr.save()

  return dtr, created

def dtr_migrate_email(dtr):
  key = str(dtr.id)
  user_data = dict(dtr.data)
  name = ''.join(user_data['name'])
  msg = MIMEMultipart()
  msg['Subject'] = '{0}, Your Defense to Repayment Application for {1}'.format(name, ''.join(user_data['school_name']))
  msg['To'] = ''.join(user_data['email'])

  migrate_url = 'https://debtcollective.org/dtr/migrate/' + key + 'email=' + ''.join(user_data['email'])

  msg.attach(MIMEText("""
Hello {0},
<p>
You filled out a Department of Education <a href="http://debtcollective.org/defense-to-repayment">Defense to Repayment claim on the Debt Collective website</a>.
</p>
<p>
We have good news. You can now you can login to the Debt Collective to edit and resubmit your form to the Department of Education.
</p>
<p>
Please go to <a href="{1}">this link</a> to make sure all your information is correct. If you haven't heard back from the Department of Education, or don't have the last four digits of your social security number listed, you might want to resubmit your application:
</p>
<p>
{1}
</p>

Solidarty,

The Debt Collective
""".format(name, migrate_url), 'html'))

  send_email(msg, headers={'X-MC-MergeVars': '{"header": "Defense to Repayment Ready for Review!"}'})

def user_get_or_create(email, password):
  try:
    user = User.objects.get(email=email)
    created = False
  except ObjectDoesNotExist:
    user = User.objects.create_user(email, password=password, email=email)
    created = True

  return user, created

def dtr_migrate(request, id):
  email = request.GET.get('email')

  try:
    dtr = DTRUserProfile.objects.get(id=id)
  except:
    dtr = None

  if not dtr:
    return json_response({'error': 'Could not find your DTR. Please contact support@debtcollective.org'}, 500)
  if ''.join(dtr.data['email']) != email:
    return json_response({'error': 'Invalid request.'}, 500)

  dtr_action = Action.objects.get(name='Defense to Repayment')

  password = email.lower()
  if request.user.is_authenticated():
    user = request.user

  user, created_user = user_get_or_create(email, password)
  create_dtr_user_action(dtr.data, user)

  if request.user_is_authenticated():
    return redirect('/profile')

  if not created_user:
    return redirect('/login')

  # user has been created for them, for the purpose of migrating.
  # they need to change their password now.
  user = auth.authenticate(username=email, password=password)
  auth.login(request, user)
  return redirect('/change_password')

def attach(msg, contents, filename):
  part = MIMEBase('application', 'octet-stream')
  part.set_payload(contents)
  Encoders.encode_base64(part)
  part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(filename))
  msg.attach(part)

def dtr_email(dtr, attachments=None):
  user_data = dict(dtr.data)
  to = settings.DTR_RECIPIENT
  msg = MIMEMultipart()

  name = ''.join(user_data['name'])
  msg['Subject'] = '{0} at {1}'.format(name, ''.join(user_data['school_name']))
  msg['To'] = to
  msg['cc'] = ''.join(user_data['email'])
  msg.attach(MIMEText("""
To whom it may concern:

Attached find my application for Defense to Repayment.

Best, %s
""" % (name)))
  fp = open(dtr.output_file, 'rb')
  filename = "{0}.pdf".format(''.join(user_data['name']))
  attach(msg, fp.read(), filename)
  fp.close()

  for key, attachment in attachments.iteritems():
    attach(msg, attachment.file.read(), attachment.name)

  send_email(msg)

def remove_dupes(profiles):
  finished = {}
  for profile in profiles:
    if type(profile.data) == dict:
      del profile.data['key']
      duped_key = json.dumps(profile.data)
      finished[duped_key] = profile
  return finished.values()

def dtr_download(request, f, to):
  if not request.user.is_superuser:
    return redirect('/login')

  # Open StringIO to grab in-memory ZIP contents
  s = StringIO.StringIO()
  zf = zipfile.ZipFile(s, "w")

  profiles = DTRUserProfile.objects.filter(
    id__gte=f
  ).filter(
    id__lte=to
  )

  for profile in remove_dupes(profiles):
    key = profile.s3_key()
    try:
      contents = key.get_contents_as_string()
      if type(profile.data) != dict:
        continue

      servicer = profile.data.get('servicer', 'NA')
      name = profile.data.get('name', 'NA')
      filename = "dtr_forms/%s/%s_%s.pdf" % (servicer, name, profile.id)
      zf.writestr(filename, contents)
    except S3ResponseError:
      pass

  zf.close()

  # Grab ZIP file from in-memory, make response with correct MIME-type
  resp = HttpResponse(s.getvalue(), mimetype = "application/x-zip-compressed")
  # ..and correct content-disposition
  resp['Content-Disposition'] = 'attachment; filename=dtr_forms.zip'

  return resp

def dtr_csv(request):
  # get dtrs as csv
  if not request.user.is_superuser:
    return redirect('/login')
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename="all_dtr.csv"'

  profiles = DTRUserProfile.objects.all()
  writer = csv.DictWriter(response, fieldnames=DTRUserProfile.FIELDS, extrasaction='ignore')
  writer.writeheader()
  for profile in remove_dupes(profiles):
    row = {}
    data = profile.data

    if type(data) == dict:
      for key, value in data.iteritems():
        if type(value) == unicode:
          profile.data[key] = value.encode('utf-8')

      writer.writerow(data)

  return response

def dtr_restore(request, id):
  profile = DTRUserProfile.objects.get(id=id)

  profile.make_a_pdf()

  return json_response({
    'id': profile.id,
    'pdf_link': profile.pdf_link(),
  }, 200)

@csrf_exempt
def dtr_generate(request):
  if request.method != "POST":
    raise Http404

  rq = get_POST_data(request)

  # school_name_2 .. 13
  school_name = rq.get('school_name', 'Unknown')
  i = 2
  while i < 14:
    rq['school_name_%s' % i] = school_name
    i += 1

  rq['name_2'] = rq.get('name', 'NA')

  if request.user.is_authenticated():
    user = request.user
  else:
    user = None
  dtr = create_dtr_user_action(rq, user=user)

  dtr_email(dtr, attachments=request.FILES)
  dtr_migrate_email(dtr)

  return json_response({
    'id': dtr.id,
    'pdf_link': dtr.pdf_link(),
  }, 200)

def dtr_data(request):
  if not request.user.is_authenticated():
    data = {'warning': 'No user found'}
  else:
    action = Action.objects.get(name='Defense to Repayment')
    try:
      user_action = UserAction.objects.get(user=request.user, action=action)
      data = user_action.data
    except ObjectDoesNotExist:
      data = {'warning': 'No dtr found'}

  return json_response(data, 200)

def dtr_view(request, id):
  if not request.user.is_superuser:
    return redirect('/login')

  c = {
    'dtrprofile': DTRUserProfile.objects.get(id=id)
  }

  return render_to_response('dtr/dtrview.html', c)

def dtr_admin(request):
  if not request.user.is_superuser:
    return redirect('/login')

  c = {
    'all_dtrs': DTRUserProfile.objects.all(),
    'dtr_total': DTRUserProfile.objects.count()
  }

  return render_to_response('dtr/admin.html', c)

def dtr(request):
  basepath = settings.TEMPLATE_DIRS[0]
  template_path = os.path.join(basepath, 'debtcollective-wizard/index.html')
  with open(template_path) as fp:
    template = fp.read()
    return HttpResponse(template)

def corinthiansignup(request):
  collective = Collective.objects.get(name='Corinthian Collective')
  c = {
    "collective": collective,
    "actions": Action.objects.filter(collective=collective)
  }
  return render_to_response('corinthian/signup.html', c)

def dtr_redirect(request):
  return redirect('/defense-to-repayment')

def corinthiancollective(request):
  return render_to_response('corinthian/signup.html')

def corinthiansolidarity(request):
  return render_to_response('corinthian/solidarity.html')

def studentstrike(request):
  return render_to_response('corinthian/studentstrike.html')

def solidaritystrike(request):
  c = {
    'collective': Collective.objects.get(name='Debt Collective'),
    'actions': Action.objects.filter(name__contains='Strike')[:3]
  }
  return render_to_response('corinthian/solidaritystrike.html', c)

def solidaritystrikeform(request):
  return render_to_response('corinthian/solidaritystrikeform.html')
