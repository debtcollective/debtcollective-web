from django.shortcuts import render_to_response, redirect
from proj.collectives.models import UserAction, Action, Collective

def collective(request, slug):
  collective = Collective.objects.get(slug=slug)

  c = {
    'collective': collective,
    'user': request.user,
    'actions': collective.actions.all(),
    'members': collective.members.all()
  }

  return render_to_response('collectives/collective.html', c)

def action(request, name):
  action = {
    'name': 'hello world'
  }
  c = {'action': action, 'user': request.user}
  return render_to_response('collectives/action.html', c)
