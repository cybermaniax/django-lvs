'''
Created on 18 gru 2014

@author: ghalajko
'''
import psutil


def memory_info():
    mem = psutil.virtual_memory()
    used = mem.total - mem.available
    return [mem.percent,int(used / 1024 / 1024),int(mem.total / 1024 / 1024)]

