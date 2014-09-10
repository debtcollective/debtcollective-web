from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.http import HttpResponse
from be.proj.gather.models import Debt, UserData
from django.core.context_processors import csrf

import uuid
import json

def splash(request):
  c = {}
  c.update(csrf(request))
  return render_to_response('proj/splash.html', c)

def map(request):
  return render_to_response('proj/map.html')

def signup(request):
  """
  POST /signup

  Creates an account for a given user, along with
  debt type information.
  """
  request.is_ajax()
  if request.method == 'POST':
    rq = request.POST

    username = rq['username']
    password = rq['password']
    user = User.objects.create_user(username, password)

    location = rq.get('location')
    data = UserData.objects.create(user=user, location=location)

    kind = rq.get('kind')
    amount = rq.get('amount')
    last_payment = rq.get('last_payment')
    if kind:
      debt = Debt.objects.create(user=user, amount=amount,
        kind=kind, last_payment=last_payment)

    response_data = {'status': 'ok'}
    return HttpResponse(json.dumps(response_data),
        content_type="application/json")
