import numpy as np
import os
from PageTableEntry import *
from Cache import *
from MultiLevelCache import *

PAGE_SIZE = 4096 
NUM_PAGES = 2**52


class CPU:
    def __init__(self):
        self.registers = np.zeros(4, dtype=np.int64) 
        self.writing_address = 0
        self.program_counter = 0
        self.physical_memory = {}
        self.capacity = 30
        self.memory = np.zeros(self.capacity, np.uint8)
        self.halted = False
        self.opcode_length = 4
        self.operand_length = 9
        self.gFlag = False
        self.lFlag = False
        self.eFlag = False
        self.conditional_branching = False
        self.iow_flag = False, 0
        self.free_frames = [] 

        cache_levels = int(input("Number of cache levels: "))
        levels_config = []

        for level in range(cache_levels):
            cache_type = input(f"Type for cache level {level + 1} (DirectMapped/SetAssociative/FullyAssociative): ")
            cache_size = int(input(f"Size for cache level {level + 1}: "))
            line_size = int(input(f"Line size for cache level {level + 1}: "))

            if cache_type == "SetAssociative":
                num_ways = int(input(f"Associativity (number of ways) for cache level {level + 1}: "))
                replacement_policy = input(f"Replacement policy (LRU/Belady) for cache level {level + 1}: ")
                levels_config.append({
                    "type": cache_type,
                    "size": cache_size,
                    "line_size": line_size,
                    "ways": num_ways,
                    "replacement_policy": replacement_policy
                })
            elif cache_type == "FullyAssociative":
                replacement_policy = input(f"Replacement policy (LRU/Belady) for cache level {level + 1}: ")
                levels_config.append({
                    "type": cache_type,
                    "size": cache_size,
                    "line_size": line_size,
                    "replacement_policy": replacement_policy
                })
            else:
                levels_config.append({
                    "type": cache_type,
                    "size": cache_size,
                    "line_size": line_size
                })

        self.cache = MultiLevelCache(levels_config, self.memory_access_function)

    def memory_access_function(self, address):
        return self.memory_read(address)


    def translate_address(self, virtual_address):
        offsets = [
            (virtual_address >> 12) & 0x1FF, 
            (virtual_address >> 21) & 0x1FF,  
            (virtual_address >> 30) & 0x1FF,  
            (virtual_address >> 39) & 0x1FF,  
        ]
        offset_within_page = virtual_address & 0xFFF

        current_table = root_page_table
        for level in range(3, -1, -1):
            if level == 0:
                if current_table.entries[offsets[level]] is None:
                    frame_number = self.allocate_frame()
                    current_table.entries[offsets[level]] = frame_number
                frame_number = current_table.entries[offsets[level]]
                return frame_number * PAGE_SIZE + offset_within_page
            else:
                if current_table.entries[offsets[level]] is None:
                    current_table.entries[offsets[level]] = PageTableLevel(level)
                current_table = current_table.entries[offsets[level]]

        raise MemoryError("Failed to translate address")

    def allocate_frame(self):
        if self.free_frames:
            frame_number = self.free_frames.pop()
        else:
            frame_number = len(self.physical_memory)
            if frame_number * PAGE_SIZE >= 64 * 1024:
                raise MemoryError("Out of physical memory")

            self.physical_memory[frame_number] = [0] * PAGE_SIZE
        return frame_number

    def free_frame(self, frame_number):
        if frame_number in self.physical_memory:
            self.free_frames.append(frame_number)
            del self.physical_memory[frame_number]

    def reallocate_frame(self, old_frame_number):
        new_frame_number = self.allocate_frame()
        self.physical_memory[new_frame_number] = self.physical_memory[old_frame_number]
        self.free_frame(old_frame_number)
        return new_frame_number

    def write_instructions(self, instructions):
        for instruction in instructions:
            if self.writing_address >= self.capacity:
                self.resize()
            
            parts = instruction.split()
            opcode = parts[0]
            operands = parts[1:]
            opcode_bytes = opcode.encode('utf-8')
            opcode_bytes = opcode_bytes.ljust(4, b'\x00')

            operand_bytes = []

            for operand in operands:
                if operand.startswith("[") and not operand[1] == 'r':
                    op_value = int(operand[1:-1],16)
                    operand_bytes.append('a'.encode('utf-8'))
                    operand_bytes.append(op_value.to_bytes(8,byteorder = 'little'))
                elif operand.startswith("r"):
                    op_value = int(operand[1:],10)
                    operand_bytes.append('r'.encode('utf-8'))
                    operand_bytes.append(op_value.to_bytes(8,byteorder = 'little'))
                    
                elif operand.startswith("[r"):
                    op_value = int(operand[2:-1],10)
                    operand_bytes.append('p'.encode('utf-8'))
                    operand_bytes.append(op_value.to_bytes(8,byteorder = 'little'))
                else:
                    op_value = int(operand)
                    print(f"opvalue is {op_value}")
                    operand_bytes.append('i'.encode('utf-8'))
                    operand_bytes.append(op_value.to_bytes(8,byteorder = 'little'))
            
            print(f"writing operand in bytes: {operand_bytes}")

            self.memory_write(self.writing_address, opcode_bytes)

            self.writing_address += len(opcode_bytes)
            print(f"updated writing address: {self.writing_address}")

            for operand in operand_bytes:
                self.memory_write(self.writing_address, operand)
                self.writing_address += len(operand)
                print(f"updated writing address: {self.writing_address}")

    def check_instruction(self, opcode):
        from instructions import binary_instructions,unary_instructions,immeadiate_instructions
        if opcode in binary_instructions or opcode in immeadiate_instructions:
            return 2
        elif opcode in unary_instructions and not opcode == "HALT":
            return 1
        return 0

    def resize(self):
        new_capacity = 2 * self.capacity
        new_array = np.zeros(new_capacity, dtype=self.memory.dtype)
        new_array[:self.memory.size] = self.memory
        self.memory = new_array
        self.capacity = new_capacity


    def memory_read(self, virtual_address):
        physical_address = self.translate_address(virtual_address)
        frame_number = physical_address // PAGE_SIZE
        offset = physical_address % PAGE_SIZE
        return self.physical_memory[frame_number][offset]

    def memory_write(self, virtual_address, value):
        physical_address = self.translate_address(virtual_address)
        frame_number = physical_address // PAGE_SIZE
        offset = physical_address % PAGE_SIZE
        self.physical_memory[frame_number][offset] = value


    def read_instruction(self, address):
        opcode_bytes = [self.memory_read(address + i) for i in range(self.opcode_length)]
        opcode = ''.join(chr(byte) for byte in opcode_bytes).strip('\x00')
        operand_count = self.check_instruction(opcode)
        operands = []
        offset = self.opcode_length
        for i in range(operand_count):
            operand_bytes = [self.memory_read(address + offset + j) for j in range(self.operand_length)]
            operand = int.from_bytes(operand_bytes, 'little')
            operands.append(operand)
            offset += self.operand_length
        
        return opcode, operands

    def set_opcode_length(self, pc):
        chunk_size = 5
        memory_chunk = np.array([self.memory_read(pc + i) for i in range(chunk_size)], dtype=np.uint8)
        
        check_if_halt = ''.join(chr(code) for code in memory_chunk[:-1])

        if check_if_halt == "HALT":
            return 4

        letters = set(range(ord('A'), ord('Z') + 1))    

        boundary_bytes = np.array([b for b in range(256) if b not in letters], dtype=np.uint8)

        is_boundary = np.isin(memory_chunk, boundary_bytes)
        
        self.opcode_length = np.argmax(is_boundary)

    def fetch_for_instruction(self,helper_counter,wanted_instruction):
        instruction_number = 0
        while wanted_instruction != instruction_number:
            if wanted_instruction == 0:
                break
            self.set_opcode_length(helper_counter)
            opcode_bytes = self.memory[helper_counter:helper_counter + self.opcode_length]
            opcode_bytes = bytes(opcode_bytes)
            opcode = opcode_bytes.decode('utf-8').strip('\x00')
            
            if opcode == '':
                raise ValueError

            operand_count = self.check_instruction(opcode)
            operand_bytes = []
            offset = helper_counter + self.opcode_length
            
            for _ in range(operand_count):
                
                operand_data = self.memory[offset:offset + self.operand_length]

                if len(operand_data) != self.operand_length:
                    raise ValueError(f"Expected {self.operand_length} bytes for operand, got {len(operand_data)} bytes.")

                operand_bytes.append(bytes(operand_data))
                offset += self.operand_length

            helper_counter += self.opcode_length + operand_count * self.operand_length
            
            instruction_number+=1
        
        return helper_counter

    def fetch(self):
        opcode_bytes = self.memory_read(self.program_counter)
        opcode_bytes = bytes(opcode_bytes)
        opcode = opcode_bytes.decode('utf-8').strip('\x00') 
        

        if opcode == '':
            return '', []

        print(f"Fetched instruction:{opcode}")

        operand_count = self.check_instruction(opcode)
        operand_bytes = []
        offset = self.program_counter + self.opcode_length
        for _ in range(operand_count):
            operand_data = [self.memory_read(offset + i) for i in range(2)]
            combined_bytes = b''.join(operand_data)

            if len(combined_bytes) != self.operand_length:
                raise ValueError(f"Expected {self.operand_length} bytes for operand, got {len(operand_data)} bytes.")
            operand_bytes.append(bytes(combined_bytes))
            offset += self.operand_length

        self.program_counter += self.opcode_length + operand_count * self.operand_length

        return opcode, operand_bytes

    def decode(self, opcode, operand_bytes):
        if opcode == "HALT":
            return opcode,[]
        operands = []
        for operand in operand_bytes:
            first_byte = operand[:1]
            first_character = first_byte.decode('utf-8').strip('\x00')
            decoded_integer = int.from_bytes(operand[1:],byteorder = 'little')
            operands.append(first_character + str(decoded_integer))
        print(f"Decoded operands: {operands}")
        return opcode, operands

    def print_register_values(self):
        i = 0
        for register in self.registers:
            print(f"Value of {i}. register: {register}")
            i+=1

    def iow_called(self):
        return self.iow_flag

    def execute(self, opcode, operands):
        from instructions import binary_instructions,unary_instructions,immeadiate_instructions
        if opcode in binary_instructions:
            binary_instructions[opcode](self, operands)
        elif opcode in unary_instructions:
            unary_instructions[opcode](self, operands)
        elif opcode == "HALT":
            self.halted = True
        elif opcode in immeadiate_instructions:
            immeadiate_instructions[opcode](self, operands)
        else:
            print(f"Unknown opcode: {opcode}")
        self.print_register_values()

    def run(self):
        while not self.halted and self.program_counter < self.capacity:
            opcode, operand_bytes = self.fetch()
            if(opcode==''):
                break
            opcode, operands = self.decode(opcode, operand_bytes)
            self.execute(opcode, operands)
        print(f"Program counter: {self.program_counter}, Memory capacity: {self.capacity}")
