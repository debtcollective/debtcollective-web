from django.test import TestCase
from proj.utils import get_s3_conn
from boto.s3.key import Key
from django.contrib.auth.models import User
from proj.arcs import dtr
from proj.collectives.models import Collective, UserAction, Action
from proj.arcs.models import DTRUserProfile

import copy
import json
import proj.settings as settings


TEST_BUCKET = 'corinthiandtr.dev'
conn = get_s3_conn()
bucket = conn.get_bucket(TEST_BUCKET)

TEST_USER = {
  'name': 'i am the duplicate user',
  'phone_primary_1': 111,
  'phone_primary_2': 333,
  'phone_primary_3': 222,
  'email': 'krmckelv@gmail.com',
  'school_name': 'everest',
  'servicer': 'navient',
  'misleading_job_stats_check': True,
  'certificate': 'associates',
  'attendance_to_month': 10,
  'misleading_quality_other': 'there were a bunch of things that were wrong'
}

TEST_USER2 = copy.deepcopy(TEST_USER)
TEST_USER2['name'] = 'name2'

class TestDTR(TestCase):

    def setUp(self):
      self.user = {
        'password': 'testingpassword',
        'email': 'testuser@test.com'
      }
      rs = self.client.post('/signup', self.user)
      self.user2 = {
        'password': 'testingpassword',
        'email': 'testuser2@test.com'
      }
      rs = self.client.post('/signup', self.user2)

      action = Action.objects.create(slug=settings.DTR_MODEL_SLUG, name='Defense to Repayment', description='dtr ya')

    def test_generate(self):
      user = User.objects.get(username=self.user['email'])
      dtrprofile, created = dtr.create_dtr_user_action(TEST_USER, user)
      dtr.make_a_pdf(dtrprofile)

      self.assertEqual(dtrprofile.data['name'], TEST_USER['name'])

      # make sure sensitive data is removed before database storage
      for field in dtr.SENSITIVE_FIELDS:
        self.assertEqual(dtrprofile.data.get(field), None)

      s3_key = dtr.s3_key(dtrprofile)

      # contents exist
      contents = s3_key.get_contents_as_string()
      self.assertTrue(len(contents) > 0)

      # url works
      url = dtr.pdf_link(dtrprofile)
      self.assertTrue(type(url), str)

      # name metadata exists
      name = s3_key.get_metadata('name')
      self.assertEqual(name, TEST_USER['name'])

      #cleanup
      bucket.delete_key(s3_key.key)

    def test_duplicate(self):
      user = User.objects.get(username=self.user['email'])
      user2 = User.objects.get(username=self.user2['email'])

      dtrprofile, created = dtr.create_dtr_user_action(TEST_USER, user)

      # duplicate, use the same data with different user! (how did that happen? idk)
      dtrprofile_dupe, created = dtr.create_dtr_user_action(TEST_USER, user2)

      action = Action.objects.get(name='Defense to Repayment')
      all_forms = UserAction.objects.filter(action=action)
      self.assertNotEqual(dtrprofile.data['key'], dtrprofile_dupe.data['key'])
      del dtrprofile.data['key']
      del dtrprofile_dupe.data['key']
      self.assertEqual(dtrprofile.data, dtrprofile_dupe.data)

      no_dupes = dtr.remove_dupes(all_forms)

      for form in no_dupes:
        for form_two in no_dupes:
          if form.id != form_two.id:
            self.assertNotEqual(form.data, form_two.data)

    def test_generate_post(self):
      # successful password. logged in
      rs = self.client.post('/login', self.user)
      self.assertEqual(rs.status_code, 302)

      rs = self.client.post('/dtr_generate', TEST_USER)
      self.assertEqual(rs.status_code, 200)

      resp = json.loads(rs.content)
      dtrprofile = UserAction.objects.get(id=resp['id'])
      self.assertEqual(resp['id'], dtrprofile.id)
      self.assertTrue(resp['pdf_link'])

    def test_generate_two_users(self):
      user = User.objects.get(username=self.user['email'])
      user2 = User.objects.get(username=self.user2['email'])

      dtrprofile, created = dtr.create_dtr_user_action(TEST_USER, user)
      dtr.make_a_pdf(dtrprofile)
      dtrprofile_two, created = dtr.create_dtr_user_action(TEST_USER2, user2)
      dtr.make_a_pdf(dtrprofile_two)

      s3_key = dtr.s3_key(dtrprofile)
      s3_key_two = dtr.s3_key(dtrprofile_two)

      # both contents exist
      contents = s3_key.get_contents_as_string()
      self.assertTrue(len(contents) > 0)

      contents_two = s3_key_two.get_contents_as_string()
      self.assertTrue(len(contents) > 0)

      # and are different!
      self.assertNotEqual(contents, contents_two)

      # metadata keys are different
      name = s3_key.get_metadata('name')
      self.assertEqual(name, 'i am the duplicate user')

      name = s3_key_two.get_metadata('name')
      self.assertEqual(name, 'name2')

      # cleanup
      bucket.delete_key(s3_key.key)
      bucket.delete_key(s3_key_two.key)

    def test_migration(self):
      # migrate from user1 to user2
      dtrprofile = DTRUserProfile.objects.create(data=TEST_USER)

      migrate_email = dtr.dtr_migrate_email(dtrprofile)
      self.assertTrue('pk=' in migrate_email)
      self.assertTrue('key=' in migrate_email)

      # no login gives login form
      rs = self.client.get('/dtr/migrate?pk={0}'.format(dtrprofile.id))
      self.assertEqual(rs.status_code, 200)

      # successful login
      rs = self.client.post('/login', self.user2)
      self.assertEqual(rs.status_code, 302)

      # bad secret key fails
      rs = self.client.get('/dtr/migrate?pk={0}&key=notakey'.format(dtrprofile.id))
      self.assertEqual(rs.status_code, 404)

      dtrprofile = DTRUserProfile.objects.get(id=dtrprofile.id)
      # good secret key success
      rs = self.client.get('/dtr/migrate?pk={0}&key={1}'.format(dtrprofile.id, dtrprofile.data['key']))
      self.assertEqual(rs.status_code, 302)

      useraction = UserAction.objects.get(user=User.objects.get(username=self.user2['email']))
      self.assertEqual(useraction.data, dtrprofile.data)
      self.assertEqual(useraction.user.username, self.user2['email'])
