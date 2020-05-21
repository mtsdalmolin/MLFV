import os
import sys
import rpyc
import time
import signal
import socket
import subprocess


SERVER="127.0.0.1"
PORT=8889
host_ip=''
port=0
cli_port = 18811

def verify_cli_port(cli_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1',cli_port))
    sock.close()
    if result == 0:
        return False
    else:
        return True


def signal_handler(sig, frame):
    global cli_port
    info = [host_ip, cli_port]
    con.root.unsubscribe(info)
    time.sleep(1)
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    global cli_port

    ret = 1
    while not verify_cli_port(cli_port):
        cli_port+=1

    rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True
    try:
        con = rpyc.connect(SERVER, PORT, config=rpyc.core.protocol.DEFAULT_CONFIG)
    except:
        print("ERROR: Could not connect to server "+SERVER+" on port "+str(PORT))
        exit()

    host_ip = "127.0.0.1"
    libs = "os,numpy,sys,timeit,pandas,sklearn.ensemble,sklearn.preprocessing,sklearn.metrics"
    cpu = 3000
    mem = 8
    net = 94

    info = [host_ip, cli_port, libs, cpu, mem, net]
    print("Subscibing to "+SERVER+" on port "+str(PORT))
    con.root.subscribe(info)

    ret = subprocess.call("rpyc_classic.py -p "+str(cli_port)+" --host 0.0.0.0 2> /dev/null", shell=True)
    print ret


