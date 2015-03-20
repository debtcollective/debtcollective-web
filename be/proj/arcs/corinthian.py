from django.shortcuts import render_to_response
from fdfgen import forge_fdf
from proj.utils import json_response, get_POST_data
from proj.gather.models import Debt, UserProfile, Point

import proj.arcs.dtr as dtr

def dtr_generate(request):
  values = get_POST_data(request)
  key = dtr.generate(values)

  return json_response({'key': key}, 200)

def corinthiansignup(request):
  return render_to_response('corinthian/signup.html')

def corinthiansolidarity(request):
  return render_to_response('corinthian/solidarity.html')

def studentstrike(request):
  return render_to_response('corinthian/studentstrike.html')

def knowyourstudentdebt(request):
  return render_to_response('corinthian/knowyourstudentdebt.html')
