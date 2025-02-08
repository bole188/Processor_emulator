import numpy as np
import os 
from emulator import CPU 
from instructions import binary_instructions, unary_instructions, immeadiate_instructions


def main():
    cpu = CPU()
    
    try:
        with open('example.txt', 'r') as file:
            instructions = file.readlines()
        
        instructions = [instr.strip() for instr in instructions if instr.strip()]

        cpu.write_instructions(instructions)

        cpu.run()
        print(cpu.cache.cache_stats())

    except FileNotFoundError:
        print(f"File example.txt not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
