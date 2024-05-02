import constRPC
import time
import threading
import logging

from context import lab_channel, lab_logging

#lab_logging.setup(stream_level=logging.INFO)
#logger = logging.getLogger('vs2lab.lab2.rpc.asynrpc')


ServerResponseRecieved = threading.Event


class DBList:
    def __init__(self, basic_list):
        self.value = list(basic_list)

    def append(self, data):
        self.value = self.value + [data]
        return self


class Client:
    def __init__(self):
        self.chan = lab_channel.Channel()
        self.client = self.chan.join('client')
        self.server = None

    def run(self):
        self.chan.bind(self.client)
        self.server = self.chan.subgroup('server')

    def stop(self):
        self.chan.leave('client')

    def append(self, data, db_list, callback):
        assert isinstance(db_list, DBList)

        msglst = (constRPC.APPEND, data, db_list)  # message payload
        self.chan.send_to(self.server, msglst)  # send msg to server
        #logger.info('client sent msg.')

        ack = self.chan.receive_from(self.server)  # wait for acknowledgement of server recieving msg
        #logger.info('client recieved ack')

        background = callback(self.chan, self.server) # invoke callback function
        background.start() # start new background thread waiting for server response

        counter = 0
        while ServerResponseRecieved == False:
            time.sleep(1)
            counter = counter + 1
            print("Seconds elapsed waiting: {}".format(counter)) # count and print seconds waiting for server result
        background.join() # execute background thread

        return ack[1]  # pass acknowledgement to caller


class Server:
    def __init__(self):
        self.chan = lab_channel.Channel()
        self.server = self.chan.join('server')
        self.timeout = 3

    @staticmethod
    def append(data, db_list):
        assert isinstance(db_list, DBList)  # - Make sure we have a list
        return db_list.append(data)

    def run(self):
        self.chan.bind(self.server)
        while True:
            msgreq = self.chan.receive_from_any(self.timeout)  # wait for any request
            if msgreq is not None:
                client = msgreq[0]  # see who is the caller
                msgrpc = msgreq[1]  # fetch call & parameters
                if constRPC.APPEND == msgrpc[0]:  # check what is being requested
                    self.chan.send_to({client}, "REQ_ACCEPTED")
                    time.sleep(10)
                    result = self.append(msgrpc[1], msgrpc[2])  # do local call
                    self.chan.send_to({client}, result)  # return response
                else:
                    pass  # unsupported request, simply ignore
