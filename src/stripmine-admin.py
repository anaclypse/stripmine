#!/usr/bin/python

import socket
import sys

msg = " ".join(sys.argv[1:])
print "Sending: ", msg

HOST = 'localhost'    
PORT = 8945           
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send(msg)
data = s.recv(1024)
s.close()
print 'Received', repr(data)
