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

def main():
    """Server routine"""

    url_worker = "inproc://workers"
    url_client = "tcp://*:5555"

    # Prepare our context and sockets
    context = zmq.Context.instance()

    # Socket to talk to clients
    clients = context.socket(zmq.ROUTER)
    clients.bind(url_client)

    # Socket to talk to workers
    workers = context.socket(zmq.DEALER)
    workers.bind(url_worker)

    # Launch pool of worker threads
    for i in range(5):
        name = "worker_{}".format(i)
        thread = threading.Thread(target=worker_routine, args=(url_worker, name ))
        thread.start()
        start = clients.recv_multipart()
        print (start)


    # Initialize poll set
    poller = zmq.Poller()
    poller.register(clients, zmq.POLLIN)
    poller.register(workers, zmq.POLLIN)

    # Switch messages between sockets
    while True:
        socks = dict(poller.poll())

        if socks.get(clients) == zmq.POLLIN:
            message = clients.recv_multipart()
            print ("Message from client {}".format(message))
            workers.send_multipart(message)

        if socks.get(workers) == zmq.POLLIN:
            message = workers.recv_multipart()
            print ("Message from worker {}".format(message))
            clients.send_multipart(message)


    # We never get here but clean up anyhow
    clients.close()
    workers.close()
    context.term()

if __name__ == "__main__":
    main()
