import unittest
import time
import Controller as controller
import Model as model


# ###### Debugging Test Example ################# #
class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here



if __name__ == '__main__':
    unittest.main()

# Testing Subject Board Tests
board = model.board_list()
controller.subject_test(1, 23, 6, 3, board)
