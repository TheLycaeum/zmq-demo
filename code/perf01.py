from socket import *
import time

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('localhost', 9090))

while True:
    start = time.time()
    sock.send(b'29')
    resp =sock.recv(100)
    end = time.time()
    print(end-start)
