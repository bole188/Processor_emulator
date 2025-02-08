import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



from instructions import add, sub, div, mul
from emulator import CPU

class TestArithmeticInstructions(unittest.TestCase):
    
    def setUp(self):
        self.cpu = CPU()

    def test_add(self):
        self.cpu.registers[0] = 5
        self.cpu.registers[1] = 10
        add(self.cpu, ["r0", "r1"])
        self.assertEqual(self.cpu.registers[0], 15)

    def test_sub(self):
        self.cpu.registers[0] = 15
        self.cpu.registers[1] = 5
        sub(self.cpu, ["r0", "r1"])
        self.assertEqual(self.cpu.registers[0], 10)

    def test_div(self):
        self.cpu.registers[0] = 20
        self.cpu.registers[1] = 5
        div(self.cpu, ["r0", "r1"])
        self.assertEqual(self.cpu.registers[0], 4)

    def test_mul(self):
        self.cpu.registers[0] = 3
        self.cpu.registers[1] = 4
        mul(self.cpu, ["r0", "r1"])
        self.assertEqual(self.cpu.registers[0], 12)

if __name__ == '__main__':
    unittest.main()
