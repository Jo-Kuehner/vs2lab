import constRPC
import time
import threading

from context import lab_channel

ServerResponseRecieved = threading.Event()
ServerResponseRecieved.clear()

class BackgroundThread (threading.Thread):
    def __init__(self, channel: lab_channel.Channel, server, callback):
        threading.Thread.__init__(self)
        self.chan = channel
        self.server = server
        self.callback = callback

    def run(self):
        res = self.chan.receive_from(self.server) # wait for server to respond
        ServerResponseRecieved.set()
        self.callback(res[1].value)


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
        ack = self.chan.receive_from(self.server)  # wait for acknowledgement of server recieving msg
        print("Server Ack: {}".format(ack[1]))

        background = BackgroundThread(self.chan, self.server, callback) # create new background thread waiting for server response
        background.start() # start background thread

        counter = 0
        while ServerResponseRecieved.is_set() is False:
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
