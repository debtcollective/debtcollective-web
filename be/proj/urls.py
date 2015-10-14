from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404
handler404 = 'proj.views.not_found'

import os
admin.autodiscover()

urlpatterns = patterns('',
  url(r'^admin/', include(admin.site.urls))
)

def basic_url(name, prefix=""):
  return url('^' + prefix + '%s$' % name, name, name=name)

urlpatterns += patterns('proj.collectives.views',
  url('^collectives/([\w-]+)$', 'collective', name='view_collective'),
  url('^actions/([\w-]+)$', 'action', name='view_action'),
  url('^actions', 'all_actions', name='view_actions'),
  url('^useractions/delete/(\d+)$', 'ua_delete', name='ua_delete')
)

## TODO: Move corinthian specific stuff to arcs.corinthian..
urlpatterns += patterns('proj.views',
  basic_url('login'),
  basic_url('logout'),
  url('^password_change$', auth_views.password_change),
  url('^password_change/done/$', auth_views.password_change_done, name='password_change_done'),
  url('^password_reset/$', auth_views.password_reset, name='password_reset'),
  url('^password_reset/done$', auth_views.password_reset_done, name='password_reset_done'),
  url('^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
  url('^reset/done$', 'password_reset_complete', name='password_reset_complete'),
  url('^activate$', 'activate', name='activate'),
  basic_url('signup'),
  basic_url('blog'),
  basic_url('thankyou'),
  basic_url('profile'),
  basic_url('solidarity'),
  basic_url('calculator'),
  basic_url('stripe_endpoint'),
  basic_url('howfartofree'),
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

urlpatterns += patterns('proj.arcs.dtr',
  url('^dtr/download/(\d+)/(\d+)$', 'dtr_download', name='dtr_download'),
  url('^dtr/view/(\d+)$', 'dtr_view', name='dtr_view'),
  url('^dtr/migrate$', 'dtr_migrate', name='dtr_migrate'),
  url('^dtr/data$', 'dtr_data', name='dtr_data'),
  url('^dtr/admin$', 'dtr_admin', name='dtr_admin'),
  url('^dtr/choice$', 'dtr_choice', name='dtr_choice'),
  url('^dtr_generate$', 'generate', name='generate'),
  basic_url('dtr_csv'),
  url('^corinthiandtr$', 'dtr_redirect', name='dtr_redirect'),
  url('^defense-to-repayment$', 'dtr', name='dtr')
)
urlpatterns += patterns('proj.arcs.dtr',
  basic_url('corinthiansignup'),
  basic_url('corinthiancollective'),
  basic_url('studentstrike'),
  basic_url('solidaritystrike'),
  basic_url('solidaritystrikeform'),
  basic_url('corinthiansolidarity')
)
