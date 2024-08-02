from emulator import CPU

def check_if_registers(operands):
    firstCheck = operands[0].startswith("r")
    secondCheck = operands[1].startswith("r")
    return firstCheck and secondCheck

def add(cpu, operands):
    if not check_if_registers(operands):
        raise MemoryError(f"Operands {operands} are not registers.\nIf operands should be considered as registers they have to start with 'R', following with the digit from 0 to 3.")
    op0 = int(operands[0][1:])
    op1 = int(operands[1][1:])
    cpu.registers[op0]+=cpu.registers[op1]

def sub(cpu, operands):
    if not check_if_registers(operands):
        raise MemoryError(f"Operands {operands} are not registers.\nIf operands should be considered as registers they have to start with 'R', following with the digit from 0 to 3.")
    op0 = int(operands[0][1:])
    op1 = int(operands[1][1:])
    cpu.registers[op0]-=cpu.registers[op1]

def div(cpu,operands):
    if not check_if_registers(operands):
        raise MemoryError(f"Operands {operands} are not registers.\nIf operands should be considered as registers they have to start with 'R', following with the digit from 0 to 3.")
    op0 = int(operands[0][1:])
    op1 = int(operands[1][1:])
    cpu.registers[op0]//=cpu.registers[op1]

def mul(cpu,operands):
    if not check_if_registers(operands):
        raise MemoryError(f"Operands {operands} are not registers.\nIf operands should be considered as registers they have to start with 'R', following with the digit from 0 to 3.")
    op0 = int(operands[0][1:])
    op1 = int(operands[1][1:])
    cpu.registers[op0]*=cpu.registers[op1]

def bitwise_and(cpu,operands):
    if not check_if_registers(operands):
        raise MemoryError(f"Operands {operands} are not registers.\nIf operands should be considered as registers they have to start with 'R', following with the digit from 0 to 3.")
    op0 = int(operands[0][1:])
    op1 = int(operands[1][1:])
    cpu.registers[op0]&=cpu.registers[op1]

def bitwise_or(cpu,operands):
    if not check_if_registers(operands):
        raise MemoryError(f"Operands {operands} are not registers.\nIf operands should be considered as registers they have to start with 'R', following with the digit from 0 to 3.")
    op0 = int(operands[0][1:])
    op1 = int(operands[1][1:])
    cpu.registers[op0]|=cpu.registers[op1]

def bitwise_xor(cpu,operands):
    if not check_if_registers(operands):
        raise MemoryError(f"Operands {operands} are not registers.\nIf operands should be considered as registers they have to start with 'R', following with the digit from 0 to 3.")
    op0 = int(operands[0][1:])
    op1 = int(operands[1][1:])
    cpu.registers[op0]^=cpu.registers[op1]

def make_accessible(cpu,location):
    location = int(location)
    while location >= cpu.capacity:
        cpu.resize()

def mov(cpu,operands):
    if operands[0].startswith("r"):
        destination = int(operands[0][1:])
        if operands[1].startswith("r"):
            source = int(operands[1][1:])
            cpu.registers[destination] = cpu.registers[source]
            return
        if operands[1].startswith("p"):
            source_register = int(operands[1][2:-1])
            source_value = cpu.memory[cpu.registers[source_register]]
            cpu.registers[destination] = source_value
            return
        if operands[1].startswith("a"):
            source = int(operands[1][1:-1])
            cpu.registers[destination] = cpu.memory[source]
            return
    if operands[1].startswith("r"):
        source = int(operands[1][1:])
        if operands[0].startswith("p"):
            destination_register = int(operands[0][2:-1])
            destination_address = cpu.registers[destination_register]
            make_accessible(cpu,destination_address)
            cpu.memory[destination_address] = cpu.registers[source]
            return
        if operands[0].startswith("a"):
            destination = int(operands[0][1:-1])
            cpu.memory[destination] = cpu.registers[source]
            return

def compare_values(cpu,left_value,right_value):
    cpu.conditional_branching = True
    if left_value == right_value:
        cpu.eFlag = True
        return
    if left_value > right_value:
        cpu.gFlag = True
        return
    if left_value < right_value:
        cpu.lFlag = True
        return

def cmp(cpu, operands):
    if operands[0].startswith("r"):
        left_operand = int(operands[0][1:])
        if operands[1].startswith("r"):
            right_operand = int(operands[1][1:])
            compare_values(cpu,cpu.registers[left_operand],cpu.registers[right_operand])
            #cpu.registers[left_operand] = cpu.registers[right_operand]
            return
        if operands[1].startswith("[r"):
            source_register = int(operands[1][2:-1])
            source_value = cpu.memory[cpu.registers[source_register]]
            compare_values(cpu,cpu.registers[left_operand],source_value)
            #cpu.registers[left_operand] = source_value
            return
        if operands[1].startswith("["):
            source = int(operands[1][1:-1])
            compare_values(cpu,cpu.registers[left_operand],cpu.memory[source])
            #cpu.registers[left_operand] = cpu.memory[source]
            return
        else:
            source = int(operands[1][1:])
            compare_values(cpu,cpu.registers[left_operand],source)
            return
    if operands[1].startswith("r"):
        right_operand = int(operands[1][1:])
        if operands[0].startswith("[r"):
            destination_register = int(operands[0][2:-1])
            destination_address = cpu.registers[destination_register]
            compare_values(cpu,cpu.memory[destination_address],cpu.registers[right_operand])
            #cpu.memory[destination_address] = cpu.registers[right_operand]
            return
        if operands[0].startswith("["):
            destination = int(operands[0][1:-1])
            compare_values(cpu,cpu.memory[destination],cpu.registers[right_operand])
            #cpu.memory[destination] = cpu.registers[right_operand]
            return
        else:
            destination = int(operands[0][1:])
            compare_values(cpu,destination,cpu.registers[right_operand])
            return

