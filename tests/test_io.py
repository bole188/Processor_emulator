import unittest
from unittest.mock import patch
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from emulator import CPU
from instructions import ior, iow

class TestIOInstructions(unittest.TestCase):

    def setUp(self):
        self.cpu = CPU()

    @patch('builtins.input', return_value='a')
    def test_iow(self, mock_input):
        iow(self.cpu, ["r0"])
        self.assertEqual(self.cpu.registers[0], ord('a'))

    @patch('builtins.input', return_value='c')
    def test_ior(self, mock_input):
        self.cpu.registers[0] = ord('x')
        self.cpu.iow_flag = (True, 0)
        ior(self.cpu, ["r0"])  # Should print character 'x' and wait for 'c' to continue
        self.assertFalse(self.cpu.iow_flag[0])

if __name__ == '__main__':
    unittest.main()
