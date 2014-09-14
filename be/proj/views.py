from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponse, Http404
from django.core.context_processors import csrf

from be.proj.utils import json_response, get_POST_data
from be.proj.gather.models import Debt, UserProfile, Point

import simplejson as json

def splash(request):
  return render_to_response('proj/splash.html')

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
  username = rq.get('username')
  password = rq.get('password')
  if not username or not password:
    return json_response({'status': 'error',
      'message': 'Those credentials could not be authenticated.'}, 500)

  user = User.objects.create_user(username, password=password, email=None)

  location = rq.get('location')
  if location:
    location = Point.objects.get(id=location)
  data = UserProfile.objects.create(user=user, location=location)

  kind = rq.get('kind')
  amount = rq.get('amount')
  last_payment = rq.get('last_payment')
  if kind:
    debt = Debt.objects.create(user=user, amount=amount,
      kind=kind, last_payment=last_payment)

  return json_response({'status': 'ok'}, 200)
