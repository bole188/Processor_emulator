# Processor Emulator

A simple Python-based processor emulator that simulates a basic CPU with a custom instruction set. This project was built as an educational tool to help understand how a processor might fetch, decode, and execute instructions.

## Overview

The emulator is composed of four main files:

- **`emulator.py`**  
  Contains the core `ProcessorEmulator` class. This class is responsible for:
  - Initializing the CPU’s registers and memory.
  - Loading a program (a sequence of instructions) into memory.
  - Executing instructions step-by-step.
  - Managing the processor’s state such as the program counter and flags.

- **`instructions.py`**  
  Defines the instruction set for the emulator. This file includes:
  - A mapping between opcode names and the functions that implement them.
  - The implementation of individual operations (e.g., arithmetic operations, data movement, and control flow instructions).
  - Utility functions to help decode and execute instructions.

- **`main.py`**  
  Acts as the entry point for the emulator application. It:
  - Instantiates the `ProcessorEmulator`.
  - Loads a sample or user-specified program.
  - Starts the execution loop, allowing you to see the emulator in action.
  - May include command-line argument parsing to customize runtime behavior.

- **`test.py`**  
  Provides a suite of tests to verify that the emulator works as expected. The tests cover:
  - The proper execution of each instruction.
  - Correct updating of registers and memory.
  - Edge cases such as overflow, branching, and error handling.

## Features

- **Instruction Simulation**  
  Simulate a variety of processor instructions such as arithmetic operations, data movement, and branching.

- **Modular Design**  
  The separation of the emulator core and the instruction definitions makes it easy to extend or modify the instruction set.

- **Testing Framework**  
  Built-in tests ensure that changes to the code do not break the core functionality, which is ideal for learning and further development.

## Getting Started

### Prerequisites

- Python 3.6 or higher is recommended.
- Basic knowledge of command-line usage.
