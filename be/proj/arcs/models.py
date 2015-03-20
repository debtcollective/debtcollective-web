from django.db import models
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
SOURCE_FILE = os.path.join(os.path.dirname(os.getcwd()), 'dc_defense_form_1-3.pdf')

def fdf_filename(key):
  return os.path.join(TMP_FILE_DIR, str(key) + '_data.fdf')

def output_filename(key):
  return os.path.join(TMP_FILE_DIR, str(key) + '_output.pdf')

class DTRUserProfile(models.Model):
  user = models.OneToOneField(User, unique=True, primary_key=True)
  data = JSONField()

  def __unicode__(self):
    return self.user.username

  def s3_key(self):
    return self.user.id

  def to_json(self):
    data = self.__dict__.copy()
    del data['_state']
    return data

  @classmethod
  def generate_for_user(cls, user, values):
    fdf_file = fdf_filename(user.id)
    output_file = output_filename(user.id)

    generate_pdf(cls.FIELDS, values, SOURCE_FILE, fdf_file, output_file)
    metadata = {
      'name': values['name']
    }
    store_in_s3(conn, S3_BUCKET_NAME, user.id, output_file, metadata)
    for field in cls.SENSITIVE_FIELDS:
      if values.get(field):
        del values[field]

    values['user_id'] = user.id
    return cls.objects.create(user=user, data=values)

  SENSITIVE_FIELDS = ["ssn_1", "ssn_2", "ssn_3"]

  # True if field is required
  FIELDS = {
    "ssn_1": True,
    "ssn_2": True,
    "ssn_3": True,
    "name": True,
    "address": True,
    "email": True,
    "servicer": True,
    "city": True,
    "state": True,
    "employed": True,
    "in_field": True,
    "out_of_field": True,
    "unemployed": True,
    "zip": True,
    "phone_primary_1": True,
    "phone_primary_2": True,
    "phone_primary_3": True,
    "phone_alt_1": None,
    "phone_alt_2": None,
    "phone_alt_3": None,
    "associates": None,
    "completed": None,
    "misleading_job_stats_check": None,
    "misleading_job_assistance_check": None,
    "misleading_job_other_check": None,
    "misleading_pass_rate_check": None,
    "misleading_accreditation_check": None,
    "certificate": None,
    "withdrew": None,
    "program_name": None,
    "school_address": None,
    "attendance_from": None,
    "school_address 2": None,
    "misleading_job_stats": None,
    "misleading_job_assistance": None,
    "misleading_job_other": None,
    "misleading_pass_rate": None,
    "misleading_accreditation": None,
    "school_name": None,
    "school_name 2": None,
    "school_name 3": None,
    "school_name 4": None
  }
