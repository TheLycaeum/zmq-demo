import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

print ("Waiting")

while True:
    message = socket.recv() # Get message
    print("Received request: %s" % message)

    time.sleep(1) # Simulate busy work
 
    socket.send(b"World") # Send response
