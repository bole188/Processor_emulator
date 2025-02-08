import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from emulator import CPU
from instructions import mov, mov_immediate

class TestDataMovementInstructions(unittest.TestCase):

    def setUp(self):
        self.cpu = CPU()

    def test_mov_register(self):
        self.cpu.registers[1] = 10
        mov(self.cpu, ["r0", "r1"])
        self.assertEqual(self.cpu.registers[0], 10)

    def test_mov_immediate(self):
        mov_immediate(self.cpu, ["r0", "i42"])
        self.assertEqual(self.cpu.registers[0], 42)

if __name__ == '__main__':
    unittest.main()
