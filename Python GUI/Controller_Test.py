import unittest
import time
import Controller

# ###### Debugging Test Example ######### #
class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


# ###### Debugging Test Code for Serial ######### #
class Serial_Tests(unittest.TestCase):
    def test_basic(self):
        controller = Controller
        s = bytearray(3)
        s[0] = 0x01
        s[1] = 0x10
        s[2] = 0x03
        controller.subject_write(str_write=s)
        time.sleep(2)
        test_bytes = controller.subject_read()
        print(test_bytes)
        int_val = int.from_bytes(test_bytes, "big")
        print(int_val)
        time.sleep(2)
        #Pin ID Echos Back
        self.assertEqual(test_bytes[0], s[0])







if __name__ == '__main__':
    unittest.main()


