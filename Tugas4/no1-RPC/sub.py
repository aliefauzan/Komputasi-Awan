import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)          # create a subscriber socket
socket.connect("tcp://127.0.0.1:12345")   # connect to the server
socket.setsockopt(zmq.SUBSCRIBE, b"TIME") # subscribe to TIME messages

for i in range(5):      # Five iterations
    time = socket.recv()  # receive a message related to subscription 
    print(time.decode())  # print the result      
