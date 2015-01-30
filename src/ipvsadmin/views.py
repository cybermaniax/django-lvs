from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse,HttpResponseServerError

from ipvsstat.lvs import ipvs
from ipvsadmin import ipvsadm
from ipvsadmin.forms import VirtualServerForm,RealServerForm
from ipvsadmin import controler 

@require_http_methods(["GET", "POST"])
def index(request):
    vsform = controler.virtualServerForm(request)
    rsform = controler.realServerForm(request)
    return render(request, 'ipvsadmin/index.html',{'ipvs':ipvs.ipvs(),'vsform':vsform,'rsform':rsform})

@require_http_methods(["GET"])
def ajax_delete_virtual_server(request,mode,port):
    if not ipvsadm.ipvadmin_exists():
        return HttpResponseServerError('<h1>Command ipvsadm not found</h1>')
    if 0 != ipvsadm.delete_virtual_server(mode, port):
        return HttpResponseServerError('<h1>Error with ipvsadm execution</h1>')
    return JsonResponse({'return':'OK'})

@require_http_methods(["GET"])
def ajax_delete_real_server(request,mode,port,realserver):
    if not ipvsadm.ipvadmin_exists():
        return HttpResponseServerError('<h1>Command ipvsadm not found</h1>')
    if 0 != ipvsadm.delete_real_server(mode, port,realserver):
        return HttpResponseServerError('<h1>Error with ipvsadm execution</h1>')
    return JsonResponse({'return':'OK'})

@require_http_methods(["GET"])
def ajax_weight(request,mode,port,realserver,weight,realsmode):
    if not ipvsadm.ipvadmin_exists():
        return HttpResponseServerError('<h1>Command ipvsadm not found</h1>')
    if 0 != ipvsadm.weight_real_server(mode, port,realserver,weight,realsmode.upper()):
        return HttpResponseServerError('<h1>Error with ipvsadm execution</h1>')
    return JsonResponse({'return':'OK'})


@require_http_methods(["GET"])
def ipvsadmin_table_content(request):
    return render(request, 'ipvsadmin/ipvsadminboad.html',{'ipvs':ipvs.ipvs()})

