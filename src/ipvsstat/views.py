from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

from ipvsstat.lvs import platform_info
from ipvsstat.lvs import mem,ipvs
import ipvsstat.lvs as lvs

def __dashboardData():
    loadavg = lvs.load()
    mem_info = mem.memory_info()
    return {"loadavg_1m": loadavg['1m'],
               "loadavg_5m": loadavg['5m'],
               "loadavg_15m": loadavg['15m'],
                'machine':platform_info['machine'],
                'os':platform_info['os'],
                'os_release':platform_info['os_release'],
                'hostname':platform_info['hostname'],
                'distname':platform_info['distname'],
                'distname_version':platform_info['distname_version'],
                'uptime':str(lvs.uptime()).split('.')[0],
                'mem_perc_use':mem_info[0],
                'mem_used':mem_info[1],
                'mem_total':mem_info[2],
                'cpu_usage':lvs.cpu_usage_total(),
                'ipvs':ipvs.ipvs(),}

@require_http_methods(["GET", "POST"])
def index(request):
    context = __dashboardData()
    return render(request, 'ipvsstate/index.html',context)

@require_http_methods(["GET"])
def ipvsadmin_table_content(request):
    return render(request, 'ipvsstate/ipvsadminboad.html',{'ipvs':ipvs.ipvs()})

@require_http_methods(["GET"])
def ajax_dashboard(request):
    return JsonResponse(__dashboardData())

@require_http_methods(["GET"])
def ajax_nic_dashboard(request):
    return JsonResponse(lvs.nic_state())