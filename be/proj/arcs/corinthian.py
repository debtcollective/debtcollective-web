from django.shortcuts import render_to_response, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from proj.arcs.models import DTRUserProfile
from proj.utils import json_response, get_POST_data
from django.contrib.auth.models import User
from django.contrib import auth
from proj.gather.models import Debt, UserProfile, Point
from proj.collectives.models import UserAction, CollectiveMember, Action
from boto.exception import S3ResponseError

import smtplib

# Import the email modules we'll need
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

def dtr_migrate(request, id):
  dtr_profile = DTRUserProfile.objects.get(id=id)
  email = request.GET.get('email')
  dtr_data = dtr_profile.data
  if not dtr_data:
    return json_response({'error': 'Could not find your DTR. Please contact support@debtcollective.org'})
  if dtr_data['email'] != email:
    return json_response({'error': 'Email does not match original. Please provide a valid email address'}, 500)

  dtr_action = Action.objects.get(name='Defense to Repayment')

  email = email.lower()
  users = User.objects.filter(email=email)
  if users:
    user = users[0]
  else:
    user = User.objects.create_user(email, password=email, email=email)

  user = auth.authenticate(username=user.username, password=email)
  auth.login(request, user)

  useraction, created = UserAction.objects.get_or_create(user=user, action=dtr_action)
  if created:
    useraction.data = dtr_profile.data
    useraction.status = UserAction.COMPLETED
    return redirect('/change_password')
  else:
    return redirect('/profile')

def dtr_email(dtr_profile):
  mailserver = smtplib.SMTP('smtp.mandrillapp.com', 587)
  mailserver.set_debuglevel(1)
  mailserver.login('noreply@debtcollective.org', settings.MANDRILL_API_KEY)

  user_data = dict(dtr_profile.data)
  from_email = 'noreply@debtcollective.org'
  to = settings.DTR_RECIPIENT

  msg = MIMEMultipart()
  name = ''.join(user_data['name'])
  msg['Subject'] = '{0} at {1}'.format(name, ''.join(user_data['school_name']))
  msg['To'] = to
  msg['cc'] = ''.join(user_data['email'])
  msg['From'] = from_email
  msg.attach(MIMEText("""
To whom it may concern:

Attached find my application for Defense to Repayment.

Best, %s
""" % (name)))
  fp = open(dtr_profile.output_file, 'rb')
  part = MIMEBase('application', "octet-stream")
  part.set_payload(fp.read())
  Encoders.encode_base64(part)
  filename = "{0}.pdf".format(''.join(user_data['name']))
  part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(filename))
  msg.attach(part)
  fp.close()

  msg.add_header('X-MC-Track', 'opens, clicks')
  mailserver.sendmail(from_email, [to], msg.as_string())

  mailserver.quit()

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
  rq['state_2'] = rq.get('state', 'NA')
  dtr_profile = DTRUserProfile.generate(rq)

  dtr_email(dtr_profile)

  return json_response({
    'id': dtr_profile.id,
    'pdf_link': dtr_profile.pdf_link(),
  }, 200)

def dtr_view(request, id):
  if not request.user.is_superuser:
    return redirect('/login')

  c = {
    'dtrprofile': DTRUserProfile.objects.get(id=id)
  }

  return render_to_response('corinthian/dtrview.html', c)

def admin(request):
  if not request.user.is_superuser:
    return redirect('/login')

  c = {
    'all_dtrs': DTRUserProfile.objects.all(),
    'dtr_total': DTRUserProfile.objects.count()
  }

  return render_to_response('corinthian/admin.html', c)

def corinthiandtr(request):
  basepath = settings.TEMPLATE_DIRS[0]
  template_path = os.path.join(basepath, 'debtcollective-wizard/index.html')
  with open(template_path) as fp:
    template = fp.read()
    return HttpResponse(template)

def corinthiansignup(request):
  return render_to_response('corinthian/signup.html')

def corinthiancollective(request):
  return render_to_response('corinthian/signup.html')

def corinthiansolidarity(request):
  return render_to_response('corinthian/solidarity.html')

def studentstrike(request):
  return render_to_response('corinthian/studentstrike.html')

def knowyourstudentdebt(request):
  return render_to_response('corinthian/knowyourstudentdebt.html')

def solidaritystrike(request):
  return render_to_response('corinthian/solidaritystrike.html')

def solidaritystrikeform(request):
  return render_to_response('corinthian/solidaritystrikeform.html')
