import unittest
from emulator import CPU


class TestCPUInstructions(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()

    def test_write_and_read_instruction(self):
        # Initialize a CPU
        cpu = self.cpu
        
        # Define an instruction and its operands
        
        opcode = 'ADD'
        operands = [0, 1]  # Move value from register 1 to register 0

        # Write the instruction into memory
        #cpu.write_instruction(0,opcode, operands)
        #cpu.write_instruction(21, 'SUB', [0,1])
        instructions = []
        with open('example.txt', 'r') as file:
            line = file.readline()
            while line:
                instructions.append(line)
                line = file.readline()

        cpu.write_instructions(instructions)
        #Read the instruction from memory
        #fetched_opcode, fetched_operands = cpu.read_instruction(address)

        cpu.run()

        print(cpu.registers[0])
        self.assertEqual(fetched_opcode, opcode, f"Expected {opcode}, got {fetched_opcode}")
        self.assertEqual(fetched_operands, operands, f"Expected {operands}, got {fetched_operands}")


if __name__ == "__main__":
    unittest.main()