def convertable_to_int(string_to_convert):
    try:
        int(string_to_convert)
        return True
    except ValueError:
        return False

def mov_immediate(cpu,operands):
    if not convertable_to_int(operands[1][1:]):
        raise ValueError
    if operands[0].startswith("r"):
        register_index = int(operands[0][1:])
        cpu.registers[register_index] = int(operands[1][1:])
        return
    first_address = operands[0][1:-1]
    make_accessible(cpu,first_address)
    cpu.memory[int(first_address)] = int(operands[1][1:])

def bitwise_not(cpu,operand):
    left_operand = int(operand[1:])
    cpu.registers[left_operand] = ~cpu.registers[left_operand]

def find_instruction(cpu,wanted_instruction):
    helper_counter = 0
    return cpu.fetch_for_instruction(helper_counter,wanted_instruction)

def jmp(cpu,operand):
    if not operand[0].startswith("["):
        wanted_instruction = int(operand[0])
        instruction_position = find_instruction(cpu,wanted_instruction)
        cpu.program_counter = instruction_position
        return
    if operand[0].startswith("[r"):
        register_index = int(operand[0][2:-1])
        instruction_position = find_instruction(cpu,cpu.registers[register_index])
        cpu.program_counter = instruction_position
        return

def reset_all_flags(cpu):
    cpu.eFlag = False
    cpu.gFlag = False
    cpu.lFlag = False

def je(cpu,operand):
    if not cpu.conditional_branching:
        return
    cpu.conditional_branching = False
    if cpu.eFlag:
        reset_all_flags(cpu)
        jmp(cpu,operand)

def jg(cpu,operand):
    if not cpu.conditional_branching:
        return
    cpu.conditional_branching = False
    if cpu.gFlag:
        reset_all_flags(cpu)
        jmp(cpu,operand)

def jl(cpu,operand):
    if not cpu.conditional_branching:
        return
    cpu.conditional_branching = False
    if cpu.lFlag:
        reset_all_flags(cpu)
        jmp(cpu,operand)

def jge(cpu,operand):
    if not cpu.conditional_branching:
        return
    cpu.conditional_branching = False
    if cpu.gFlag or cpu.eFlag:
        reset_all_flags(cpu)
        jmp(cpu,operand)

def jle(cpu,operand):
    if not cpu.conditional_branching:
        return
    cpu.conditional_branching = False
    if cpu.lFlag or cpu.eFlag:
        reset_all_flags(cpu)
        jmp(cpu,operand)

def jne(cpu,operand):
    if not cpu.conditional_branching:
        return
    cpu.conditional_branching = False
    if not cpu.eFlag:
        reset_all_flags(cpu)
        jmp(cpu,operand)

def halt(cpu,operands):
    while True:
        u_input = input("System is in halt state. To continue processing commands, enter character 'c':  ")
        if u_input[0] == 'c':
            break

def ior(cpu,operand):
    if not operand[0].startswith("r"):
        raise ValueError
    register_index = int(operand[0][1:])
    tuple2 = cpu.iow_called()
    if not tuple2[0] == True and not tuple2[1] == register_index:
    #if not boolean,reg_index == True,register_index:
        raise ValueError("invalid command syntax")
    print("IOR Called. Character inside the r" + str(register_index) + " is: '" + chr(cpu.registers[register_index]) +  "'.")
    cpu.iow_flag = False,register_index
    user_input = input("Press 'c' to continue.")   
    while not user_input[0] == 'c':
        user_input = input("Still waiting for that c.")

def iow(cpu,operand):
    if not operand[0].startswith("r"):
        raise ValueError
    register_index = int(operand[0][1:])
    user_input = input("Please enter the character you want to write to the register.\n If you input a string, only the first character will be stored. ")
    char_input = user_input[0]
    cpu.registers[register_index] = ord(char_input)
    cpu.iow_flag = True,register_index


binary_instructions = {
    'ADD':add,
    "DIV":div,
    "SUB":sub,
    "MUL":mul,
    "AND":bitwise_and,
    "OR":bitwise_or,
    "XOR":bitwise_xor,
    "MOV":mov,
    "CMP":cmp
}

unary_instructions = {
    "NOT":bitwise_not,
    "JMP":jmp,
    "JE":je, 
    "JNE":jne,
    "JGE":jge,
    "JL":jl,
    "JLE":jle,
    "JG":jg,
    "IOR":ior,
    "IOW":iow,
    "HALT":halt
} 

immeadiate_instructions = {
    "MOVI" : mov_immediate 
}
