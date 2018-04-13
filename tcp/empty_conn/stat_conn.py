#!/bin/env python
# -*- coding: utf-8 -*-

import sys
import dpkt
import socket


filename = sys.argv[1]

invalid_pack = 0
counter = 0
not_eth = 0
not_tcp = 0
tcpcounter = 0
udpcounter = 0
result = {}


def get_flags(tcp):
    '''result (syn, syn-ack, fin, fin-ack, rst)'''
    syn_flag = (tcp.flags & dpkt.tcp.TH_SYN) != 0
    ack_flag = (tcp.flags & dpkt.tcp.TH_ACK) != 0
    fin_flag = (tcp.flags & dpkt.tcp.TH_FIN) != 0
    rst_flag = (tcp.flags & dpkt.tcp.TH_RST) != 0

    if syn_flag:
        if ack_flag:
            return 'syn-ack'
        else:
            return 'syn'
    elif fin_flag:
        if ack_flag:
            return 'fin-ack'
        else:
            return 'fin'
    elif rst_flag:
        return 'rst'
    elif ack_flag:
        return 'ack'


def is_eth(pkt):
    eth = dpkt.ethernet.Ethernet(pkt)
    if eth.type == dpkt.ethernet.ETH_TYPE_IP:
        return True
    else:
        return False


def is_ipv4_tcp(pkt):
    eth = dpkt.ethernet.Ethernet(pkt)
    if is_eth(pkt):
        if eth.data.p == dpkt.ip.IP_PROTO_TCP:
            return True
        else:
            return False
    else:
        return False


def get_conn_key(ip, tcp):

    ip_src = socket.inet_ntop(socket.AF_INET, ip.src)
    ip_dst = socket.inet_ntop(socket.AF_INET, ip.dst)

    if tcp.sport > tcp.dport:
        conn_key = '%s_%d_%s_%d' % (ip_src, tcp.sport, ip_dst, tcp.dport)
    else:
        conn_key = '%s_%d_%s_%d' % (ip_dst, tcp.dport, ip_src, tcp.sport)

    return conn_key

conn_table = {}

def get_conn(conn_key):
    return conn_table.get(conn_key)


def conn_exist(conn_key):
    if conn_table.get(conn_key):
        return True
    else:
        return False


def conn_close(conn_key):
    conn = conn_table.get(conn_key)
    if conn['state'] == 'closed':
        return True
    else:
        return False


def new_conn(conn_key):
    conn = {}
    conn['state'] = 'syn_send'
    conn['count'] = 0
    conn_table[conn_key] = conn
    return conn


def process_syn(conn_key, tcp):
    if conn_exist(conn_key):
        if conn_close(conn_key):
            new_conn(conn_key)
        else:
            return 'drop'
    else:
        new_conn(conn_key)


def process_syn_ack(conn_key, tcp):
    if conn_exist(conn_key):
        conn = get_conn(conn_key)
        if conn['state'] == 'syn_send':
            conn['state'] = 'syn_received'
        else:
            return 'drop'
    else:
        return 'drop'


def process_ack(conn_key, tcp):
    if conn_exist(conn_key):
        conn = get_conn(conn_key)
        if conn['state'] == 'syn_received':
            conn['state'] = 'established'
        elif conn['state'] == 'established':
            conn['count'] = conn['count'] + 1
        else:
            return 'drop'

def process_fin(conn_key, tcp):
    if conn_exist(conn_key):
        conn = get_conn(conn_key)
        if conn['state'] == 'established':
            conn['state'] = 'closed'
        else:
            return 'drop'
    else:
        return 'drop'


for ts, pkt in dpkt.pcap.Reader(open(filename, 'r')):
    if not is_ipv4_tcp(pkt):
        continue

    ip = dpkt.ethernet.Ethernet(pkt).data
    tcp = ip.data

    conn_key = get_conn_key(ip, tcp)
    flags = get_flags(tcp)
    if flags == 'syn':
        process_syn(conn_key, tcp)
    elif flags == 'syn-ack':
        process_syn_ack(conn_key, tcp)
    elif flags == 'ack':
        process_ack(conn_key, tcp)
    elif flags in ['fin', 'fin-ack']:
        process_fin(conn_key, tcp)
    else:
        pass

empty_conn = 0
import json
print json.dumps(conn_table)

print len(conn_table)

empty_conn = 0
for conn_key, conn in conn_table.iteritems():
    if conn['count'] == 0 and conn['state'] == 'closed':
        empty_conn = empty_conn + 1

print empty_conn
