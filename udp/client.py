#!/bin/env python
# -*- coding: utf-8 -*-

# Description:
# Author: weiyu
# Email: spunkzwy@gmail.com

import socket
import time
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.bind(('10.20.183.8', int(sys.argv[1])))
#sock.bind(('10.20.183.8', 61289))
#sock.bind(('10.20.183.8', 61288))

server_address = ('10.26.38.25', 9999)

for i in range(1, 1000):
    message = str(i)
    time.sleep(0.1)
    # Send data
    print >>sys.stderr, 'sending "%s"' % message
    sent = sock.sendto(message, server_address)

    # Receive response
    print >>sys.stderr, 'waiting to receive'
    data, server = sock.recvfrom(4096)
    print >>sys.stderr, 'received "%s"' % data

sock.close()
