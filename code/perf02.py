# requests/sec of fast requests

from socket import *
import time

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('localhost', 9090))

n = 0

from threading import Thread

def monitor():
    global n
    while True:
        time.sleep(1)
        print(n, 'reqs/sec')
        n = 0
Thread(target=monitor).start()

while True:
    sock.send(b'25')
    resp =sock.recv(100)
    n += 1
