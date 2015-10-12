from django.test.client import Client
from django.test import TestCase
from django.contrib.auth.models import User
from proj.gather.models import UserProfile, Debt, Point

import proj.settings as settings
import json


class TestSignup(TestCase):
    fixtures = ['7-14-15.json']

    def test_simple(self):
      # it can create a user from the frontend
      rs = self.client.post('/signup',
          {'email': 'test@test.com', 'password': 'anoyther'})
      self.assertEqual(rs.status_code, 200)

      user = User.objects.get(username='test@test.com')
      self.assertEqual('test@test.com', user.username)

    def test_login(self):
      # it can login a user from the frontend
      password = 'testingpassword'
      email = 'testuser@test.com'
      rs = self.client.post('/signup',
          {'email': email, 'password': password})
      self.assertEqual(rs.status_code, 200)

      user = User.objects.get(username=email)
      self.assertEqual(email, user.username)

      # bad password
      rs = self.client.post('/login',
        {'username': email, 'password': 'this is a bad password'})
      self.assertEqual(rs.status_code, 200)

      # successful password
      rs = self.client.post('/login',
        {'username': email, 'password': password})
      self.assertEqual(rs.status_code, 302)

    def test_points(self):
      Point.objects.create(latitude=12.23, longitude=-34.35, name="Albuquerque")
      Point.objects.create(latitude=12.23, longitude=-32.35, name="New York")
      Point.objects.create(latitude=42.23, longitude=-34.35, name="Newark")
      Point.objects.create(latitude=12.23, longitude=-31.25, name="San Francisco")

      rs = self.client.post('/points')
      self.assertEqual(rs.status_code, 200)

      resp = json.loads(rs.content)
      self.assertEqual(len(resp), 4)
      fields = resp[0]
      self.assertIn('name', fields)
      self.assertIn('latitude', fields)
      self.assertIn('longitude', fields)

    def test_map_data(self):
      Point.objects.create(latitude=12.23, longitude=-34.35, name="Albuquerque")
      Point.objects.create(latitude=12.23, longitude=-32.35, name="New York")
      Point.objects.create(latitude=42.23, longitude=-34.35, name="Newark")
      p1 = Point.objects.create(latitude=12.23, longitude=-31.25, name="San Francisco")

      rs = self.client.post('/signup',
          {'email': 'doingit',
           'password': 'testingpw',
           'kind': 'home',
           'amount': 132200,
           'point': p1.id
           })
      self.assertEqual(rs.status_code, 200)

      rs = self.client.post('/signup',
          {'email': 'doingit2',
           'password': 'testingpw',
           'kind': 'home',
           'amount': 132200,
           'point': p1.id
           })
      self.assertEqual(rs.status_code, 200)

      def test(rs):
        self.assertEqual(rs.status_code, 200)
        data = json.loads(rs.content)

        self.assertEqual(data['total_amount'], 132200 * 2)
        self.assertEqual(len(data['points']), 1)
        sf = data['points'][0]
        self.assertEqual(sf['name'], 'San Francisco')
        self.assertEqual(sf['sum_amount'], 132200 * 2)
        self.assertEqual(sf['num_users'], 2)

      rs = self.client.get('/map_data')
      test(rs)

      rs = self.client.get('/generate_map_json')
      self.assertEqual(rs.status_code, 500)


    def test_location(self):
      # it can store and retrieve point from the frontend
      p = Point.objects.create(latitude=12.23, longitude=-34.35, name="Albuquerque")
      rs = self.client.post('/signup',
          {'email': 'testingloc@yo.com',
           'password': 'testingpw',
           'point':  p.id})
      self.assertEqual(rs.status_code, 200)

      user = User.objects.get(username='testingloc@yo.com')
      self.assertEqual('testingloc@yo.com', user.username)

      data = user.get_profile()
      self.assertEqual(p.id, data.point.id)

      # it turns numeric data into character
      p = Point.objects.create(latitude=12.23, longitude=-32.35, name="New York")
      rs = self.client.post('/signup',
          {'email': 'testingloc2@yo.com',
           'password': 'testingpw',
           'point': p.id})
      self.assertEqual(rs.status_code, 200)

      user = User.objects.get(username='testingloc2@yo.com')
      self.assertEqual('testingloc2@yo.com', user.username)

      data = UserProfile.objects.get(user=user)
      self.assertEqual(p.id, data.point.id)

    def test_debt(self):
      p = Point.objects.create(latitude=12.23, longitude=-32.35, name="New York")
      rs = self.client.post('/signup',
          {'email': 'doingit@gmail.com',
           'password': 'testingpw',
           'kind': 'home',
           'amount': 132200,
           'point': p.id
           })
      self.assertEqual(rs.status_code, 200)

      user = User.objects.get(username='doingit@gmail.com')
      debt = Debt.objects.get(user=user)
      self.assertEqual(debt.kind, 'home')
      self.assertEqual(debt.amount, 132200)

      # TODO: add last_payment as a viable option
      # do we use ISO or unix time?
