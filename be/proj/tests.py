from django.test.client import Client
from django.utils import unittest
from django.contrib.auth.models import User
from be.proj.gather.models import UserData, Debt

class DebtisTest(unittest.TestCase):

    def setUp(self):
      self.client = Client()

    def populateUsers(self):
      rs = self.client.post('/signup/',
          {'username': 'testing', 'password': 'testingpw'})
      self.assertEqual(rs.status_code, 200)

      user = User.objects.get(username='testing')
      self.assertEqual('testing', user.username)

    def tearDown(self):
      User.objects.all().delete()
      UserData.objects.all().delete()
      Debt.objects.all().delete()

class TestSignup(DebtisTest):

    def setUp(self):
      self.client = Client()

    def test_simple(self):
      # it can create a user from the frontend
      rs = self.client.post('/signup/',
          {'username': 'test', 'password': 'anoyther'})
      self.assertEqual(rs.status_code, 200)

      user = User.objects.get(username='test')
      self.assertEqual('test', user.username)

    def test_login(self):
      # it can login a user from the frontend
      username = 'testuser'
      password = 'testingpassword'
      rs = self.client.post('/signup/',
          {'username': username, 'password': password})
      self.assertEqual(rs.status_code, 200)

      user = User.objects.get(username=username)
      self.assertEqual(username, user.username)

      # bad password
      rs = self.client.post('/login/',
        {'username': username, 'password': 'this is a bad password'})
      self.assertEqual(rs.status_code, 500)

      # successful password
      rs = self.client.post('/login/',
        {'username': username, 'password': password})
      self.assertEqual(rs.status_code, 200)


    def test_location(self):
      # it can store and retrieve location from the frontend
      rs = self.client.post('/signup/',
          {'username': 'testingloc',
           'password': 'testingpw',
           'location': '47404'})
      self.assertEqual(rs.status_code, 200)

      user = User.objects.get(username='testingloc')
      self.assertEqual('testingloc', user.username)

      data = UserData.objects.get(user=user)
      self.assertEqual('47404', data.location)

      # it turns numeric data into character
      rs = self.client.post('/signup/',
          {'username': 'testingloc2',
           'password': 'testingpw',
           'location': 47404})
      self.assertEqual(rs.status_code, 200)

      user = User.objects.get(username='testingloc2')
      self.assertEqual('testingloc2', user.username)

      data = UserData.objects.get(user=user)
      self.assertEqual('47404', data.location)

    def test_debt(self):
      rs = self.client.post('/signup/',
          {'username': 'doingit',
           'password': 'testingpw',
           'location': '47404',
           'kind': 'home',
           'amount': 132200
           })

      self.assertEqual(rs.status_code, 200)

      user = User.objects.get(username='doingit')
      debt = Debt.objects.get(user=user)
      self.assertEqual(debt.kind, 'home')
      self.assertEqual(debt.amount, 132200)


      # TODO: add last_payment as a viable option
      # do we use ISO or unix time?
