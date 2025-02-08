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

### Cache Management and Memory Paging Files

The processor emulator repository includes several files dedicated to simulating cache behavior and managing virtual memory. Below is an overview of these key files:

#### `cache.py`

This file defines the foundational `Cache` class which is used to simulate cache memory operations. It includes functionalities such as:

- **Cache Initialization:**  
  Setting up cache parameters such as the cache size, block size, and (if applicable) the associativity.

- **Cache Operations:**  
  Methods for reading and writing data to the cache, handling data placement, and managing replacement policies.

- **Hit/Miss Tracking:**  
  Basic logic to track cache hits and misses during memory accesses, which is crucial for evaluating cache performance.

The `Cache` class is designed as a base class that can be extended to implement more specialized caching strategies.

#### `multiLevelCache.py`

This file implements a multi-level cache system to simulate the behavior of modern processors that use a hierarchical cache architecture. Key features include:

- **Multiple Cache Levels:**  
  Simulation of more than one cache level (e.g., L1 and L2) to mimic realistic memory hierarchies. The design typically allows for a faster, smaller cache at level 1 and a larger, slightly slower cache at level 2.

- **Latency and Access Differentiation:**  
  Modeling the differences in access times between the various cache levels. This helps in analyzing how the hierarchical design can impact overall system performance.

- **Inter-cache Communication:**  
  Logic to handle cache misses in a higher-level cache by checking lower-level caches, thereby improving data retrieval efficiency.

This file builds upon the basic caching operations provided by `cache.py` and extends them to support a multi-level structure.

#### `PageTableEntry.py`

This file defines the `PageTableEntry` class, which is essential for simulating virtual memory management using a paging mechanism. The class typically provides:

- **Virtual-to-Physical Mapping:**  
  Attributes that store the virtual page number and its corresponding physical frame number. This mapping is crucial for translating virtual addresses to physical memory addresses.

- **Validity and Status Flags:**  
  A valid bit to indicate whether the page is currently in physical memory, as well as potential additional flags (e.g., dirty bit, access permissions) that help manage and optimize memory usage.

- **Memory Management Support:**  
  The structure supports advanced memory management features such as page replacement strategies and permission checks, which are integral parts of an operating system’s virtual memory system.

This class allows the emulator to model the behavior of an operating system’s memory management unit (MMU), making it possible to simulate paging and other related memory operations.


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
