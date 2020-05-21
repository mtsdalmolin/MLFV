import sqlite3
import os


class DataBase:
    def __init__(self):
        try:
            self._restart_()
            self.con = sqlite3.connect('mlfv.db')
            self.cursor = self.con.cursor()
            self.cursor.execute("""
            CREATE TABLE hosts (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    ip TEXT NOT NULL,
                    port INTEGER NOT NULL,
                    libs TEXT NOT NULL,
                    cpu INTEGER NOT NULL,
                    mem INTEGER NOT NULL,
                    net INTEGER NOT NULL,
                    runs INTEGER
            );
            """)
        except:
            self.con = sqlite3.connect('mlfv.db')
            self.cursor = self.con.cursor()

    def insert_reg(self, r):
        try:
            data = (r['ip'], r['port'], r['libs'], r['cpu'], r['mem'], r['net'], 0)

            self.cursor.execute("""
            INSERT INTO hosts (ip, port, libs, cpu, mem, net, runs)
            VALUES (?,?,?,?,?,?,?)
            """, data)

            self.con.commit()
        except:
            print "Nao foi possivel inserir o registro"

    def remove_reg(self, r):
        try:
            ip = r['ip']
            port = r['port']

            self.cursor.execute("""
            DELETE FROM hosts
            WHERE ip=? AND port=?
            """, (ip, port))

            self.con.commit()
        except:
            print "Nao foi possivel remover o registro"

    def get_hosts_cpu_mem(self, cpu, mem):
        try:
            print "cpu: ", cpu, "  mem: ", mem
            ret = []

            self.cursor.execute("""
            SELECT * FROM hosts
            WHERE cpu>=? AND mem>=?
            GROUP BY ip,port,libs,cpu,mem,net
            """, (cpu, mem))

            for reg in self.cursor.fetchall():
                a = []
                for value in reg:
                    a.append(value)
                ret.append(a[1:-1])
            return ret
        except:
            print("Error: no client!")
            return None

    def get_less_runs(self):
        self.cursor.execute("""
        SELECT * FROM hosts
        ORDER BY runs
        """)

        r = self.cursor.fetchone()
        if r:
            self.cursor.execute("""
            UPDATE hosts
            SET runs=?
            WHERE id=?
            """, ((r[-1] + 1), r[0]))
            self.con.commit()

            a = {'ip': r[1], 'port': r[2], 'libs': r[3], 'cpu': r[4], 'mem': r[5], 'net': r[6]}
            return a

    def get_less_runs(self, hosts):
        self.cursor.execute("""
        SELECT * FROM hosts
        ORDER BY runs
        """)

        reg = self.cursor.fetchall()
        for r in reg:
            for i in hosts:
                if (r[1] == i[0] and r[2] == i[1]):
                    self.cursor.execute("""
                    UPDATE hosts
                    SET runs=?
                    WHERE id=?
                    """, ((r[-1] + 1), r[0]))
                    self.con.commit()
                    a = {'ip': r[1], 'port': r[2], 'libs': r[3], 'cpu': r[4], 'mem': r[5], 'net': r[6]}
                    return a
        return None

    def print_all(self):
        self.cursor.execute("""
        SELECT * FROM hosts
        """)

        for i in self.cursor.fetchall():
            print i

    def _restart_(self):
        try:
            os.remove("mlfv.db")
        except:
            return
