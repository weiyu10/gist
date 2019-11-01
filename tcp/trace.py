#!/bin/env python
# -*- coding: utf-8 -*-

# Description: trace all network path
# Author: weiyu
# Email: spunkzwy@gmail.com


import sys
import time
import subprocess
import multiprocessing
from multiprocessing import Pool, Queue, Manager


def format_traceroute_output(output):
    net_path = []
    for line in output.split('\n')[1:-1]:
        dev_ip = line.split()[1]
        net_path.append(dev_ip)
    return net_path


def trace(src_port_base, src_port_count, dst_ip, dst_port, result_queue):
    result = []
    src_port_max = src_port_base + src_port_count
    for src_port in range(src_port_base, src_port_max):
        net_path = run_traceroute(src_port, dst_port, dst_ip)
        net_path_str = '->'.join(net_path)
        result_queue.put(net_path_str)


def run_traceroute(src_port, dst_port, dst_ip):
    cmd = "traceroute -n --sport=%s -p %s -T %s -q 1 -m 10 -w 0.5" % (src_port,
                                                                      dst_port,
                                                                      dst_ip)
    output = subprocess.check_output(cmd, shell=True)
    return format_traceroute_output(output)


if __name__ == "__main__":
    # src_port_count必须能够整除process_num
    process_num = multiprocessing.cpu_count() * 2
    src_port_base = 3000
    src_port_count = 12
    dst_ip = 'baidu.com'
    dst_port = 9999

    result_queue = Manager().Queue()
    p = Pool(process_num)
    per_process_src_port_count = src_port_count // process_num
    for i in range(process_num):
        per_process_src_port_base = src_port_base + \
            (i * per_process_src_port_count)
        result = p.apply_async(trace, args=(per_process_src_port_base,
                                           per_process_src_port_count,
                                           dst_ip,
                                           dst_port,
                                           result_queue))

    result = []
    try:
        for i in range(src_port_count):
            result.append(result_queue.get(timeout=1))
    except:
        pass
    result.get()
    for net_path in list(set(result)):
        print net_path
