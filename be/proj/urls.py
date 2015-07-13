from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404
handler404 = 'proj.views.not_found'

import os
admin.autodiscover()

urlpatterns = patterns('',
  url(r'^admin/', include(admin.site.urls)),
  url('^change_password/done', auth_views.password_change_done, name='password_change_done')
)

def basic_url(name, prefix=""):
  return url('^' + prefix + '%s$' % name, name, name=name)

urlpatterns += patterns('proj.collectives.views',
  url('^collectives/([\w-]+)$', 'collective', name='view_collective'),
  url('^actions/([\w-]+)$', 'action', name='view_action'),
  url('^actions', 'all_actions', name='view_actions')
)

## TODO: Move corinthian specific stuff to arcs.corinthian..
urlpatterns += patterns('proj.views',
  basic_url('map'),
  basic_url('login'),
  basic_url('logout'),
  basic_url('change_password'),
  basic_url('signup'),
  basic_url('thankyou'),
  basic_url('profile'),
  basic_url('solidarity'),
  basic_url('calculator'),
  basic_url('stripe_endpoint'),
  url(r'^$', 'splash', name='splash'),
)

urlpatterns += patterns('proj.gather.views',
  basic_url('points'),
  basic_url('states'),
  basic_url('map_data'),
  basic_url('debt_choices'),
  basic_url('debt_total'),
  basic_url('generate_map_json')
)

def corinthian_url(name):
  return basic_url(name, prefix="corinthian/")

urlpatterns += patterns('proj.arcs.corinthian',
  corinthian_url('dtr_generate'),
  corinthian_url('dtr_csv'),
  corinthian_url('admin'),
  url('^corinthian/dtr/download/(\d+)/(\d+)$', 'dtr_download', name='dtr_download'),
  url('^corinthian/dtr/migrate/(\d+)$', 'dtr_migrate', name='dtr_migrate'),
  url('^corinthian/dtr/restore/(\d+)$', 'dtr_restore', name='dtr_restore'),
  url('^corinthian/dtr/view/(\d+)$', 'dtr_view', name='dtr_view'),
  basic_url('knowyourstudentdebt'),
  basic_url('corinthiandtr'),
  basic_url('corinthiansignup'),
  basic_url('corinthiancollective'),
  basic_url('studentstrike'),
  basic_url('solidaritystrike'),
  basic_url('solidaritystrikeform'),
  basic_url('corinthiansolidarity')
)

