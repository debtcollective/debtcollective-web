from django.shortcuts import render, render_to_response, redirect
from django.contrib import auth
from django.http import HttpResponse, Http404
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from proj.utils import json_response, get_POST_data

from django.contrib.auth.models import User
from proj.gather.models import Debt, UserProfile, Point
from proj.collectives.models import Collective, UserAction, CollectiveMember, Action

import simplejson as json

import settings
import stripe

@csrf_exempt
def stripe_endpoint(request):
  stripe.api_key = settings.STRIPE_KEY

  if request.method == 'POST':
    rq = get_POST_data(request)
    try:
      stripe.Charge.create(
        amount=int(float(rq['amount']) * 100),
        currency='usd',
        source=rq['stripeToken']['id'],
        description="donation"
      )
    except stripe.CardError, e:
      pass

  return json_response({'status': 'ok'}, 200)

def password_reset_complete(request):
  template_response = auth.views.password_reset_complete(request)
  if request.method == 'GET':
    template_response.template_name = 'proj/login.html'
    template_response.context_data['password_change'] = True
  return template_response

def change_password(request):
  template_response = auth.views.password_change(request, post_change_redirect='/profile')
  if request.method == 'GET':
    template_response.template_name = 'proj/change_password.html'
    template_response.context_data['user'] = request.user
  return template_response

def profile(request):
  """
  GET /profile
  """
  if not request.user.is_authenticated():
    return redirect('/login')
  c = {}

  c['user'] = request.user
  c['user'].profile = UserProfile.objects.get_or_create(user=request.user)
  c['debts'] = Debt.objects.filter(user=c['user'])
  # user_actions = UserAction.objects.select_related('action').filter(user=request.user).distinct('action__id')
  # c['user_actions'] = map(lambda u: u.action, user_actions)
  memberships = CollectiveMember.objects.select_related('collective').filter(user=request.user)
  c['collectives'] = map(lambda m: m.collective, memberships)
  c['collective_actions'] = set()
  for collective in c['collectives']:
    actions = collective.actions.all()
    for action in actions:
      c['collective_actions'].add(action)
  return render_to_response('proj/profile.html', c)

def logout(request):
  """
  GET /logout
  """
  auth.logout(request)
  return redirect('/login')

def login(request):
  """
  GET /login
  POST /login
  """
  c = {}
  if request.user.is_authenticated():
    return redirect('/profile')

  if request.method == 'POST':
    rq = get_POST_data(request)
    email = rq.get('email')
    username = rq.get('username')
    password = rq.get('password')
    if email and not username:
      username = User.objects.get(email=email).username

    if not username or not password:
      return json_response({'status': 'error', 'message': 'Username/password required.'}, 500)
    user = do_login(request, username, password)
    if user:
      return redirect('/profile')
    else:
      c.update({"bad_auth": True})

  c.update(csrf(request))
  return render_to_response('proj/login.html', c)

def do_login(request, username, password):
  user = auth.authenticate(username=username, password=password)
  if user is not None:
    user = auth.login(request, user)
    return True
  return False

@csrf_exempt
def signup(request):
  """
  POST /signup

  Creates an account for a given user, along with
  debt type information.
  """
  if request.method == 'GET':
    return render_to_response('proj/signup.html')

  if request.method != 'POST':
    return Http404

  rq = get_POST_data(request)
  email = rq.get('email')
  password = rq.get('password')
  if not email or not password:
    return json_response({'status': 'error', 'message': 'Email/password required.'}, 500)

  user = User.objects.filter(username=email)
  if user:
    if do_login(request, email, password):
      return json_response({'status': 'logged_in'}, 200)
    else:
      return json_response({'status': 'user_exists'}, 500)

  user = User.objects.create_user(username=email, email=email, password=password)
  point = rq.get('point')
  if point:
    point = Point.objects.get(id=point)

  userprofile = UserProfile.objects.get(user=user)
  userprofile.point = point
  userprofile.save()

  kind = rq.get('kind')
  amount = rq.get('amount')
  last_payment = rq.get('last_payment')
  if amount:
    debt = Debt.objects.create(user=user, amount=amount,
      kind=kind, last_payment=last_payment)

  return json_response({'status': 'ok'}, 200)

@ensure_csrf_cookie
def splash(request):
  if request.user.is_authenticated():
    return redirect('/profile')
  c = {"actions": Action.objects.filter(featured=True)[:2]}
  return render_to_response('proj/splash.html', c)

def solidarity(request):
  return redirect('https://docs.google.com/document/d/1m5l55FCsaQmFef4HcIUJHIE6PsyHjauV1FT6ztSRkSc/edit?usp=sharing')

def howfartofree(request):
  return render_to_response('proj/howfartofree.html')

def calculator(request):
  return render_to_response('proj/calculator.html')

def nov_fourth(request):
  return render_to_response('proj/nov4.html')

def thankyou(request):
  return render_to_response('proj/thankyou.html')

def not_found(request):
  return render(request, template_name='proj/404.html', status=404)

def blog(request):
  return render_to_response('proj/blog.html')
