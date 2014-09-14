from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'be.proj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

def basic_url(name):
  return url(r'^%s/' % name, name, name=name)

urlpatterns += patterns('be.proj.views',
  basic_url('map'),
  basic_url('login'),
  basic_url('signup'),
  basic_url('corinthian'),
  url(r'^$', 'splash', name='splash')
)

urlpatterns += patterns('be.proj.gather.views',
  basic_url('points'),
  basic_url('map_data')
)
