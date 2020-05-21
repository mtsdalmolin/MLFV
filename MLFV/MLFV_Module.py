import rpyc
import sys
import signal

from rpyc.utils.server import ThreadedServer as Server #ThreadedServer ThreadPoolServer

from MLFV_Parsing import * 
from MLFV_Hosts import *
from MLFV_Manager import * 
import MLFV_DB
from util import *

db = None

class ReceiveChain(rpyc.Service):
   def on_connect(self,x):
       print("Chain received")
   def on_disconnect(self,x):
       print("Chain ended"),x
   def exposed_exec_chain(self, c, p):
       x = parse_chain(c, p)


class ReceiveClient(rpyc.Service):
    def exposed_subscribe(self, info):
        db.insert_reg({'ip':info[0], 'port':info[1], 'libs':info[2], 'cpu':info[3], 'mem':info[4], 'net':info[5]})
        print "Host " + str(info[0]) + ":" + str(info[1]) + " subscribed \n"
    def exposed_unsubscribe(self, info):
        print db.remove_reg({'ip':info[0], 'port':info[1]})
        print "Host " + str(info[0]) + ":" + str(info[1]) + " unsubscribed"



port_chain=8888
port_cli=8889
if __name__ == "__main__":
    rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True
    
    db = MLFV_DB.DataBase("override")

    print "Starting chain receiver in port", port_chain
    server_chain = Server(ReceiveChain, port=port_chain, backlog=10, protocol_config=rpyc.core.protocol.DEFAULT_CONFIG)
    server_chain._start_in_thread()

    print "Starting client receiver in port", port_cli
    server_cli = Server(ReceiveClient, port=port_cli, backlog=10, protocol_config=rpyc.core.protocol.DEFAULT_CONFIG)
    server_cli.start()
