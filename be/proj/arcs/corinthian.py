from django.shortcuts import render_to_response, redirect
from django.core.exceptions import ObjectDoesNotExist
from proj.arcs.models import DTRUserProfile
from django.http import Http404, HttpResponse
from proj.utils import json_response, get_POST_data
from proj.gather.models import Debt, UserProfile, Point
from django.views.decorators.csrf import csrf_exempt
from boto.exception import S3ResponseError

import os
import zipfile
import StringIO
import csv
import json

def dtr_download(request):
  if not request.user.is_superuser:
    return redirect('/login')

  # Open StringIO to grab in-memory ZIP contents
  s = StringIO.StringIO()
  zf = zipfile.ZipFile(s, "w")

  profiles = DTRUserProfile.objects.all()
  for profile in profiles:
    key = profile.s3_key()
    try:
      contents = key.get_contents_as_string()
      zf.writestr("dtr_forms/%s/%s_%s.pdf" % (profile.data.get('servicer', 'NA'), profile.data['name'], profile.id), contents)
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

  writer = csv.writer(response)
  for profile in DTRUserProfile.objects.all():
    row = []
    data = profile.data

    if type(data) == dict:
      for key, value in data.iteritems():
        row.append(value)
      writer.writerow(row)

  return response

@csrf_exempt
def dtr_generate(request):
  if request.method != "POST":
    raise Http404

  rq = get_POST_data(request)

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
  return render_to_response('debtcollective-wizard/index.html')

def corinthiansignup(request):
  return render_to_response('corinthian/signup.html')

def corinthiansolidarity(request):
  return render_to_response('corinthian/solidarity.html')

def studentstrike(request):
  return render_to_response('corinthian/studentstrike.html')

def knowyourstudentdebt(request):
  return render_to_response('corinthian/knowyourstudentdebt.html')