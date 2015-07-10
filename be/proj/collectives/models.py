from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class Action(models.Model):
  slug = models.SlugField(max_length=40, unique=True)
  name = models.CharField(max_length=100)
  description = models.TextField()
  link = models.CharField(max_length=150, null=True, blank=True)
  image = models.CharField(max_length=150, null=True, blank=True)

  def __unicode__(self):
    return self.name

class Collective(models.Model):
  slug = models.SlugField(max_length=40, unique=True)
  name = models.CharField(max_length=100)
  description = models.TextField()
  actions = models.ManyToManyField(Action)
  members = models.ManyToManyField(User)
  image = models.CharField(max_length=150, null=True, blank=True)

  def __unicode__(self):
    return self.name

class UserAction(models.Model):
  DONE = 1
  APPROVED = 2

  STATES = (
    (DONE, 'Done'),
    (APPROVED, 'Approved'),
  )

  status = models.IntegerField(max_length=1, choices=STATES, null=False, default=DONE)
  user = models.ForeignKey(User)
  action = models.ForeignKey(Action)


  def __unicode__(self):
    return '%s %s' % (self.user, self.action)