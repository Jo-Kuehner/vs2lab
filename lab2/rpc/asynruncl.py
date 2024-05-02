import asynrpc
import logging
import threading

from context import lab_channel, lab_logging

lab_logging.setup(stream_level=logging.INFO)


class AsyncCommunication(threading.Thread):
    def __init__(self, channel: lab_channel.Channel, server):
        threading.Thread.__init__(self)
        self.chan = channel
        self.server = server

    def run(self):
        res = self.chan.receive_from(self.server) # wait for server to respond
        asynrpc.ServerResponseRecieved.set()
        print("Result: {}".format(res[1]))

cl = asynrpc.Client()
cl.run()

base_list = asynrpc.DBList({'foo'})
result_list = cl.append('bar', base_list, AsyncCommunication)
#print("Result: {}".format(result_list.value))

cl.stop()
