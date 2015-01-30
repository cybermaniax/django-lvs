from django.conf.urls import patterns, url

from ipvsadmin import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^content/ipvadmin/table/dashboard$', views.ipvsadmin_table_content, name='content.ipvsadm.table'),
    url(r'^ajax/deletevs/(?P<mode>\w{3})/(?P<port>\d{1,21}|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,4})$', views.ajax_delete_virtual_server, name='ajax_delete_virtual_server'),
    url(r'^ajax/deleterealserv/(?P<mode>\w{3})/(?P<port>\d{1,21}|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,4})/(?P<realserver>\d{1,21}|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,4})$', views.ajax_delete_real_server, name='ajax_delete_real_server'),
    url(r'^ajax/weight/(?P<mode>\w{3})/(?P<port>\d{1,21}|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,4})/(?P<realserver>\d{1,21}|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,4})/(?P<weight>\d{1,4})/(?P<realsmode>\w{4,6})$', views.ajax_weight, name='ajax_weight'),
)