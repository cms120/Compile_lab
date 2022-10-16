import unittest

from lexical.state import State


class TestState(unittest.TestCase):
    def test_reset_flag(self):
        State.reset_flag()
        self.assertEqual(State.get_flag(), 0)

    def test_flag_plus(self):
        State.reset_flag()
        for i in range(100):
            State.flag_plus()
        self.assertEqual(State.get_flag(), 100)
        State.reset_flag()
        self.assertEqual(State.get_flag(), 0)


if __name__ == '__main__':
    unittest.main()
