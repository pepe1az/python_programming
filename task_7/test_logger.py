import unittest
import io

from logger_decorator import logger


class TestLoggerWithStringIO(unittest.TestCase):
    def setUp(self):
        self.stream = io.StringIO()

    def test_logs_success(self):
        @logger(handle=self.stream)
        def test_function(x):
            return x * 2

        self.assertEqual(test_function(21), 42)
        logs = self.stream.getvalue()

        self.assertIn("INFO", logs)
        self.assertIn("CALL test_function", logs)
        self.assertIn("args=(21,)", logs)
        self.assertIn("OK   test_function", logs)
        self.assertIn("result=42", logs)

    def test_logs_error_and_reraises(self):
        @logger(handle=self.stream)
        def boom():
            raise RuntimeError("kaboom")

        with self.assertRaises(RuntimeError):
            boom()

        logs = self.stream.getvalue()
        self.assertRegex(logs, "ERROR")
        self.assertIn("RuntimeError", logs)


class TestStreamWriteExample(unittest.TestCase):
    def setUp(self):
        self.stream = io.StringIO()

        @logger(handle=self.stream)
        def wrapped():
            from currencies import get_currencies
            return get_currencies(['USD'], url="https://invalid.invalid", timeout=1)

        self.wrapped = wrapped

    def test_logging_error(self):
        with self.assertRaises(ConnectionError):
            self.wrapped()

        logs = self.stream.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("ConnectionError", logs)
