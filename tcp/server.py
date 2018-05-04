#!/bin/env python
# -*- coding: utf-8 -*-

# Description:
# Author: weiyu
# Email: spunkzwy@gmail.com

import time
import json
import thread
import threading
from socket import *


def handler(clientsock, addr):
    while True:
        data = clientsock.recv(1024)
        if not data:
            break
        clientsock.send(data)
    clientsock.close()


if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 9081
    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    serversock = socket(AF_INET, SOCK_STREAM)
    serversock.bind(ADDR)
    serversock.listen(5)

    while True:
        clientsock, addr = serversock.accept()
        '...connected from: ', addr
        thread.start_new_thread(handler, (clientsock, addr))
