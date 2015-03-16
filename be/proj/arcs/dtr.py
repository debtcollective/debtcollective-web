from fdfgen import forge_fdf
from boto.s3.key import Key
from proj.utils import get_s3_conn

import proj.settings as settings
import datetime
import subprocess
import sys
import json
import os

TMP_FILE_DIR = '/tmp'
SOURCE_FILE = os.path.join(os.path.dirname(os.getcwd()), 'dc_defense_form_1-3.pdf')

S3_BUCKET_NAME = 'corinthiandtr'
if settings.DEBUG:
  S3_BUCKET_NAME += '.dev'

conn = get_s3_conn()

def fdf_filename(key):
  return os.path.join(TMP_FILE_DIR, str(key) + '_data.fdf')

def output_filename(key):
  return os.path.join(TMP_FILE_DIR, str(key) + '_output.pdf')

def generate_for_user(user, values):
  key = user.id
  fdf_file = fdf_filename(key)
  output_file = output_filename(key)

  generate(values, fdf_file, output_file)
  metadata = {
    'name': values['name']
  }
  store_in_s3(key, output_file, metadata)
  return key

def store_in_s3(key, output_file, metadata=None):
  if not metadata:
    metadata = {}
  bucket = conn.get_bucket(S3_BUCKET_NAME)
  k = Key(bucket)
  k.key = key
  k.set_metadata('version', 1)
  for key, value in metadata.iteritems():
    k.set_metadata(key, value)
  k.set_contents_from_filename(output_file)

def generate(values, fdf_filename, output_filename):
  fdf_fields = []
  for fieldname, value in FIELDS.iteritems():
    fdf_fields.append((fieldname, values.get(fieldname, 'N/A')))

  fdf = forge_fdf("", fdf_fields, [], [], [])

  fdf_file = open(fdf_filename, "w")
  fdf_file.write(fdf)
  fdf_file.close()

  subprocess.call(['pdftk', SOURCE_FILE ,'fill_form', fdf_filename, 'output', output_filename])

FIELDS = {
  "ssn_1": None,
  "ssn_2": None,
  "ssn_3": None,
  "name": None,
  "address": None,
  "email": None,
  "servicer": None,
  "city": None,
  "state": None,
  "employed": None,
  "in_field": None,
  "out_of_field": None,
  "unemployed": None,
  "zip": None,
  "phone_primary_1": None,
  "phone_primary_2": None,
  "phone_primary_3": None,
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