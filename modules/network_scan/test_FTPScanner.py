#!/usr/bin/env python
# -*- coding:utf-8 -*-

from modules.network_scan.FTPScanner import FTPScanner
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import unittest
from tempfile import mkdtemp
import multiprocessing
from time import sleep

import http.server
import socketserver
import os

TEST_CREDS = (("admin", "admin"), ("1", "1"), ('user', 'password'))
PORT = 2121


def run_anonymous_ftp(temp_dir):
    authorizer = DummyAuthorizer()
    authorizer.add_anonymous(temp_dir)
    handler = FTPHandler
    handler.authorizer = authorizer
    server = FTPServer(("127.0.0.1", PORT), handler)
    server.serve_forever()


def run_bruteforce_ftp(temp_dir):
    authorizer = DummyAuthorizer()
    user, password = TEST_CREDS[-1]
    authorizer.add_user(user, password, temp_dir, perm="elradfmw")
    handler = FTPHandler
    handler.authorizer = authorizer
    handler.max_login_attempts = 2  # Drop connection on each 2 incorrect attempts
    server = FTPServer(("127.0.0.1", PORT), handler)
    server.serve_forever()


def run_mumble():
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    httpd.serve_forever()


class TestFTPScanner(unittest.TestCase):
    def test_closed_port(self):
        scanner = FTPScanner(timeout=10)
        result = scanner.scan_address('127.0.0.1', 31337, credentials=TEST_CREDS)
        print(result)
        self.assertEqual(result['status'], 'error', "Should be error")
        self.assertTrue("Connection refused" in result['error_type'], "Connection refused")

    def test_mumble(self):
        p = multiprocessing.Process(target=run_mumble)
        p.start()
        sleep(5)
        scanner = FTPScanner(timeout=10)
        result = scanner.scan_address('127.0.0.1', PORT, credentials=TEST_CREDS)
        print(result)
        self.assertEqual(result['status'], 'error', "Should be error")
        self.assertTrue("timed out" in result['error_type'], "Timed out")
        p.terminate()

    def test_anonymous_login(self):
        temp_dir = mkdtemp()
        p = multiprocessing.Process(target=run_anonymous_ftp, args=(temp_dir,))
        p.start()
        sleep(5)
        scanner = FTPScanner(timeout=10)
        result = scanner.scan_address('127.0.0.1', PORT, credentials=TEST_CREDS)
        print(result)
        self.assertEqual(result['anonymous_login'], True, "Should be True")
        p.terminate()
        os.rmdir(temp_dir)

    def test_bruteforce(self):
        temp_dir = mkdtemp()
        p = multiprocessing.Process(target=run_bruteforce_ftp, args=(temp_dir,))
        p.start()
        sleep(5)
        scanner = FTPScanner(timeout=10)
        result = scanner.scan_address('127.0.0.1', PORT, credentials=TEST_CREDS)
        print(result)
        self.assertEqual(result['credentials'], TEST_CREDS[-1], "Should be True")
        p.terminate()
        os.rmdir(temp_dir)


if __name__ == '__main__':
    unittest.main()
