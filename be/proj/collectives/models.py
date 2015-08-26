from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from jsonfield import JSONField
from django.db.models.signals import pre_save

import datetime

class Action(models.Model):
  slug = models.SlugField(max_length=40, unique=True)
  name = models.CharField(max_length=100)
  description = models.TextField()
  byline = models.CharField(max_length=90, blank=True)
  link = models.CharField(max_length=150, null=True, blank=True)
  image = models.CharField(max_length=150, null=True, blank=True)
  active = models.BooleanField(default=True)
  featured = models.BooleanField(default=False)
  private = models.BooleanField(default=False)

  def __unicode__(self):
    return self.name

class Collective(models.Model):
  slug = models.SlugField(max_length=40, unique=True)
  name = models.CharField(max_length=100)
  description = models.TextField()
  actions = models.ManyToManyField(Action)
  image = models.CharField(max_length=150, null=True, blank=True)
  link = models.CharField(max_length=150, null=True, blank=True)

  def __unicode__(self):
    return self.name

def gen_link(path):
  def pre_save(sender, instance, **kwargs):
    if not instance.link:
      instance.link = '/%s/%s' % (path, instance.slug)
  return pre_save

pre_save.connect(gen_link('collectives'), sender=Collective)
pre_save.connect(gen_link('actions'), sender=Action)

class CollectiveMember(models.Model):
  MEMBER = 1
  ADMIN = 2

  CHOICES = (
    (MEMBER, 'Member'),
    (ADMIN, 'Moderator'),
  )

  user = models.ForeignKey(User)
  collective = models.ForeignKey(Collective)
  status = models.IntegerField(max_length=1, choices=CHOICES, null=False, default=MEMBER)

  def __unicode__(self):
    return '%s - %s' % (self.user, self.collective)

  def pretty_status(self):
    for c in self.CHOICES:
      if self.status is c[0]:
        return c[1]
    return None

class UserAction(models.Model):
  COMPLETED = 1
  ACTIVE = 2

  STATES = (
    (COMPLETED, 'Completed'),
    (ACTIVE, 'Active'),
  )

  status = models.IntegerField(max_length=1, choices=STATES, null=False, default=COMPLETED)
  user = models.ForeignKey(User)
  action = models.ForeignKey(Action)
  data = JSONField(blank=True)
  last_changed = models.DateTimeField(default=datetime.datetime.now())

  def __unicode__(self):
    return '%s %s' % (self.user, self.action)

