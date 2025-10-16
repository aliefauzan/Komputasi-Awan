import zmq
import time

context = zmq.Context()         
socket = context.socket(zmq.PUB)          # create a publisher socket
socket.bind("tcp://*:12345")              # bind socket to the address
while True:                    
    time.sleep(5)                           # wait every 5 seconds
    t = "TIME " + time.asctime()
    socket.send(t.encode())                 # publish the current time