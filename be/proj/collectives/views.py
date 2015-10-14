from django.shortcuts import redirect
from proj.collectives.models import UserAction, Action, Collective
from proj.utils import json_response, get_POST_data, render_response
from django.core.exceptions import ObjectDoesNotExist

def collective(request, slug):
  collective = Collective.objects.get(slug=slug)
  c = {
    'collective': collective,
    'user': request.user
  }
  return render_response(request, 'collectives/collective.html', c)

def action(request, slug):
  action = Action.objects.get(slug=slug)
  c = {
    'action': action,
    'user': request.user
  }
  return render_response(request, 'collectives/action.html', c)

def all_actions(request):
  if request.user.is_authenticated():
    return redirect('/profile')
  collectives = Collective.objects.all()
  actions = Action.objects.filter(active=True, private=False)
  c = {
    'collectives': collectives,
    'actions': actions,
    'user': request.user
  }
  return render_response(request, 'collectives/all_actions.html', c)

def ua_delete(request, pk):
  if not request.user.is_authenticated():
    return redirect('/login')

  try:
    useraction = UserAction.objects.get(id=pk)
    useraction.delete()
  except ObjectDoesNotExist:
    pass

  url = request.GET.get('redirect')
  return redirect(url)
