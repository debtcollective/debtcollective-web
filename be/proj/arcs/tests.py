from django.test import TestCase
from proj.utils import get_s3_conn
from boto.s3.key import Key
from django.contrib.auth.models import User
from proj.arcs.models import DTRUserProfile

TEST_BUCKET = 'corinthiandtr.dev'
conn = get_s3_conn()
bucket = conn.get_bucket(TEST_BUCKET)

class TestDTR(TestCase):

    def test_generate(self):
      # it can create a user from the frontend
      rs = self.client.post('/signup/',
          {'username': 'test', 'password': 'anoyther'})
      self.assertEqual(rs.status_code, 200)

      user = User.objects.get(username='test')
      self.assertEqual('test', user.username)

      dtrprofile = DTRUserProfile.generate_for_user(user, {
        'name': 'this is awesome',
        'ssn_1': '234',
        'ssn_2': '555',
        'ssn_3': '123'
      })

      key = dtrprofile.s3_key()

      user_data = dtrprofile.data
      self.assertEqual(user_data['user_id'], user.id)
      self.assertEqual(user_data['name'], 'this is awesome')
      for field in DTRUserProfile.SENSITIVE_FIELDS:
        self.assertEqual(user_data.get(field), None)

      s3_key = bucket.get_key(key)

      # contents exist
      contents = s3_key.get_contents_as_string()
      self.assertTrue(len(contents) > 0)

      # name metadata exists
      name = s3_key.get_metadata('name')
      self.assertEqual(name, 'this is awesome')

      #cleanup
      bucket.delete_key(key)

    def test_generate_two_users(self):
      rs = self.client.post('/signup/',
          {'username': 'test', 'password': 'anoyther'})
      self.assertEqual(rs.status_code, 200)

      rs = self.client.post('/signup/',
          {'username': 'test2', 'password': 'anoyther'})
      self.assertEqual(rs.status_code, 200)

      user = User.objects.get(username='test')
      self.assertEqual('test', user.username)
      user_two = User.objects.get(username='test2')
      self.assertEqual('test2', user_two.username)

      dtrprofile = DTRUserProfile.generate_for_user(user, {
        'name': 'i am the first user'
      })

      dtrprofile_two = DTRUserProfile.generate_for_user(user_two, {
        'name': 'i am a second user'
      })

      self.assertEqual(dtrprofile.user.id, user.id)
      self.assertEqual(dtrprofile_two.user.id, user_two.id)

      key = dtrprofile.s3_key()
      key_two = dtrprofile_two.s3_key()

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

