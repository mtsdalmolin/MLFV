import multiprocessing
import operator
from MLFV_DB import DataBase


def get_less_busy_host(hr):
    lb = DataBase("open").get_less_runs()
    return (lb['ip'],lb['port'])


def get_host(c):
    hr = get_compatible_hosts(c)
    if len(hr) == 0:
        print "Bug: no compatible host found!"
        return None
    h = get_less_busy_host(hr)

    return h


def get_compatible_hosts(c):
    hs = []
    hr = []
    db = DataBase("open")

    # get hosts considering cpu and memory constraints 
    hosts = db.get_hosts_cpu_mem(c.constr.cpu, c.constr.mem)

    for i in hosts:
        # filter network constraints 
        #TODO: Openstack & Ceilometer integration
        if (i[5] >= c.constr.net):
            hs.append((i[0],i[1],sorted(i[2].split(',')))) # append (host,port)
    l = sorted(c.constr.imports.split(','))
    for h,p,libs in hs:
        if len(set(l).intersection(libs)) == len(l):
            hr.append((h,p))

    print "HOSTS"
    print hr
    return hr

