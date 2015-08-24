from django.shortcuts import render_to_response, redirect
from proj.collectives.models import UserAction, Action, Collective
from proj.utils import json_response, get_POST_data

def collective(request, slug):
  collective = Collective.objects.get(slug=slug)
  c = {
    'collective': collective,
    'user': request.user
  }
  return render_to_response('collectives/collective.html', c)

def action(request, slug):
  action = Action.objects.get(slug=slug)
  c = {
    'action': action,
    'user': request.user
  }
  return render_to_response('collectives/action.html', c)

def all_actions(request):
  collectives = Collective.objects.all()
  actions = Action.objects.filter(active=True, private=False)
  c = {
    'collectives': collectives,
    'actions': actions,
    'user': request.user
  }
  return render_to_response('collectives/all_actions.html', c)
