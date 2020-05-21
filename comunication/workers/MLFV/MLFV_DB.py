import sys
from pydblite import Base
import numpy as np


class DataBase():
    def __init__(self, mode):
        self.db = Base("./mlfv_hosts.pdl")
        self.db.create('ip', 'port', 'libs', 'cpu', 'mem', 'net', 'runs', mode=mode)

    def insert_reg(self, r):
        if (len(r) < 6):
            print("Bad insertion")
            return False
        if self.db.exists():
            print self.db.insert(ip=r['ip'], port=r['port'], libs=r['libs'], cpu=r['cpu'], mem=r['mem'], net=r['net'], runs=0)
            self.db.commit()
            return True


    def remove_reg(self, r):
        if self.db.exists():
            for i in self.db:
                if i['ip'] == r['ip'] and i['port'] == r['port']:
                    self.db.delete(i)
                    self.db.commit()
                    print str(i['ip']) + " removed\n"
                    return True
        return False

    def print_all(self):
        if self.db.exists():
            for r in self.db:
                print r

    def get_less_runs(self):
        if self.db.exists():
            less_runs = sys.maxsize
            for r in self.db:
                if (r['runs'] < less_runs):
                    new_host = r
                    less_runs = r['runs']
            new_host['runs'] += 1
            self.db.commit()
            return new_host

    def get_hosts_cpu_mem(self, cpu, mem):
        print "cpu", cpu, mem
        ret = []
        if self.db.exists():
            for r in (self.db("cpu") >= cpu) & (self.db("mem") >= mem):
                ret.append([r['ip'], r['port'], r['libs'], r['cpu'], r['mem'], r['net']])
            #ret = [r for r in self.db if r['cpu'] >= cpu and r['mem'] >= mem]
            return ret
        else:
            print("Error: no client!")
            return None

    def get_registers_values(self):
        if self.db.exists():
            l = []
            for r in self.db:
                l.append([r['ip'], r['port'], r['libs'], r['cpu'], r['mem'], r['net']])
            a = np.array(l, dtype=object)
            return a
