from django.shortcuts import redirect, render, render_to_response
from proj.utils import json_response, get_POST_data

def portal(request):
  if not request.user.is_authenticated():
    return redirect('/login')

  return render_to_response('portal/dashboard.html', {'user': request.user})

