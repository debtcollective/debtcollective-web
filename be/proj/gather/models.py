from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import post_save


class Point(models.Model):
  name = models.CharField(max_length=50, unique=True)
  latitude = models.FloatField()
  longitude = models.FloatField()

  def __unicode__(self):
    return self.name

  def to_json(self):
    data = self.__dict__.copy()
    del data['_state']
    return data


class States(models.Model):
  state = models.CharField(max_length='22')
  state_code = models.CharField(max_length='2', primary_key=True)

  def __unicode__(self):
    return self.state

  def to_json(self):
    data = {
      'state': self.state,
      'state_code': self.state_code
    }
    return data


class UserProfile(models.Model):
  user = models.OneToOneField(User, unique=True)
  created_at = models.DateTimeField(default=datetime.now)
  point = models.ForeignKey(Point, null=True)

def create_user_profile(sender, instance, created, **kwargs):
  if created:
    UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

class Debt(models.Model):
  AUTO = 'auto'
  HOME = 'home'
  STUDENT = 'student'
  CREDIT = 'credit'
  MEDICAL = 'medical'
  OTHER = 'other'

  DEBT_CHOICES = (
    (AUTO, 'Auto'),
    (HOME, 'Home'),
    (STUDENT, 'Student'),
    (CREDIT, 'Credit'),
    (MEDICAL, 'Medical'),
    (OTHER, 'Other')
  )

  user = models.ForeignKey(User)

  # required
  amount = models.IntegerField()

  # optional
  kind = models.CharField(max_length=7, choices=DEBT_CHOICES, null=True)
  last_payment = models.DateTimeField(null=True)

  def total(self):
    return self.objects.all().aggregate(Sum('amount'))
