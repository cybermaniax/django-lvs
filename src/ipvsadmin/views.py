from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from ipvsstat.lvs import ipvs

@require_http_methods(["GET", "POST"])
def index(request):
    return render(request, 'ipvsadmin/index.html',{'ipvs':ipvs.ipvs()})