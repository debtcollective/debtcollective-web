from django.conf import settings
from django.shortcuts import render_to_response
from django.db.models import Count, Sum

from django.contrib.auth.models import User
from proj.gather.models import UserProfile, Point, Debt
from proj.utils import json_response, get_POST_data

import simplejson as json
import os

def points(request):
  data = [p.to_json() for p in Point.objects.all()]
  return json_response(data, 200)

def debt_total(request):
  total = Debt.objects.all().aggregate(Sum('amount'))
  return json_response({'total': total['amount__sum']}, 200)

def debt_choices(request):
  choices = Debt.DEBT_CHOICES
  choices = map(lambda c: {'id': c[0], 'name': c[1]}, choices)

  return json_response(choices, 200)

def get_map_data():
  total_amount = Debt.objects.all().aggregate(Sum('amount'))

  total_users = User.objects.count()
  query = Point.objects.annotate(
      num_users=Count('userprofile'),
      sum_amount=Sum('userprofile__user__debt__amount') # o fuck
    ).filter(num_users__gte=1)

  points = []
  for p in query:
    if p.sum_amount:
      points.append(p.to_json())

  # TODO: loading them and then dumping them again is
  # probably costing us performance (karissa)
  return {
    'total_users': total_users,
    'total_amount': total_amount['amount__sum'],
    'points': points
  }

def generate_and_store_map_data():
    data = get_map_data()
    static_dir = settings.STATIC_ROOT
    fp = open("%s/%s.json" % (os.path.join(static_dir, 'js'), "map_data"), 'wb')
    fp.write(json.dumps(data))
    fp.close()
    return data

def map_data(request):
  """
  GET /map_data
  """
  data = get_map_data()
  return json_response(data, 200)


def generate_map_json(request):
  """
  GET /generate_map_json
  write the map data json to file
  """
  password = request.GET.get('password')
  if password == settings.MAP_PASSWORD:
    data = generate_and_store_map_data()
    return json_response(data, 200)
  else:
    return json_response({'status': 'error'}, 500)

