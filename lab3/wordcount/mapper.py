import pickle
import time
import sys

import zmq

import constPipe
import const 

me = str(sys.argv[1])
address = "tcp://" + constPipe.SRC + ":" + constPipe.SPORT  # splitter address

src = constPipe.SRC
print("me: {}".format(me))
if (me == "0") or (me == "3"):
    port1 = constPipe.RPORT10
    port2 = constPipe.RPORT20
elif me == "1":
    port1 = constPipe.RPORT11
    port2 = constPipe.RPORT21
elif me == "2":
    port1 = constPipe.RPORT12
    port2 = constPipe.RPORT22
else:
    print("Mapper unavailable")
    quit

context = zmq.Context()
pull_socket = context.socket(zmq.PULL)  # create a pull socket
push_socket1 = context.socket(zmq.PUSH)  # create a push socket
push_socket2 = context.socket(zmq.PUSH)  # create a push socket

pull_socket.connect(address)  # connect to splitter

address1 = "tcp://" + src + ":" + port1  # how and where to connect
push_socket1.bind(address1)  # bind socket to address
address2 = "tcp://" + src + ":" + port2  # how and where to connect
push_socket2.bind(address2)  # bind socket to address

time.sleep(1) # wait to allow all reducers to connect

reducer1Scheme = (const.reducerScheme[0])

while True:
    sentence = pickle.loads(pull_socket.recv())  # receive sentence from a splitter
    print("recieved sentence: {}".format(sentence))

    words = sentence.split() # split sentence into words

    for word in words:  # take each word in words
        if word[0] in reducer1Scheme: # check to which reducer word should get sent
            push_socket1.send(pickle.dumps(word))  # publish word to reducer 1
        else:
            push_socket2.send(pickle.dumps(word))  # publish word to reducer 2
