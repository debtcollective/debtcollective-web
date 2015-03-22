from django.test import TestCase
from proj.utils import get_s3_conn
from boto.s3.key import Key
from django.contrib.auth.models import User
from proj.arcs.models import DTRUserProfile

import json

TEST_BUCKET = 'corinthiandtr.dev'
conn = get_s3_conn()
bucket = conn.get_bucket(TEST_BUCKET)


TEST_DATA = {
  'name': 'this is awesome',
  'ssn_1': '234',
  'ssn_2': '555',
  'ssn_3': '123',
  'misleading_job_stats_check': True
}
class TestDTR(TestCase):

    def test_generate(self):
      dtrprofile = DTRUserProfile.generate(TEST_DATA)

      key = dtrprofile.s3_key().key

      user_data = dtrprofile.data
      self.assertEqual(user_data['key'], dtrprofile.id)
      self.assertEqual(user_data['name'], 'this is awesome')

      # make sure sensitive data is removed before database storage
      for field in DTRUserProfile.SENSITIVE_FIELDS:
        self.assertEqual(user_data.get(field), None)

      s3_key = bucket.get_key(key)

      # contents exist
      contents = s3_key.get_contents_as_string()
      self.assertTrue(len(contents) > 0)

      # url works
      url = dtrprofile.pdf_link()
      self.assertTrue(type(url), str)

      # name metadata exists
      name = s3_key.get_metadata('name')
      self.assertEqual(name, 'this is awesome')

      #cleanup
      bucket.delete_key(key)

    def test_generate_post(self):
      rs = self.client.post('/corinthian/dtr_generate', TEST_DATA)
      self.assertEqual(rs.status_code, 200)

      resp = json.loads(rs.content)

      dtrprofile = DTRUserProfile.objects.get(id=resp['id'])
      self.assertEqual(resp['id'], dtrprofile.id)
      self.assertTrue(resp['pdf_link'])


    def test_generate_two_users(self):
      dtrprofile = DTRUserProfile.generate({
        'name': 'i am the first user'
      })

      dtrprofile_two = DTRUserProfile.generate({
        'name': 'i am a second user'
      })

      key = dtrprofile.s3_key().key
      key_two = dtrprofile_two.s3_key().key

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

