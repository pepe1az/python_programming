import unittest
import threading
import http.client
import socket
import time

from http.server import HTTPServer
from myapp.myapp import MyHandler


def get_free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    host, port = s.getsockname()
    s.close()
    return port


class ServerThread(threading.Thread):
    def __init__(self, port):
        super().__init__(daemon=True)
        self.httpd = HTTPServer(("127.0.0.1", port), MyHandler)

    def run(self):
        self.httpd.serve_forever()

    def stop(self):
        self.httpd.shutdown()
        self.httpd.server_close()


class TestController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = get_free_port()
        cls.server = ServerThread(cls.port)
        cls.server.start()
        time.sleep(0.2)

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def fetch(self, path):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=3)
        conn.request("GET", path)
        resp = conn.getresponse()
        body = resp.read().decode("utf-8", errors="ignore")
        conn.close()
        return resp.status, body

    def test_index(self):
        status, body = self.fetch("/")
        self.assertEqual(status, 200)
        self.assertIn("CurrenciesListApp", body)

    def test_users(self):
        status, body = self.fetch("/users")
        self.assertEqual(status, 200)
        self.assertIn("Пользователи", body)

    def test_user_query(self):
        status, body = self.fetch("/user?id=1")
        self.assertEqual(status, 200)
        self.assertIn("Пользователь", body)

    def test_currencies(self):
        status, body = self.fetch("/currencies")
        # может быть 200 или 502 если нет сети — тест не должен падать
        self.assertIn(status, (200, 502))
