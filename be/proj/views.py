from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponse, Http404
from django.core.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie

from proj.utils import json_response, get_POST_data
from proj.gather.models import Debt, UserProfile, Point

import simplejson as json

@ensure_csrf_cookie
def splash(request):
  return render_to_response('proj/splash.html')

def map(request):
  return render_to_response('proj/map.html')

def corinthian(request):
  return render_to_response('proj/corinthian.html')

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

  point = rq.get('point')
  if point:
    point = Point.objects.get(id=point)
  data = UserProfile.objects.create(user=user, point=point)

  kind = rq.get('kind')
  amount = rq.get('amount')
  last_payment = rq.get('last_payment')
  if amount:
    debt = Debt.objects.create(user=user, amount=amount,
      kind=kind, last_payment=last_payment)

  return json_response({'status': 'ok'}, 200)
