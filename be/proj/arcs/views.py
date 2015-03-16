from django.shortcuts import render
import dtr
from proj.utils import json_response, get_POST_data

def strikers(request):
  data = [p.to_json() for p in Point.objects.all()]
  return json_response(data, 200)

def dtr_generate(request):
  values = get_POST_data(request)
  dtr.generate(values)
  return render_to_response

def corinthiansignup(request):
  return render_to_response('proj/strikeform.html')

def corinthiansolidarity(request):
  return render_to_response('proj/corinthiansolidarity.html')
