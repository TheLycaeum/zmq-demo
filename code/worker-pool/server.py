"""

   Multithreaded Hello World server

   Author: Guillaume Aubert (gaubert) <guillaume(dot)aubert(at)gmail(dot)com>

"""
import socketserver
import time
import threading

import zmq

def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n-1) + fib(n-2)


def worker_routine(worker_url, name, context=None):
    """Worker routine"""
    context = context or zmq.Context.instance()
    # Socket to talk to dispatcher
    socket = context.socket(zmq.REP)

    socket.connect(worker_url)

    while True:

        data  = socket.recv()

        # print("{} Received request: [ {} ]".format(name, data))

        val = fib(int(data))
        ret = str(val).encode('ascii') + b'\n'
        #send reply back to client
        socket.send(ret)

def launch_workers(context, url_worker):
    # Socket to talk to workers
    workers = context.socket(zmq.DEALER)
    workers.bind(url_worker)

    # Launch pool of worker threads
    for i in range(5):
        name = "worker_{}".format(i)
        print ("Launching {}".format(name))
        thread = threading.Thread(target=worker_routine, args=(url_worker, name ))
        thread.start()

    return workers
        
def launch_broker(context, url_client, workers):
    # Socket to talk to clients
    clients = context.socket(zmq.ROUTER)
    clients.bind(url_client)

    thread = threading.Thread(target = zmq.proxy, args=(clients, workers))
    thread.start()

    return thread

class FibHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            num = self.request.recv(10)
            if not num:
                break
            self.server.zmq_socket.send(num)
            # val = fib(int(num))
            # ret = str(val).encode('ascii') + b'\n'
            message = self.server.zmq_socket.recv()
            # print("Received reply [%s]" % (message))
            self.request.send(message)

def launch_server(context, server_addr):

    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")


    socketserver.TCPServer.allow_reuse_address = True
    socketserver.TCPServer.zmq_socket = socket
    server = socketserver.TCPServer(server_addr, FibHandler)
    server.serve_forever()



def main():
    context = zmq.Context.instance()

    url_worker = "inproc://workers"
    url_client = "tcp://*:5555"
    server_addr = ("0.0.0.0", 9090)

    workers = launch_workers(context, url_worker)
    launch_broker(context, url_client, workers)

    launch_server(context, server_addr)


    


if __name__ == "__main__":
    main()
