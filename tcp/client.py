#!/bin/env python
# -*- coding: utf-8 -*-

# Description: A simeple TCP client
# Author: weiyu
# Email: spunkzwy@gmail.com


import socket
import random
import select
import time
import sys
import datetime
from multiprocessing import Pool, Process


def gen_random_message():
    return random.randint(100000, 999999)


def send_random_message(client):
    message = gen_random_message()
    client.sendall(str(message))
    data = ''
    for i in range(1, 20):
        recv_data = client.recv(1024)
        data = data + str(recv_data)
        if str(data) == str(message):
            break
        time.sleep(0.1)


def tcp_conn(dst_ip, dst_port, send_count, send_interval):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((dst_ip, dst_port))

    for i in range(1, send_count):
        time.sleep(send_interval)
        send_time = time.time()
        send_random_message(client)
        cost_time = time.time() - send_time
        if cost_time > 0.1:
            current_time = time.asctime(time.localtime(send_time))
            print '%s: cost_time=%s' % (current_time, cost_time)
            print client.getsockname()
    client.close()


if __name__ == '__main__':
    dst_ip = sys.argv[1]
    dst_port = int(sys.argv[2])

    for process_id in range(2):
        send_count = random.randint(1, 30)
        send_interval = random.uniform(0.1, 0.2)
        print 'process %d: send_count: %s send_interval:%s' % (process_id,
                                                               send_count,
                                                               send_interval)
        process = Process(target=tcp_conn, args=(dst_ip,
                                                 dst_port,
                                                 send_count,
                                                 send_interval))
        process.start()
