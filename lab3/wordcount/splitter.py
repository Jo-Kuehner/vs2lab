import pickle
import time

import zmq

import constPipe
import const

src = constPipe.SRC # set splitter host
prt = constPipe.SPORT # set splitter port

context = zmq.Context()
push_socket = context.socket(zmq.PUSH)  # create a push socket

address = "tcp://" + src + ":" + prt  # how and where to connect
push_socket.bind(address)  # bind socket to address

time.sleep(1) # wait to allow all mappers to connect

inputText = const.inputText
print("input text: {}".format(inputText))
outputText = const.inputText.split(".") # split text at each sentence end
print("output text: {}".format(outputText))

for sentence in outputText:  # take each sentence in outputText
    push_socket.send(pickle.dumps(sentence))  # send sentence to mappers
    print("sent sentence: {}".format(sentence))
    time.sleep(1)


