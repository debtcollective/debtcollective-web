from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf.urls import handler404
handler404 = 'proj.views.not_found'

import os
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

def basic_url(name):
  return url(r'^%s' % name, name, name=name)


## TODO: Move corinthian specific stuff to arcs.corinthian..
urlpatterns += patterns('proj.views',
  basic_url('map'),
  basic_url('login'),
  basic_url('logout'),
  basic_url('signup'),
  basic_url('thankyou'),
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

urlpatterns += patterns('proj.arcs.corinthian',
  basic_url('dtr_generate'),
  basic_url('dtr_stats'),
  basic_url('dtr_download'),
  basic_url('dtr_view'),
  basic_url('knowyourstudentdebt'),
  basic_url('corinthiansignup'),
  basic_url('studentstrike'),
  basic_url('corinthiansolidarity')
)

urlpatterns += patterns('proj.arcs.views',
  basic_url('portal')
)


