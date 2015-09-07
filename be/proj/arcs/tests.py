from django.test import TestCase
from proj.utils import get_s3_conn
from boto.s3.key import Key
from django.contrib.auth.models import User
from proj.arcs import dtr
from proj.collectives.models import Collective, UserAction

import json

TEST_BUCKET = 'corinthiandtr.dev'
conn = get_s3_conn()
bucket = conn.get_bucket(TEST_BUCKET)

TEST_DATA = {
  'name': 'this is awesome TEST!',
  'ssn_1': '234',
  'ssn_2': '555',
  'ssn_3': '123',
  'misleading_job_stats_check': True,
  'credential': 1,
  'attendance_to_month': 10
}

class TestDTR(TestCase):

    def test_generate(self):
      dtrprofile = dtr.create_dtr_user_action(TEST_DATA)

      key = dtrprofile.s3_key().key

      user_data = dtrprofile.data
      self.assertEqual(user_data['key'], dtrprofile.id)
      self.assertEqual(user_data['name'], TEST_DATA['name'])

      # make sure sensitive data is removed before database storage
      for field in dtr.SENSITIVE_FIELDS:
        self.assertEqual(user_data.get(field), None)

      s3_key = bucket.get_key(key)

      # contents exist
      contents = s3_key.get_contents_as_string()
      self.assertTrue(len(contents) > 0)

      # url works
      url = dtr.pdf_link(dtrprofile)
      self.assertTrue(type(url), str)

      # name metadata exists
      name = s3_key.get_metadata('name')
      self.assertEqual(name, TEST_DATA['name'])

      #cleanup
      bucket.delete_key(key)

    def test_duplicate(self):
      dupe = {
        'name': 'i am the duplicate user',
        'phone_primary_1': 111,
        'phone_primary_2': 333,
        'phone_primary_3': 222,
        'servicer': 'navient',
        'misleading_job_stats_check': True,
        'certificate': 'associates',
        'attendance_to_month': 10,
        'misleading_quality_other': 'there were a bunch of things that were wrong'
      }

      dtrprofile = dtr.generate(dupe)
      dtrprofile_dupe = dtr.generate(dupe)

      dtrprofile_one = dtr.generate({
        'name': 'i am the first user',
        'servicer': 'Great Lakes/Navient'
      })

      dtrprofile_two = dtr.generate({
        'name': 'i am a second user',
        'servicer': 'Great Lakes'
      })

      action = Action.objects.get(name='Defense to Repayment')
      all_forms = UserAction.objects.filter(action=action)
      self.assertEqual(dtrprofile.data, dtrprofile_dupe.data)

      no_dupes = dtr.remove_dupes(all_forms)

      for form in no_dupes:
        for form_two in no_dupes:
          if form.id != form_two.id:
            self.assertNotEqual(form.data, form_two.data)

    def test_generate_post(self):
      rs = self.client.post('/dtr_generate', TEST_DATA)
      self.assertEqual(rs.status_code, 200)

      resp = json.loads(rs.content)

      dtrprofile = UserAction.objects.get(id=resp['id'])
      self.assertEqual(resp['id'], dtrprofile.id)
      self.assertTrue(resp['pdf_link'])

    def test_generate_two_users(self):
      dtrprofile = dtr.generate({
        'name': 'i am the first user'
      })

      dtrprofile_two = dtr.generate({
        'name': 'i am a second user'
      })

      key = dtr.s3_key(dtrprofile).key
      key_two = dtr.s3_key(dtrprofile_two).key

      s3_key = bucket.get_key(key)
      s3_key_two = bucket.get_key(key_two)

      # both contents exist
      contents = s3_key.get_contents_as_string()
      self.assertTrue(len(contents) > 0)

      contents_two = s3_key_two.get_contents_as_string()
      self.assertTrue(len(contents) > 0)

      # and are different!
      self.assertNotEqual(contents, contents_two)

      # metadata keys are different
      name = s3_key.get_metadata('name')
      self.assertEqual(name, 'i am the first user')

      name = s3_key_two.get_metadata('name')
      self.assertEqual(name, 'i am a second user')

      # cleanup
      bucket.delete_key(key)
      bucket.delete_key(key_two)
