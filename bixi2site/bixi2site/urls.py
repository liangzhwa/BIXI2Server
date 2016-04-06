from django.conf.urls import patterns, include, url
from django.contrib import admin
import views
import settings

urlpatterns = patterns('',
    url(r'^report/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.REPORT_PATH}),
    url(r'^newversion/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.NEWVERSION_PATH}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rest/', include('rest.urls')),
    url(r'^$', views.login),
    url(r'^main$', views.index),
)
