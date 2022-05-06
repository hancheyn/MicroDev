import unittest
import time
import Controller


# ###### Debugging Test Example ################# #
class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


# ###### Debugging Test Code for Serial ######### #
class SerialTests(unittest.TestCase):
    # Tests that serial communication is established and subject board can reply
    def test_basic(self):
        controller = Controller
        s = bytearray(3)
        s[0] = 0x01
        s[1] = 0x10
        s[2] = 0x03

        # s[3] = 0x0a
        # s[4] = 0x0D
        ser = controller.open_serial()
        time.sleep(2)
        controller.subject_write(str_write=s, ser=ser)
        time.sleep(2)
        test_bytes = controller.subject_read(ser_=ser)
        controller.close_serial(ser)

        print(test_bytes)
        int_val = int.from_bytes(test_bytes, "big")
        print(int_val)
        time.sleep(2)
        # Pin ID Echos Back
        self.assertEqual(test_bytes[0], s[0])

    # Tests Encoding CRC for data packet
    def test_crc_encode(self):
        controller = Controller

    # Tests decoding CRC data packet to pin, result, and test id
    # E.G. 1 = pin, 2 = test, 3 = results
    def test_crc_decode(self):
        controller = Controller
        s = bytearray(3)
        s[0] = 0x01
        s[1] = 0x10
        s[2] = 0x03
        output = controller.crc_decode(s, 1)
        print(output)


# ###### Debugging Test Code for CLI ########## #
# CLI Functionality Tests
class CLITests(unittest.TestCase):
    # Test that Uno ID Info is Obtained
    def test_board_list_Uno(self):
        controller = Controller
        board_out = controller.board_list()
        print(board_out)
        # Test of Output (? Output 2 for Uno)
        self.assertEqual(board_out, board_out)

    # Test that STM ID Info is Obtained
    def test_board_list_STM(self):
        controller = Controller
        board_out = controller.board_list()
        print(board_out)
        # Test of Output (? Output 1 for STM)
        self.assertEqual(board_out, board_out)

    # Test that No Board Info is Obtained
    def test_board_list_None(self):
        controller = Controller
        board_out = controller.board_list()
        print(board_out)
        # Test of Output (? Output 0 for no board)
        self.assertEqual(board_out, board_out)

    # Flash Subject Board Test



if __name__ == '__main__':
    unittest.main()
