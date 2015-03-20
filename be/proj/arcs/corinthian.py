from django.shortcuts import render_to_response, redirect
from django.core.exceptions import ObjectDoesNotExist
from proj.arcs.models import DTRUserProfile
from django.http import Http404
from proj.utils import json_response, get_POST_data
from proj.gather.models import Debt, UserProfile, Point

import proj.arcs.dtr as dtr

def dtr_download(request):
  # turn into zip file
  return json_response({'status': 'ok'}, 200)

def dtr_stats(request):
  profiles = DTRUserProfile.objects.all()
  data = [profile.to_json() for p in profiles]
  return json_response(data, 200)

def dtr_generate(request):
  if request.method != 'POST':
    return dtr_view(request)

  rq = get_POST_data(request)
  values = rq['values']

  user = User.objects.get(username=rq['username'])
  dtrprofile = DTRUserProfile.generate_for_user(user, values)

  return dtr_view_handler(user, dtrprofile)

def dtr_view(request):
  if not request.user.is_authenticated():
    return redirect('/login')

  user = request.user
  try:
    dtrprofile = DTRUserProfile.objects.get(user=user)
  except ObjectDoesNotExist:
    return redirect('/corinthian/dtr_wizard')

  return dtr_view_handler(user, dtrprofile)

def dtr_view_handler(user, dtrprofile):
  c = {}
  c.update({
    'key': user.id,
    's3_link': dtrprofile.s3_link()
  })
  return render_to_response('corinthian/dtrview.html', c)

def dtr_wizard(request):
  return render_to_response('corinthian/wizard.html')

def corinthiansignup(request):
  return render_to_response('corinthian/signup.html')

def corinthiansolidarity(request):
  return render_to_response('corinthian/solidarity.html')

def studentstrike(request):
  return render_to_response('corinthian/studentstrike.html')

def knowyourstudentdebt(request):
  return render_to_response('corinthian/knowyourstudentdebt.html')
