from django.test import TestCase

class TestDTR(TestCase):

    def test_generate(self):
      # it can create a user from the frontend
      rs = self.client.post('/dtr_generate/',
          {'email': 'testemail@gmail.com',
           'password': 'anoyther'})

      self.assertEqual(rs.status_code, 200)

      user = User.objects.get(username='test')
      self.assertEqual('test', user.username)
