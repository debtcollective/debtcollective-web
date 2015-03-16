from django.test import TestCase
from proj.utils import get_s3_conn
from boto.s3.key import Key
from django.contrib.auth.models import User

import proj.arcs.dtr as dtr

class TestDTR(TestCase):

    def test_generate(self):
      # it can create a user from the frontend
      rs = self.client.post('/signup/',
          {'username': 'test', 'password': 'anoyther'})
      self.assertEqual(rs.status_code, 200)

      user = User.objects.get(username='test')
      self.assertEqual('test', user.username)

      TEST_BUCKET = 'corinthiandtr.dev'

      key = dtr.generate_for_user(user, {
        'name': 'this is awesome'
      })

      self.assertEqual(key, user.id)

      conn = get_s3_conn()
      bucket = conn.get_bucket(TEST_BUCKET)
      s3_key = bucket.get_key(key)

      contents = s3_key.get_contents_as_string()
      self.assertTrue(len(contents) > 0)

      name = s3_key.get_metadata('name')
      self.assertEqual(name, 'this is awesome')




