from django.shortcuts import render_to_response

# Create your views here.
def splash(request):
  return render_to_response('proj/splash.html')

def map(request):
  return render_to_response('proj/map.html')

