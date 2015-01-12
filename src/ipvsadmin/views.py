from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse,HttpResponseServerError

from ipvsstat.lvs import ipvs
from ipvsadmin import ipvsadm
from ipvsadmin.forms import VirtualServerForm
from django.contrib import messages

@require_http_methods(["GET", "POST"])
def index(request):
    
    if request.method == 'POST':
        form = VirtualServerForm(request.POST)
        if form.is_valid():
            
            if 0 != ipvsadm.add_virtual_server(ip=form['ip'].value(),
                                       port=form['port'].value(),
                                       fwmark=form['fwmark'].value(),
                                       mode=form['type'].value(),
                                       peristtimeout=form['peristtimeout'].value(),
                                       scheduler=form['scheduler'].value(),):
                messages.error(request, 'Error with ipvsadm execution')
            else:
                messages.info(request, 'Virtual server added successfully')
            
            
        return render(request, 'ipvsadmin/index.html',{'ipvs':ipvs.ipvs(),'vsform':form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = VirtualServerForm()
    return render(request, 'ipvsadmin/index.html',{'ipvs':ipvs.ipvs(),'vsform':form})

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

