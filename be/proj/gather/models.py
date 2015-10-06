from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from simple_email_confirmation import SimpleEmailConfirmationUserMixin
from django.db.models.signals import post_save
from django.utils import timezone
from proj.collectives.models import Collective, CollectiveMember

class User(SimpleEmailConfirmationUserMixin, AbstractUser):
    pass

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
  created_at = models.DateTimeField(default=timezone.now)
  point = models.ForeignKey(Point, null=True)

def create_user_profile(sender, instance, created, **kwargs):
  if created:
    UserProfile.objects.create(user=instance)

def add_dc(sender, instance, created, **kwargs):
  if created:
    dc = Collective.objects.get(slug='debt-collective')
    CollectiveMember.objects.get_or_create(collective=dc, user=instance)

post_save.connect(create_user_profile, sender=User)
post_save.connect(add_dc, sender=User)

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
