import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from emulator import CPU
from instructions import jmp, je, jne, jg, jl, jge, jle, cmp

class TestJumpInstructions(unittest.TestCase):

    def setUp(self):
        self.cpu = CPU()

    def test_jmp(self):
        jmp(self.cpu, ["5"])
        self.assertEqual(self.cpu.program_counter, 5)

    def test_je(self):
        self.cpu.eFlag = True
        self.cpu.program_counter = 0
        je(self.cpu, ["10"])
        self.assertEqual(self.cpu.program_counter, 10)

    def test_jne(self):
        self.cpu.eFlag = False
        self.cpu.program_counter = 0
        jne(self.cpu, ["15"])
        self.assertEqual(self.cpu.program_counter, 15)

    def test_jg(self):
        self.cpu.gFlag = True
        self.cpu.program_counter = 0
        jg(self.cpu, ["20"])
        self.assertEqual(self.cpu.program_counter, 20)

    def test_jl(self):
        self.cpu.lFlag = True
        self.cpu.program_counter = 0
        jl(self.cpu, ["25"])
        self.assertEqual(self.cpu.program_counter, 25)

    def test_jge(self):
        self.cpu.gFlag = True
        self.cpu.program_counter = 0
        jge(self.cpu, ["30"])
        self.assertEqual(self.cpu.program_counter, 30)
        self.cpu.gFlag = False
        self.cpu.eFlag = True
        jge(self.cpu, ["35"])
        self.assertEqual(self.cpu.program_counter, 35)

    def test_jle(self):
        self.cpu.lFlag = True
        self.cpu.program_counter = 0
        jle(self.cpu, ["40"])
        self.assertEqual(self.cpu.program_counter, 40)
        self.cpu.lFlag = False
        self.cpu.eFlag = True
        jle(self.cpu, ["45"])
        self.assertEqual(self.cpu.program_counter, 45)

if __name__ == '__main__':
    unittest.main()
