"""

   Multithreaded Hello World server

   Author: Guillaume Aubert (gaubert) <guillaume(dot)aubert(at)gmail(dot)com>

"""
import time
import threading
import zmq

def worker_routine(worker_url, name, context=None):
    """Worker routine"""
    context = context or zmq.Context.instance()
    # Socket to talk to dispatcher
    socket = context.socket(zmq.REP)

    socket.connect(worker_url)

    while True:

        string  = socket.recv()

        print("{} Received request: [ {} ]".format(name, string))

        # do some 'work'
        time.sleep(1)

        #send reply back to client
        socket.send(b"World")

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

def launch_server(context, server_addr):
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    
    for request in range(1,11):
        socket.send(b"Hello")
        message = socket.recv()
        print("Received reply %s [%s]" % (request, message))



def main():
    context = zmq.Context.instance()

    url_worker = "inproc://workers"
    url_client = "tcp://*:5555"

    workers = launch_workers(context, url_worker)
    launch_broker(context, url_client, workers)

    launch_server(context, "")


    


if __name__ == "__main__":
    main()
