from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/ipvsstat/')),
    url(r'^ipvsstat/', include('ipvsstat.urls',namespace="ipvsstate")),
    url(r'^admin/', include(admin.site.urls)),
)
