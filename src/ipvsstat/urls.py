from django.conf.urls import patterns, url

from ipvsstat import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^ajax/dashboard$', views.ajax_dashboard, name='ajax.dashboard'),
    url(r'^ajax/nicdashboard$', views.ajax_nic_dashboard, name='ajax.nic_dashboard'),
)