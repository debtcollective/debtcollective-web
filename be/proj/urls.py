from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'be.proj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'be.proj.views.splash', name='splash'),
    url(r'^map/', 'be.proj.views.map', name='map'),
    url(r'^signup/', 'be.proj.views.signup', name='signup'),
)
