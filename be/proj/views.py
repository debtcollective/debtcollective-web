from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponse, Http404
from be.proj.gather.models import Debt, UserData
from django.core.context_processors import csrf

import json

def get_POST_data(request):
  """
  For some reason, posting json to the backend can be a real
  headache and django wants to have control over the form
  submission data. This is a workaround in cases where we want
  to use ajax POST requests but don't have it encoded as form data.
  """
  if len(request.POST.keys()) > 0:
    return request.POST
  else:
    # assuming request.body contains json data which is UTF-8 encoded
    json_str = request.body.decode(encoding='UTF-8')
    # turn the json bytestr into a python obj
    json_obj = json.loads(json_str)
    return json_obj

def json_response(response_data, status_code):
  rs = HttpResponse(json.dumps(response_data),
      content_type="application/json")
  rs.status_code = status_code
  return rs

def splash(request):
  c = {}
  c.update(csrf(request))
  return render_to_response('proj/splash.html', c)

def map(request):
  return render_to_response('proj/map.html')

def login(request):
  """
  POST /login
  """
  if request.method != 'POST':
    raise Http404

  rq = get_POST_data(request)
  user = authenticate(username=rq['username'], password=rq['password'])
  if user is not None:
    return json_response({'status': 'ok'}, 200)
  else:
    return json_response({'status': 'error',
      'message': 'Those credentials could not be authenticated.'}, 500)

def signup(request):
  """
  POST /signup

  Creates an account for a given user, along with
  debt type information.
  """
  if request.method != 'POST':
    raise Http404

  rq = get_POST_data(request)
  username = rq['username']
  password = rq['password']
  user = User.objects.create_user(username, password=password, email=None)

  location = rq.get('location')
  data = UserData.objects.create(user=user, location=location)

  kind = rq.get('kind')
  amount = rq.get('amount')
  last_payment = rq.get('last_payment')
  if kind:
    debt = Debt.objects.create(user=user, amount=amount,
      kind=kind, last_payment=last_payment)

  return json_response({'status': 'ok'}, 200)
