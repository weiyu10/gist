#!/bin/env python
# -*- coding: utf-8 -*-

# Description:
# Author: weiyu
# Email: spunkzwy@gmail.com

import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('0.0.0.0', 9999)
sock.bind(server_address)

while True:
    data, address = sock.recvfrom(4096)
    # print address
    print 'received %s' % data
    if data:
        sent = sock.sendto(data, address)
        print 'sended %s' % data
