import socket
import time

HOST = '103.37.152.1'
PORT = 80

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.close()
    time.sleep(1)
