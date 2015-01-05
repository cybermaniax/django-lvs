import os
import platform
import psutil
import socket
from datetime import datetime, timedelta
import time

def cpu_usage_total():
    return psutil.cpu_percent(interval=None, percpu=False)

def load():
    av1, av2, av3 = os.getloadavg()
    return {'1m':av1,'5m':av2,'15m':av3}

def __platform_info():
    ld = platform.linux_distribution()
    
    return {'machine':platform.machine(),
            'os_release':platform.release(),
            'os':platform.system(),
            'hostname':socket.gethostname(),
            'distname' : ld[0],
            'distname_version':ld[1],}
    
def uptime():
    return datetime.now() - datetime.fromtimestamp(psutil.boot_time())


def __nic_poll_stat():
    """Retrieve raw stats within an interval window."""
    pnic_before = psutil.net_io_counters(pernic=True)
    # sleep some time
    time.sleep(1)
    pnic_after = psutil.net_io_counters(pernic=True)
    return [pnic_before, pnic_after]

def nic_state():
    pnic_before, pnic_after = __nic_poll_stat()
    nic_names = list(pnic_after.keys())
    nic_names.sort(key=lambda x: sum(pnic_after[x]), reverse=True)
    rstate = dict()
    for name in nic_names:
        stats_before = pnic_before[name]
        stats_after = pnic_after[name]
        rstate[name] = [stats_after.bytes_sent,stats_after.bytes_sent - stats_before.bytes_sent,
                            stats_after.bytes_recv,stats_after.bytes_recv - stats_before.bytes_recv,
                            stats_after.packets_sent,stats_after.packets_sent - stats_before.packets_sent,
                            stats_after.packets_recv,stats_after.packets_recv - stats_before.packets_recv]
    return rstate
    
platform_info = __platform_info()

if __name__ == "__main__":
    nic_state()