from django.http import HttpResponse, Http404
from fdfgen import forge_fdf
from boto.s3.key import Key
from django.core.serializers.json import Serializer, DjangoJSONEncoder
from boto.s3.connection import S3Connection

import smtplib
import json
import settings
import subprocess

def send_email(msg):
  mailserver = smtplib.SMTP('smtp.mandrillapp.com', 587)
  mailserver.set_debuglevel(1)
  mailserver.login('noreply@debtcollective.org', settings.MANDRILL_API_KEY)

  from_email = 'noreply@debtcollective.org'
  msg['From'] = from_email
  to = msg['To']
  msg.add_header('X-MC-Track', 'opens')
  mailserver.sendmail(from_email, to.split(','), msg.as_string())
  mailserver.quit()

def get_POST_data(request):
  """
  For some reason, posting json to the backend can be a real
  headache and django wants to have control over the form
  submission data. This is a workaround in cases where we want
  to use ajax POST requests but don't have it encoded as form data.
  """
  if len(request.POST.keys()) > 0:
    return request.POST.copy()
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

def store_in_s3(conn, bucket_name, key, output_file, metadata=None):
  if not metadata:
    metadata = {}
  bucket = conn.get_bucket(bucket_name)
  k = Key(bucket)
  k.key = key
  for key, value in metadata.iteritems():
    k.set_metadata(key, value)
  k.set_contents_from_filename(output_file)

def generate_pdf(values, source_filename, fdf_filename, output_filename):
  # values: dictionary of fieldname, value
  fdf_fields = []

  for fieldname, value in values.iteritems():
    fdf_fields.append((fieldname, value))


  fdf = forge_fdf("", fdf_fields, [], [], [])

  fdf_file = open(fdf_filename, "w")
  fdf_file.write(fdf)
  fdf_file.close()

  subprocess.call(['pdftk', source_filename ,'fill_form', fdf_filename, 'output', output_filename])
