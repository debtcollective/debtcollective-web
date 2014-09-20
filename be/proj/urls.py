from django.conf.urls import patterns, include, url
from django.contrib import admin

import os
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

def basic_url(name):
  return url(r'^%s/' % name, name, name=name)

urlpatterns += patterns('proj.views',
  basic_url('map'),
  basic_url('login'),
  basic_url('signup'),
  basic_url('thankyou'),
  basic_url('corinthian'),
  url(r'^$', 'splash', name='splash')
)

urlpatterns += patterns('proj.gather.views',
  basic_url('points'),
  basic_url('map_data'),
  basic_url('generate_map_json')
)
