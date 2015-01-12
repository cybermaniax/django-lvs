'''
Created on 18 gru 2014

@author: ghalajko
'''
from django.conf import settings

__lvs_version = None

import string
import os.path


if not os.path.isfile(settings.IP_VS_FILE):
    raise RuntimeError("LVS is disabled. File \'"+os.path.abspath(settings.IP_VS_FILE)+"\' not found.")

def isExist_virtual_server(port):
    for vsr in ip_vs_parse():
        if port in vsr.port:
            return True
    return False

def ip_vs_stat():
    ipvs = []
    with open(settings.IP_VS_STAT_FILE, 'rb') as f:
        for line in f:
            ipvs += [' '+line]
    return ipvs

def ipvs():
    retval = []
    for vep in ip_vs_parse():
        drels = []
        for rels in vep.real_servers:
            drels.append({'ip':rels._ip,
                          'port':rels._port,
                          'forward_mode':rels._forward_mode,
                          'weight':rels._weight,
                          'active_conn':rels._active_conn,
                          'inact_conn':rels._inact_conn
                          })
            
        retval.append({'mode':vep.mode,
             'port':vep.port,
             'scheduler':vep.scheduler,
             'persistent':vep.persistent,
             'persistent_timeout':vep.persistent_timeout,
             'flags':vep.flags,
             'realserv':drels,
             })
    return retval

def ip_vs_parse():
    global __lvs_version
    v_endpoints = []
    with open(settings.IP_VS_FILE, 'rb') as f:
        if __lvs_version is None:
            __lvs_version = f.readline()
        else:
            next(f)

        # Skip 2 line heder
        next(f)
        next(f)

        current_v_edpoint = None

        for line in f:
            splited_line = line.split()
            if splited_line[0] == "->" and current_v_edpoint is not None:
                rs = RealServer(splited_line)
                current_v_edpoint.add_real_server(rs)
            else:
                current_v_edpoint = VirtualEndPoint(splited_line)
                v_endpoints.append(current_v_edpoint)
        
    return v_endpoints

def _hexToInt(hexstr):
    return int(hexstr,16)

def _parce_to_ip(hexip):
    ip_l = []
    for x in range(0, 4):
        pozs = x*2
        poze = pozs+2
        ip_l += [str(_hexToInt(hexip[pozs:poze]))]
    return string.join(ip_l,'.')

def _parce_to_port(hexip):
    splited_hexip = hexip.split(':')
    v = splited_hexip[1].lstrip('0')
    v = [v,'0'][len(v) <= 0] 
    return str(_hexToInt(v))

class VirtualEndPoint(object):

    def __init__(self, args):
        self.mode = args[0]
        self.port = args[1]
        self.scheduler = args[2]
        if 3 < len(args):
            self.persistent = args[3]
            self.persistent_timeout = int(args[4])/1000 # msec to sec
            self.flags = args[5]
        else:
            self.persistent,self.persistent_timeout,self.flags = '','',''
        self.__real_servers = []
        if 'TCP' == self.mode or 'UDP' == self.mode:
            self.port = _parce_to_ip(self.port)+':'+_parce_to_port(self.port)
        elif 'FWM' == self.mode:
            self.port = str(_hexToInt(self.port))

    @property
    def real_servers(self):
        return self.__real_servers
    
    def sort_real_servers(self):
        self.__real_servers = sorted(self.__real_servers)

    def add_real_server(self, real_server):
        self.__real_servers.append(real_server)
        
    def __repr__(self):
        return  "(%s %s %s)" % (self.mode, self.port, ''.join(str(v) for v in self.__real_servers))

class RealServer(object):

    def __init__(self, args):
        self._ip = _parce_to_ip(args[1])
        self._port = _parce_to_port(args[1])
        self._forward_mode = args[2]
        self._weight = int(args[3])
        self._active_conn = args[4]
        self._inact_conn = args[5]

    def __repr__(self):
        return "(%s a=%s ina=%s)" % (self._ip,self._active_conn,self._inact_conn)

    def __cmp__(self, other):
        if hasattr(other, '_ip'):
            return cmp(self._ip,other._ip)
