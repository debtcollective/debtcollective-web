from django.http import HttpResponse, Http404
from django.core.serializers.json import Serializer, DjangoJSONEncoder
from boto.s3.connection import S3Connection

import json
import settings

def get_POST_data(request):
  """
  For some reason, posting json to the backend can be a real
  headache and django wants to have control over the form
  submission data. This is a workaround in cases where we want
  to use ajax POST requests but don't have it encoded as form data.
  """
  if len(request.POST.keys()) > 0:
    return request.POST
  else:
    # assuming request.body contains json data which is UTF-8 encoded
    return json.loads(request.body, encoding='utf-8')

def json_response(response_data, status_code):
  if type(response_data) == dict or type(response_data) == list:
    response_data = json.dumps(response_data)
  rs = HttpResponse(response_data, content_type="application/json")
  rs.status_code = status_code
  return rs


def get_s3_conn():
  conn = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
  return conn
