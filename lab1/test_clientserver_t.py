"""
Simple client server unit test
"""

import logging
import threading
import unittest

import clientserver_t
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)


class TestEchoService(unittest.TestCase):
    """The test"""

    _telephoneDB = {
        "Markus Bauer": "52780574396",
        "Michael Bauer": "643643708598",
        "Lisa Meier": "5730496794634"
    } # create DB
    _server = clientserver_t.Server()  # create single server in class variable
    _server_thread = threading.Thread(target=_server.serve, args=(_telephoneDB,))  # define thread for running server

    @classmethod
    def setUpClass(cls):
        cls._server_thread.start()  # start server loop in a thread (called only once)

    def setUp(self):
        super().setUp()
        self.client = clientserver_t.Client()  # create new client for each test

    def test_telephone_get(self):  # each test_* function is a test
        """Test simple call"""
        msg = self.client.get("Bauer")
        self.assertEqual(msg, "Markus Bauer: 52780574396, Michael Bauer: 643643708598")

    def test_telephone_getAll(self):  # each test_* function is a test
        """Test simple call"""
        msg = self.client.getAll()
        self.assertEqual(msg, "Markus Bauer: 52780574396, Michael Bauer: 643643708598, Lisa Meier: 5730496794634")

    def tearDown(self):
        self.client.close()  # terminate client after each test

    @classmethod
    def tearDownClass(cls):
        cls._server._serving = False  # break out of server loop. pylint: disable=protected-access
        cls._server_thread.join()  # wait for server thread to terminate


if __name__ == '__main__':
    unittest.main()
