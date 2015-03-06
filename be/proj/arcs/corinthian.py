from django.shortcuts import render_to_response
from fdfgen import forge_fdf

from proj.utils import json_response, get_POST_data

def dtr_generate(request):
  rq = get_POST_data(request)

  fdf = forge_fdf("",fields,[],[],[])
  fdf_file = open("data.fdf","w")
  fdf_file.write(fdf)
  fdf_file.close()

def dtr_view(request):
  asdf

def corinthiansignup(request):
  return render_to_response('corinthian/signup.html')

def corinthiansolidarity(request):
  return render_to_response('corinthian/solidarity.html')

def studentstrike(request):
  return render_to_response('corinthian/studentstrike.html')

def knowyourstudentdebt(request):
  return render_to_response('corinthian/knowyourstudentdebt.html')
