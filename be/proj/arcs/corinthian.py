from django.shortcuts import render_to_response, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from proj.arcs.models import DTRUserProfile
from proj.utils import json_response, get_POST_data
from proj.gather.models import Debt, UserProfile, Point
from boto.exception import S3ResponseError

import proj.settings as settings

import os
import zipfile
import StringIO
import csv
import json

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
  dtrprofile = DTRUserProfile.generate(rq)

  return json_response({
    'id': dtrprofile.id,
    'pdf_link': dtrprofile.pdf_link(),
  }, 200)
  #return redirect('/corinthian/dtr/view/' + dtrprofile.id)

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
