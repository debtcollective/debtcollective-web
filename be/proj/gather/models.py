from django.db import models
from django.contrib import admin

class UserData(models.Model):
  user_id_secret = models.CharField(max_length=200)
  created_at = models.DateTimeField()
  location = models.CharField(max_length=200)

  @staticmethod
  def user_id_secret(user_id):
    """encrypt the given user id to create the user_id_secret"""
    m = hashlib.md5()
    m.update()

class Debt(models.Model):
  AUTO = 1
  HOME = 2
  STUDENT = 3
  CREDIT = 4
  MEDICAL = 5
  DEBT_CHOICES = (
    (AUTO, 'Auto'),
    (HOME, 'Home'),
    (STUDENT, 'Student'),
    (CREDIT, 'Credit'),
    (MEDICAL, 'Medical')
  )

  userdata = models.ForeignKey(UserData)
  amount = models.IntegerField()
  kind = models.IntegerField(max_length=1, choices=DEBT_CHOICES)
  last_payment = models.DateTimeField()

