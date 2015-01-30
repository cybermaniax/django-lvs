
from ipvsadmin.forms import VirtualServerForm, RealServerForm
from django.contrib import messages
from ipvsadmin import ipvsadm

def virtualServerForm(request, prefix='vs-add'):
    if request.method == 'POST' and 'virtualServerForm' in request.POST:
        form = VirtualServerForm(request.POST, request.FILES, prefix=prefix)
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
                form = VirtualServerForm(prefix=prefix)
    else:
        form = VirtualServerForm(prefix='vs-add')

    return form

def realServerForm(request, prefix='rs-add'):
    if request.method == 'POST' and 'realServerForm' in request.POST:
        form = RealServerForm(request.POST, request.FILES, prefix=prefix)
        if form.is_valid():
            if 0 != ipvsadm.add_real_server(ip=form['ip'].value(),
                                            port=form['port'].value(),
                                            fwmark=form['fwmark'].value(),
                                            mode=form['vstype'].value(),
                                            route_type=form['type'].value(),
                                            real_server="ss",
                                            weight=form['weight'].value(),
                                            uthreshold=form['uthreshold'].value(),
                                            lthreshold=form['lthreshold'].value()):
                messages.error(request, 'Error with ipvsadm execution')
            else:
                messages.info(request, 'Real server added successfully')
                form = RealServerForm(prefix=prefix)
    else:
        form = RealServerForm(prefix='vs-add')

    return form

