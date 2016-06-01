import socket

def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n-1) + fib(n-2)


s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(("0.0.0.0", 9090))
s.listen(1)

while True:
    print("Waiting for connections")
    cs, remote_addr = s.accept()
    print (" Received connection on {}".format(remote_addr))
    while True:
        num = cs.recv(10)
        if not num:
            break
        val = fib(int(num))
        ret = str(val).encode('ascii') + b'\n'
        cs.send(ret)
        
    
