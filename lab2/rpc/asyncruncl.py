import asyncrpc
import logging
import threading

from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)

def printRes(result) :
    print("Result: {}".format(result))

cl = asyncrpc.Client()
cl.run()

base_list = asyncrpc.DBList({'foo'})
result_list = cl.append('bar', base_list, printRes)
#print("Result: {}".format(result_list.value))

cl.stop()
