import threading
import time

import zmq

def worker_process(context, name):
    socket = context.socket(zmq.REP)
    socket.connect("inproc://workers")

    while True:
        print ("{} connected and waiting".format(name))
        data = socket.recv()
        print ("{} on {}".format(data, name))
        time.sleep(2)
        print ("{} is Done".format(name))
        socket.send("foo")
        
        
def create_worker_pool(context):
    workers = []
    for i in range(5):
        name = "thread_{}".format(i)
        w = threading.Thread(target = worker_process, args = (context, name))
        print ("Spawning {}".format(name))
        workers.append(w)
        w.start()
    return workers
        

def main():
    context = zmq.Context()
    server_socket = context.socket(zmq.DEALER)
    server_socket.bind("inproc://workers")
    pool = create_worker_pool(context)
    for i in range(100):
        server_socket.send_multipart(str(i))
    

if __name__ == '__main__':
    main()
