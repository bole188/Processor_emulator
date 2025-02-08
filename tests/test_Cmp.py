import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from emulator import CPU
from instructions import cmp

class TestComparisonInstructions(unittest.TestCase):

    def setUp(self):
        self.cpu = CPU()

    def test_cmp(self):
        self.cpu.registers[0] = 20
        self.cpu.registers[1] = 20
        cmp(self.cpu, ["r0", "r1"])
        self.assertTrue(self.cpu.eFlag)  # Check equality flag

        self.cpu.registers[1] = 10
        cmp(self.cpu, ["r0", "r1"])
        self.assertTrue(self.cpu.gFlag)  # Check greater-than flag

        self.cpu.registers[1] = 30
        cmp(self.cpu, ["r0", "r1"])
        self.assertTrue(self.cpu.lFlag)  # Check less-than flag

if __name__ == '__main__':
    unittest.main()
