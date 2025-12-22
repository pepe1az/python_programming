import unittest

def add(a, b):
    return a + b

class TestMath(unittest.TestCase):
    def test_add_positive(self):
        self.assertEqual(add(2, 3), 5)

    def test_add_negative(self):
        self.assertEqual(add(-1, -3), -4)

    def test_add_zero(self):
        self.assertEqual(add(0, 5), 5)

unittest.main(argv=[''], verbosity=2, exit=False)