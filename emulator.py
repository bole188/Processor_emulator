import numpy as np
import os

class CPU:
    def __init__(self):
        self.registers = np.zeros(4,dtype = np.int64)  # 4 registra od 64 bita
        self.writing_address = 0
        self.program_counter = 0
        self.capacity = 30 # in bits
        self.memory = np.zeros(self.capacity, np.uint8)
        self.halted = False
        #self.opcode_length = int(os.getenv('OPCODE_LENGTH', 4)) 
        self.opcode_length = 4
        self.operand_length = 9
        self.gFlag = False
        self.lFlag = False
        self.eFlag = False
        self.conditional_branching = False
        self.iow_flag = False,0

    def write_instructions(self, instructions):
        for instruction in instructions:
            if self.writing_address >= self.capacity:
                self.resize()
            
            # Assuming each instruction is a string "OPCODE OPERAND"
            parts = instruction.split()
            opcode = parts[0]
            operands = parts[1:]
            print(f"writing: {operands}")
            opcode_bytes = opcode.encode('utf-8')
            opcode_bytes = opcode_bytes.ljust(4, b'\x00')

            operand_bytes = []

            #operand_bytes = [int(operand).to_bytes(self.operand_length, 'little') for operand in operands]
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

            #operand_bytes = [operand.encode('utf-8') for operand in operands]
            
            print(f"writing operand in bytes: {operand_bytes}")

            self.memory_write(self.writing_address, opcode_bytes)

            self.writing_address += len(opcode_bytes)
            print(f"updated writing address: {self.writing_address}")

            for operand in operand_bytes:
                self.memory_write(self.writing_address, operand)
                self.writing_address += len(operand)
                #self.writing_address += self.operand_length
                print(f"updated writing address: {self.writing_address}")

    def check_instruction(self, opcode):
        from instructions import binary_instructions,unary_instructions,immeadiate_instructions
        if opcode in binary_instructions or opcode in immeadiate_instructions:
            return 2
        elif opcode in unary_instructions and not opcode == "HALT":
            return 1
        return 0

    def resize(self):
        # Increase capacity
        new_capacity = 2 * self.capacity
        # Create a new array with the increased capacity
        new_array = np.zeros(new_capacity, dtype=self.memory.dtype)
        # Copy old elements to the new array
        new_array[:self.memory.size] = self.memory
        # Update array and capacity
        self.memory = new_array
        self.capacity = new_capacity

    def memory_read(self, address):
        if address >= self.capacity:
            raise MemoryError("Impossible to read from this address")
        return self.memory[address]

    def memory_write(self, address, value):
        if address >= self.capacity:
            self.resize()
        
        # Handle single byte (int)
        if isinstance(value, int):
            if not (0 <= value <= 255):
                raise ValueError("Single byte value must be between 0 and 255.")
            self.memory[address] = value
        
        # Handle bytes object
        elif isinstance(value, bytes):
            # Ensure enough capacity to write the bytes
            if address + self.operand_length > self.capacity:
                self.resize()
            # Write the bytes to memory
            converted_value = np.frombuffer(value, dtype=np.uint8)

            # Create a zero-filled array of length 8
            result = np.zeros(self.operand_length, dtype=np.uint8)

            # Copy the converted value into the zero-filled array
            result[:len(converted_value)] = converted_value

            # Write the result array into the memory
            self.memory[address:address + self.operand_length] = result
            #self.memory[address:address + len(value)] = np.frombuffer(value, dtype=np.uint8)

    def read_instruction(self, address):
        # Read the opcode bytes
        opcode_bytes = [self.memory_read(address + i) for i in range(self.opcode_length)]
        opcode = ''.join(chr(byte) for byte in opcode_bytes).strip('\x00')

        # Determine the number of operands based on the opcode
        operand_count = self.check_instruction(opcode)
        operands = []
        # Read the operands
        offset = self.opcode_length
        for i in range(operand_count):
            operand_bytes = [self.memory_read(address + offset + j) for j in range(self.operand_length)]
            operand = int.from_bytes(operand_bytes, 'little')
            operands.append(operand)
            offset += self.operand_length
        
        return opcode, operands

    def set_opcode_length(self, pc):
        # Read a chunk of memory into a NumPy array
        chunk_size = 5
        memory_chunk = np.array([self.memory_read(pc + i) for i in range(chunk_size)], dtype=np.uint8)
        
        check_if_halt = ''.join(chr(code) for code in memory_chunk[:-1])

        if check_if_halt == "HALT":
            return 4

        print(f"Memory chunk: {memory_chunk}")
        # Define boundary bytes (ASCII codes for space and digits)
        letters = set(range(ord('A'), ord('Z') + 1))    

        boundary_bytes = np.array([b for b in range(256) if b not in letters], dtype=np.uint8)

        #boundary_bytes = np.array([ord(' ')] + list(range(1,10)) + [0], dtype=np.uint8)

        #print(f"boundary_bytes: {boundary_bytes}")            

        # Find indices where the memory_chunk contains boundary bytes
        is_boundary = np.isin(memory_chunk, boundary_bytes)
        
        print(f"Is boundary: {is_boundary}")
        # Get the index of the first boundary byte
        self.opcode_length = np.argmax(is_boundary)

    def fetch_for_instruction(self,helper_counter,wanted_instruction):
        instruction_number = 0
        while wanted_instruction != instruction_number:
            if wanted_instruction == 0:
                break
            self.set_opcode_length(helper_counter)
            #print(f"Opcode length: {self.opcode_length}")
            # Fetch opcode bytes from memory
            opcode_bytes = self.memory[helper_counter:helper_counter + self.opcode_length]
            # Convert bytes to string and remove any null characters
            opcode_bytes = bytes(opcode_bytes)  # Convert numpy array to bytes
            opcode = opcode_bytes.decode('utf-8').strip('\x00')
            
            if opcode == '':
                raise ValueError

            #print(f"Fetched instruction:{opcode}")
            operand_count = self.check_instruction(opcode)
            operand_bytes = []
            offset = helper_counter + self.opcode_length
            # Fetch operand bytes from memory
            for _ in range(operand_count):
                # Ensure the slice covers the correct range for the operand
                operand_data = self.memory[offset:offset + self.operand_length]

                if len(operand_data) != self.operand_length:
                    raise ValueError(f"Expected {self.operand_length} bytes for operand, got {len(operand_data)} bytes.")

                operand_bytes.append(bytes(operand_data))
                offset += self.operand_length

            helper_counter += self.opcode_length + operand_count * self.operand_length
            
            instruction_number+=1
        
        return helper_counter

    def fetch(self):
        #self.set_opcode_length(self.program_counter)
        print(f"Opcode length: {self.opcode_length}")
        # Fetch opcode bytes from memory
        opcode_bytes = self.memory[self.program_counter:self.program_counter + self.opcode_length]
        # Convert bytes to string and remove any null characters
        opcode_bytes = bytes(opcode_bytes)  # Convert numpy array to bytes
        opcode = opcode_bytes.decode('utf-8').strip('\x00')
        
        if opcode == '':
            return '', []

        print(f"Fetched instruction:{opcode}")

        # Determine the number of operands based on the opcode
        operand_count = self.check_instruction(opcode)
        operand_bytes = []
        print(f"operand count: {operand_count}")
        offset = self.program_counter + self.opcode_length
        # Fetch operand bytes from memory
        for _ in range(operand_count):
            # Ensure the slice covers the correct range for the operand
            operand_data = self.memory[offset:offset +self.operand_length]
            print(f"Operand data (raw): {operand_data}")

            if len(operand_data) != self.operand_length:
                raise ValueError(f"Expected {self.operand_length} bytes for operand, got {len(operand_data)} bytes.")
            operand_bytes.append(bytes(operand_data))
            offset += self.operand_length

        self.program_counter += self.opcode_length + operand_count * self.operand_length

        return opcode, operand_bytes

    def decode(self, opcode, operand_bytes):
        # Convert each operand's bytes to an integer
        if opcode == "HALT":
            return opcode,[]
        print(f"Operand bytes: {operand_bytes}")
        #operands = [int.from_bytes(operand, 'little') for operand in operand_bytes]
        operands = []
        print(len(operand_bytes))
        for operand in operand_bytes:
            first_byte = operand[:1]
            first_character = first_byte.decode('utf-8').strip('\x00')
            decoded_integer = int.from_bytes(operand[1:],byteorder = 'little')
            operands.append(first_character + str(decoded_integer))
            print(first_character + str(decoded_integer))
        #operands = [operand.decode('utf-8').strip('\x00') for operand in operand_bytes]
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
