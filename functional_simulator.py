"""
Author: Rutuja Muttha
Computer Architecture_ECE586_Spring2023
Functional Simulator
MIPS-lite

"""


import os

#Define opcode values as per defined in Project_specs

# Arithmetic Instruction
ADD  = 0b000000
SUB  = 0b000010
MUL  = 0b000100
ADDI = 0b000001
SUBI = 0b000011
MULI = 0b000101

# Logical Instruction
OR   = 0b000110
AND  = 0b001000
XOR  = 0b001010
ORI  = 0b000111
ANDI = 0b001001
XORI = 0b001011

# Memory Access Instruction
LDW  = 0b001100                     # Load the contents of the memory location 
STW  = 0b001101                     # Store the contents of the memory location

# Control Flow Instruction 
BZ   = 0b001110                     # Branch
BEQ  = 0b001111                     # Branch if equal
JR   = 0b010000                     # Jump to new PC
HALT = 0b010001                     # Stop executing the program

# Instruction Format
R_TYPE = [ADD,SUB,MUL,OR,AND,XOR]
I_TYPE = [ADDI,SUBI,MULI,ORI,ANDI,XORI]
IJ_TYPE = [LDW,STW,BZ,BEQ,JR,HALT]

# Initialize variables and data structures

trace = []                          # trace of instruction
PC = 0                              # Program Counter
idx = 0                             # Current index in trace
current_instruction = 0             # Current Instruction
fetch_instruction = []              # Fetched Instruction
opcode = 0                          # Opcode of the current instruction
output = 0                          # Output value

reg = {}                            # Register dictionary to store register values
temporary_reg = [0] * 32            # Temporary register file
RS = 0                              # Source Register 1
RD = 0                              # Destination Register
RT = 0                              # Source Register 2
Imm = 0                             # Immediate value
src1 = 0                            # Value of source register 1
src2 = 0                            # Value of source register 2
destination = 0                     # Value of destination register

no_of_arithmetic = 0                # Number of arithmetic instructions executed  
no_of_logic = 0                     # Number of logic instructions executed
no_of_memory = 0                    # Number of memory access instructions executed
no_of_control = 0                   # Number of control flow instructions executed
total_instruction = 0               # Total number of instructions 

memory_dictionary = {}              # Memory dictionary to store memory contents
mem_addr = 0                        # Memory Address
temp_addr = 0                       # Temporary memory address
branch_flag = []                    # Branch flags
penalty = 0                         # Penalty cycle
halt = 0                            # Flags to indicate halt instruction

"""
    Function name: trace_reader

    Read the trace file and populate the trace list.

    Parameters:
    - path (str): Path to the directory containing the trace file.
    - file_name (str): Name of the trace file.

    Returns:
    - trace (list): List containing the trace of instructions.
    """

def trace_reader(path,file_name):

    global trace
    trace_file = open(os.path.join(path,file_name),"r")
    for read_line in trace_file:
        read_line.strip()
        read_val = int(read_line,16)
        trace.append(read_val)
    return trace

"""
    Function name: two_complement
    Convert a value to its two's complement representation.
    Parameters:
    - value (int): Value to be converted.
    - bit_size (int): Size of the bit representation.
    Returns:
    - value (int): Two's complement representation of the value.
    """

def two_complement(value,bit_size):
    if((value & (1 << (bit_size - 1))) != 0):
        value = value - (1 << bit_size)
        return value
    else:
        return value
    
"""
Function name: instruction_fetch
    Fetch the next instruction from the trace.
    Parameters:
    - trace (list): List containing the trace of instructions.
    Returns:
    - current_instruction (int): Current instruction fetched from the trace.
    """

def instruction_fetch(trace):
    global PC,idx,current_instruction,fetch_instruction,halt
    idx = int(PC/4)
    current_instruction = trace[idx]
    fetch_instruction.append(current_instruction)
    if(halt != 1):
        PC += 4
    else:
        return
    return current_instruction

""" 
    Function name: instruction_decode
    Decode the current instruction and extract relevant fields.

    Parameters:
    - current_instruction (int): Current instruction to be decoded.
    Returns:
    - opcode (int): Opcode of the current instruction.
    """

def instruction_decode(current_instruction):
    global opcode,RS,RD,RT,Imm,src1,src2,destination,R_TYPE,I_TYPE
    opcode = (current_instruction >> 26) & 63
    if(opcode in R_TYPE):
        RS = (current_instruction >> 21) & 31
        RT = (current_instruction >> 16) & 31
        RD = (current_instruction >> 11) & 31
        src1 = temporary_reg[RS]
        src2 = temporary_reg[RT]
    elif(opcode in I_TYPE or opcode in IJ_TYPE):
        RS = (current_instruction >> 21) & 31
        RT = (current_instruction >> 16) & 31
        Imm = current_instruction & 65535     
        src1 = temporary_reg[RS]
        destination = temporary_reg[RT]
    return opcode

"""
    Function name: instruction_execute
    Execute the instruction based on its opcode.
    Parameters:
    - opcode (int): Opcode of the current instruction.
    Returns:
    - output (int): Output value produced by the instruction.
    """

