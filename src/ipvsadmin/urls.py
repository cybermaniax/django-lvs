from django.conf.urls import patterns, url

from ipvsadmin import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^content/ipvadmin/table/dashboard$', views.ipvsadmin_table_content, name='content.ipvsadm.table'),
    url(r'^ajax/deletevs/(?P<mode>\w{3})/(?P<port>\d{1,21}|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,4})$', views.ajax_delete_virtual_server, name='ajax_delete_virtual_server'),
)