from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponse, Http404
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt

from proj.utils import json_response, get_POST_data
from proj.gather.models import Debt, UserProfile, Point

import simplejson as json

import settings
import stripe

@ensure_csrf_cookie
def splash(request):
  return render_to_response('proj/splash.html', {})

def map(request):
  return render_to_response('proj/map.html')

def corinthiansignup(request):
  return render_to_response('proj/strikeform.html')

def corinthiansolidarity(request):
  return render_to_response('proj/corinthiansolidarity.html')

def knowyourstudentdebt(request):
  return render_to_response('proj/knowyourstudentdebt.html')

def studentstrike(request):
  return render_to_response('proj/studentstrike.html')

def nov_fourth(request):
  return render_to_response('proj/nov4.html')

def thankyou(request):
  return render_to_response('proj/thankyou.html')

def not_found(request):
  return render_to_response('proj/404.html')

@csrf_exempt
def stripe_endpoint(request):
  stripe.api_key = settings.STRIPE_KEY

  if request.method == 'POST':
    rq = get_POST_data(request)
    try:
      stripe.Charge.create(
        amount=int(rq['amount']) * 100,
        currency='usd',
        source=rq['stripeToken']['id'],
        description="donation"
      )
    except stripe.CardError, e:
      pass

  return json_response({'status': 'ok'}, 200)

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

@csrf_exempt
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
