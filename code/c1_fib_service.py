import socketserver

def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n-1) + fib(n-2)

class FibHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            num = self.request.recv(10)
            if not num:
                break
            val = fib(int(num))
            ret = str(val).encode('ascii') + b'\n'
            self.request.send(ret)

if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer(("0.0.0.0", 9090), FibHandler)
    server.serve_forever()
