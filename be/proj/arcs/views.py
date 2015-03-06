from django.shortcuts import render
from fdfgen import forge_fdf

def strikers(request):
  data = [p.to_json() for p in Point.objects.all()]
  return json_response(data, 200)

def dtr_generate(request):
  fields = [('name','John Smith'),('telephone','555-1234')]
  fdf = forge_fdf("",fields,[],[],[])
  fdf_file = open("data.fdf","w")
  fdf_file.write(fdf)
  fdf_file.close()

def dtr_view(request):


def corinthiansignup(request):
  return render_to_response('proj/strikeform.html')

def corinthiansolidarity(request):
  return render_to_response('proj/corinthiansolidarity.html')
