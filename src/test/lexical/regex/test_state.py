import unittest

from lexical.regex.state import State


class StateTest(unittest.TestCase):
    def test_reset_flag(self):
        State.reset()
        self.assertEqual(State.get_flag(), 0)

    def test_flag_plus(self):
        State.reset()
        for i in range(100):
            State.flag_plus()
        self.assertEqual(State.get_flag(), 100)
        State.reset()
        self.assertEqual(State.get_flag(), 0)


if __name__ == '__main__':
    unittest.main()