def instruction_execute(opcode):
    global PC,RS,RD,RT,Imm,src1,src2,destination
    global no_of_arithmetic,no_of_logic,no_of_memory,no_of_control
    global temp_addr,mem_addr,output
    global branch_flag,halt,penalty
    if(opcode == ADD):
        no_of_arithmetic += 1
        output = src1 + src2
    elif(opcode == ADDI):
        no_of_arithmetic += 1
        output = src1 + two_complement(Imm,16)
    elif(opcode == SUB):
        no_of_arithmetic += 1
        output = src1 - src2
    elif(opcode == SUBI):
        no_of_arithmetic += 1
        output = src1 - two_complement(Imm,16)
    elif(opcode == MUL):
        no_of_arithmetic += 1
        output = src1 * src2
    elif(opcode == MULI):
        no_of_arithmetic += 1
        output = src1 * two_complement(Imm,16)
    elif(opcode == OR):
        no_of_logic += 1
        output = src1 | src2
    elif(opcode == ORI):
        no_of_logic += 1
        output = src1 | Imm
    elif(opcode == AND):
        no_of_logic += 1
        output = src1 & src2
    elif(opcode == ANDI):
        no_of_logic += 1
        output = src1 & Imm
    elif(opcode == XOR):
        no_of_logic += 1
        output = src1 ^ src2
    elif(opcode == XORI):
        no_of_logic += 1
        output = src1 ^ Imm
    elif(opcode == LDW or opcode == STW):
        no_of_memory += 1
        temp_addr = src1 + two_complement(Imm,16)
        mem_addr = int(temp_addr/4)
    elif(opcode == BZ):
        no_of_control += 1
        if(src1 == 0):
            PC = PC - 4
            PC = (PC + (4 * (two_complement(Imm,16))))
            penalty += 2
            branch_flag.append(opcode)
    elif(opcode == BEQ):
        no_of_control += 1
        if(src1 == destination):
            PC = PC - 4
            PC = (PC + (4 * (two_complement(Imm,16))))
            penalty += 2
            branch_flag.append(opcode)
    elif(opcode == JR):
        no_of_control += 1
        PC = src1
        penalty += 2
        branch_flag.append(opcode)
    elif(opcode == HALT):
        no_of_control += 1
        halt = 1
        return
    return output

"""
    Function name: memory_access
    Access memory based on the opcode of the instruction.
    Parameters:
    - trace (list): List containing the trace of instructions.
    """

def memory_access(trace):
    global opcode,memory_dictionary,temporary_reg,mem_addr,output,RT
    if(opcode == LDW):
        output = two_complement(trace[mem_addr],32)
    elif(opcode == STW):
        trace[mem_addr] = temporary_reg[RT]
        memory_dictionary[4 * mem_addr] = trace[mem_addr]

"""
    Function name: write_back
    Write back the output value to the appropriate register.
    Parameters:
    - output (int): Output value produced by the instruction.
    """        

def write_back(output):
    global opcode,temporary_reg,RD,RT
    if(opcode in R_TYPE):
        temporary_reg[RD] = output
        reg[RD] = temporary_reg[RD]
    elif(opcode in I_TYPE or opcode == LDW):
        temporary_reg[RT] = output
        reg[RT] = temporary_reg[RT]

"""
    Function name: show()
    Show the final simulation results.
    """ 
def show():
    global total_instruction,no_of_arithmetic,no_of_logic,no_of_memory,no_of_control,PC,reg,memory_dictionary
    print("\n------------------------------------------------------------------")
    print("MIPS-Lite: Functional Simulator")
    print("\n------------------------------------------------------------------")
    print(r" Total number of instructions            = ",total_instruction)
    print(r" Number of Arithmetic instructions       = ",no_of_arithmetic)
    print(r" Number of Logical instructions          = ",no_of_logic)
    print(r" Number of Memory Acess instructions     = ",no_of_memory)
    print(r" Number of Control Transfer instructions = ",no_of_control)
    print(r" PC: ",PC)  
    for i,j in reg.items():
        print(r" R",i,": ",j)
    for i,j in memory_dictionary.items():
        print(r" Memory : Address: ",i,", Values: ",j)
    print("------------------------------------------------------------------\n")

"""
    Function name: main
    Main function to execute the simulator.
    """

def main():
    global current_instruction,opcode,output,halt
    global no_of_arithmetic,no_of_logic,no_of_memory,no_of_control,total_instruction
    read_inputs = trace_reader(r'C:\Users\saksh\OneDrive\Desktop\Spring_2022\ECE_586\Project','final_proj_trace.txt')
    while(halt != 1):
        current_instruction = instruction_fetch(read_inputs)
        opcode = instruction_decode(current_instruction)
        output = instruction_execute(opcode)
        memory_access(read_inputs)
        write_back(output)
    total_instruction = no_of_arithmetic + no_of_logic + no_of_memory + no_of_control
    show()

# Execute the main function
main()