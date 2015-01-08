from django.conf import settings
import os
from subprocess import call
import subprocess

__LVS_MODE = {'TCP':'-t','UDP':'-u','FWM':'-f'}

def ipvadmin_exists():
    return os.path.exists(settings.IPVSADMIN)

def delete_virtual_server(mode,port):
    command = [settings.IPVSADMIN,]
    command.append('-D') 
    command.append(__LVS_MODE[mode])
    command.append(port)
    return call(command,stderr=subprocess.STDOUT)

    