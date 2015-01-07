from django.conf.urls import patterns, url

from ipvsadmin import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)