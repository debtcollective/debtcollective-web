from django.db import models
from boto.s3.key import Key
from proj.utils import get_s3_conn, store_in_s3, generate_pdf
from django.contrib.auth.models import User
from jsonfield import JSONField

import proj.settings as settings
import datetime
import sys
import json
import os

## TODO: move this shiz to dtr.py
S3_BUCKET_NAME = 'corinthiandtr'
if settings.DEBUG:
  S3_BUCKET_NAME += '.dev'

conn = get_s3_conn()

TMP_FILE_DIR = '/tmp'
SOURCE_FILE = os.path.join(os.path.dirname(__file__), 'dc_defense_form_1-3.pdf')
DTR_FIELDS_FILE = os.path.join(os.path.dirname(__file__), 'dtr_fields.json')

def fdf_filename(key):
  return os.path.join(TMP_FILE_DIR, str(key) + '_data.fdf')

def output_filename(key):
  return os.path.join(TMP_FILE_DIR, str(key) + '_output.pdf')

class DTRUserProfile(models.Model):
  data = JSONField()

  def __unicode__(self):
    return self.user.username

  def s3_key(self):
    bucket = conn.get_bucket(S3_BUCKET_NAME)
    key = Key(bucket)
    key.key = self.id
    return key

  def to_json(self):
    data = self.__dict__.copy()
    del data['_state']
    return data

  def pdf_link(self, expires_in=3000):
    key = self.s3_key()
    url = key.generate_url(expires_in=expires_in, force_http=True)
    return url

  @classmethod
  def generate(cls, values):
    obj = cls.objects.create()
    key = obj.id

    fdf_file = fdf_filename(key)
    output_file = output_filename(key)
    generate_pdf(cls.FIELDS, values, SOURCE_FILE, fdf_file, output_file)

    metadata = {
      'name': values['name'],
      'version': 1
    }
    store_in_s3(conn, S3_BUCKET_NAME, key, output_file, metadata)

    for field in cls.SENSITIVE_FIELDS:
      if values.get(field):
        del values[field]
    values['key'] = key
    obj.data = values
    obj.save()

    return obj

  SENSITIVE_FIELDS = ["ssn_1", "ssn_2", "ssn_3"]

with open(DTR_FIELDS_FILE, 'rb') as fp:
  DTRUserProfile.FIELDS = json.loads(fp.read())