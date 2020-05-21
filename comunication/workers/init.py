from socket import *               # Import socket module
import os
import sys
import time
import timeit
import subprocess

#### FINDING SERVER ####

'''
start = time.time()
'''

# Create a UDP socket
sock = socket(AF_INET, SOCK_DGRAM)
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
sock.settimeout(5)

server_address = ('localhost', 8886)
message = 'registration'

try:
	while True:
		# Send data
		print('sending: ' + message)
		sent = sock.sendto(message.encode(), server_address)

		# Receive response
		print('waiting to receive')
		data, server = sock.recvfrom(4096)
		data = data.decode('UTF-8')
                print "+++++++++++++++++++++++++++  " + data + "  +++++++++++++++++++++++++++"
		if data.decode('UTF-8').startswith('okay'):
			print('Received confirmation')
			print('Server ip: ' + str(server[0]) + '\n')
			data = data[5:]
			print('My ip ' + str(data) + ' was registered' + '\n')
			break
		else:
			print('Verification failed')
		
		print('Trying again...')

finally:	
	sock.close()


#### RECIVING SOCKET TIME ####
import socket

s = socket.socket()         # Create a socket object
host = str(server[0])
port = 8887                 # Reserve a port for your service.

s.connect((host, port))
s.send("subscribe")

f = open('MLFV.zip','w')
l = s.recv(1024)
while (l):
    #print 'Reciving...'
    f.write(l)    
    l = s.recv(1024)    
f.close()
print "Done Receiving"
m = s.recv(1024)
print m
s.close()


#### UNZIPING AND LOADING MLFV ####

path_zip_file = 'MLFV.zip'
unzip = ['unzip', '-o', '-q', path_zip_file]
p = subprocess.call(unzip)
p = subprocess.call(unzip)


s = open("MLFV/init_client.py").read()
s = s.replace('$', ('"'+ str(server[0]) + '"'))
# print '--- str(server[0]) ---' + s + '-----'
s = s.replace('@', ('"'+ str(data) + '"'))
# print '--- str(data) ---' + s + '-----'
f = open("MLFV/init_client.py", 'w')
f.write(s)
f.close()

zip_ = ['zip', '-r', 'MLFV.zip', 'MLFV']
p = subprocess.call(zip_)

if len(sys.argv) > 3:
    if (sys.argv[3] == 0):
        True 
	'''Se 0 nao buildar o docker, apenas inicializar'''
    else:
        dockerfile = ['docker', 'build', '-t', 'mlfv/docker:2.0', '.']
        p = subprocess.call(dockerfile)

'''
stop = time.time()
print(stop-start)
'''

'''
client = docker.from_env()
client.containers.run("mlfv/docker:2.0", "sleep infinity", detach=True)
'''

dockerrun = ['docker', 'run', '-ti', '--net=host', 'mlfv/docker:2.0']
p = subprocess.call(dockerrun)

'''
stop = time.time()
print(stop-start)
'''
