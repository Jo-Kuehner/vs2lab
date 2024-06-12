import pickle
import time
import sys

import zmq

import constPipe

me = str(sys.argv[1])
print("me: {}".format(me))
if (me == "0") or (me == "2"):
    address1 = "tcp://" + constPipe.SRC + ":" + constPipe.RPORT20  # 1st mapper
    address2 = "tcp://" + constPipe.SRC + ":" + constPipe.RPORT21  # 2nd mapper
    address3 = "tcp://" + constPipe.SRC + ":" + constPipe.RPORT22  # 3rd mapper
elif me == "1":
    address1 = "tcp://" + constPipe.SRC + ":" + constPipe.RPORT10  # 1st mapper
    address2 = "tcp://" + constPipe.SRC + ":" + constPipe.RPORT11  # 2nd mapper
    address3 = "tcp://" + constPipe.SRC + ":" + constPipe.RPORT12  # 3rd mapper
else:
    print("Mapper unavailable")
    quit

context = zmq.Context()
pull_socket = context.socket(zmq.PULL)  # create a pull socket

pull_socket.connect(address1)  # connect to mapper 1
pull_socket.connect(address2)  # connect to mapper 2
pull_socket.connect(address3)  # connect to mapper 3

time.sleep(1) 

wordcount = 0

while True:
    word = pickle.loads(pull_socket.recv())  # receive work from a source
    wordcount = wordcount + 1
    print("current wordcount: {}    reducer {} received new word '{}'".format(wordcount, me, word))
