"""
Client and server using classes
"""

import logging
import socket

import const_cs
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)  # init loging channels for the lab

# pylint: disable=logging-not-lazy, line-too-long



def searchDB(DB:dict, request):
    resDic = {}
    for kname in DB.keys():
        if (kname.count(request) > 0):
            kvalue = DB.get(kname)
            resDic.update({kname:kvalue})
    return resDic


def parseDB(DB:dict, request=""):
    if not request:
        resData = DB
    else:
        resData = searchDB(DB, request)
    i = len(resData)
    response = ""
    for kname, kvalue in resData.items():
        response = response + kname + ": " + kvalue
        i = i-1
        if i > 0:
            response = response + ", "
    return response



class Server:
    """ The server """
    _logger = logging.getLogger("vs2lab.lab1.clientserver.Server")
    _serving = True

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # prevents errors due to "addresses in use"
        self.sock.bind((const_cs.HOST, const_cs.PORT))
        self.sock.settimeout(3)  # time out in order not to block forever
        self._logger.info("Server bound to socket " + str(self.sock))

    def serve(self, telephoneDB={"Helena Bauer": "57849366434"}):
        """ Serve echo """
        self.sock.listen(1)
        self._logger.info("Server ready and waiting")
        while self._serving:  # as long as _serving (checked after connections or socket timeouts)
            try:
                # pylint: disable=unused-variable
                (connection, address) = self.sock.accept()  # returns new socket and address of client
                while True:  # forever
                    reqStream = connection.recv(1024)  # receive data from client
                    if not reqStream:
                        break  # stop if client stopped
                    request = reqStream.decode("ascii")
                    operation = request[0]
                    request = request.removeprefix(operation)
                    self._logger.info("Server recieved request: " + request + " Operation: " + operation)
                    if (operation.__eq__("G")):
                        response = parseDB(telephoneDB, request)
                        if not response:
                            response = "No matching Entry in Telephone book"
                        connection.send(response.encode("ascii"))
                        self._logger.info("Server sent response:" + response)
                    elif (operation.__eq__("A")):
                        response = parseDB(telephoneDB)
                        connection.send(response.encode("ascii"))
                        self._logger.info("Server sent response:" + response)
                    else: 
                        self._logger.info("Request invalid")
                        connection.send("Invalid Request".encode("ascii"))
                connection.close()  # close the connection
            except socket.timeout:
                pass  # ignore timeouts
        self.sock.close()
        self._logger.info("Server down.")




class Client:
    """ The client """
    logger = logging.getLogger("vs2lab.a1_layers.clientserver.Client")

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((const_cs.HOST, const_cs.PORT))
        self.logger.info("Client connected to socket " + str(self.sock))

    def get(self, searchKey="noInput"):
        """ Get specified telephone number """
        searchMsg = "G" + searchKey
        self.logger.info("Client sent request:" + searchMsg)
        self.sock.send(searchMsg.encode('ascii'))  # send encoded string as data
        data = self.sock.recv(1024)  # receive the response
        result = data.decode('ascii')
        self.logger.info("Client recieved response:" + result)
        print(result)  # print the result
        self.sock.close()  # close the connection
        self.logger.info("Client down.")
        return result
    
    def getAll(self, searchKey="A"):
        """ Get all telephone numbers """
        self.logger.info("Client sent request:" + searchKey)
        self.sock.send(searchKey.encode('ascii'))  # send encoded string as data
        data = self.sock.recv(1024)  # receive the response
        result = data.decode('ascii')
        self.logger.info("Client recieved response:" + result)
        print(result)  # print the result
        self.sock.close()  # close the connection
        self.logger.info("Client down.")
        return result

    def close(self):
        """ Close socket """
        self.sock.close()
