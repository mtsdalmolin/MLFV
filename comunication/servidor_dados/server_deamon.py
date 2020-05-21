import threading
import socket
import signal
import sys

'''
def signal_handler(sig, frame):
    s.close()
'''

def ip_discover():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('', 8886)

    sock.bind(server_address)

    response = 'okay '

    while True:
	    data, address = sock.recvfrom(4096)
	    data = str(data.decode('UTF-8'))
	    #print('Received ' + str(len(data)) + ' bytes from ' + str(address) )
	    #print('Data:' + data)
            response += str(address[0])
	    
	    if data == 'registration':
		    #print('responding...')
		    sent = sock.sendto(response.encode(), address)
                    response = 'okay '


def send_MLFV():
    s = socket.socket() 
    host = socket.gethostname() # Get local machine name
    port = 8887                 # Reserve a port for your service.
    s.bind(('', port))          # Bind to the port

    s.listen(100)                # Now wait for client connection.

    while True:
        c, addr = s.accept()     # Establish connection with client.
	f = open('MLFV_docker.zip','rb')
        print 'Got connection from', addr
        m = c.recv(1024)
        print 'Message from ', addr, ': ', m

        if m == 'subscribe':
            print "Sending..."
            
            l = f.read(1024)
            while (l):
                # print "Sending..."
                c.send(l)
                l = f.read(1024)
            #f.close()
            print "Done Sending"
            c.shutdown(socket.SHUT_WR)
            print c.recv(1024)
            c.close()


if __name__=='__main__':
    '''signal.signal(signal.SIGINT, signal_handler)'''
    #### discovering net_ip ####
    ip_d = threading.Thread(target=ip_discover)
    ip_d.start()

    #### sending package ####    
    connect = threading.Thread(target=send_MLFV)
    connect.start()

                
