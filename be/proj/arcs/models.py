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
basepath = settings.TEMPLATE_DIRS[0]
SOURCE_FILE = os.path.join(basepath, 'debtcollective-wizard/borrower_defense_to_repayment.pdf')
DTR_FIELDS_FILE = os.path.join(os.path.dirname(__file__), 'dtr_fields.json')

def fdf_filename(key):
  return os.path.join(TMP_FILE_DIR, str(key) + '_data.fdf')

def output_filename(key):
  return os.path.join(TMP_FILE_DIR, str(key) + '_output.pdf')

class DTRUserProfile(models.Model):
  #   ##
  #   we don't create any more dtruserprofiles.

  #  -> we moved all methods off the model into the dtr.py file
  #     -> all methods take a UserAction so they can get at the id and data
  #  -> generates a user if the user isn't logged in
  #  -> DTRProfile.generate will update the existing user action if it already exists
  #  -> if the user action doesn't exist, create it and mark it as UserAction.COMPLETED
  data = JSONField()

  def __unicode__(self):
    return self.data['email']
