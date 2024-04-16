
# MIPS-lite Functional and Timing Simulators

## 1. Project Overview
This repository contains the implementation and analysis of various simulation models for MIPS-lite architecture. It includes functional simulators without forwarding, with forwarding, and a detailed study of branch predictors. These tools are developed to enhance understanding of pipeline processing, data hazards, and instruction decoding in MIPS-like systems.

## 2. Background
MIPS-lite Simulators - The MIPS-lite simulator is a simplified version of the MIPS (Microprocessor without Interlocked Pipelined Stages) architecture, designed specifically for educational purposes to demonstrate the basic functionality of a MIPS processor. It involves the following components and functionalities:

  ### a. Functional Simulator:
This basic simulator models the sequential execution of instructions without considering any pipeline techniques. 
It aims to replicate the core aspects of MIPS, including register operations, memory access, and simple branching.<br>
  ### b. Pipelined Simulator without Forwarding:
Enhancing the functional simulator, this model introduces pipelining, a technique that overlaps the 
execution of multiple instructions to improve throughput. However, without forwarding (or data hazard resolution), 
this simulator also demonstrates the impact of data dependencies between successive instructions, which can lead to stalls or bubbles in the pipeline.<br>
  ### c. Pipelined Simulator with Forwarding:
This version of the simulator includes mechanisms to resolve data hazards by forwarding data directly between pipeline stages, 
reducing the need for stalls and thus improving the efficiency of the pipelined execution.<br>

The primary objective of this project is to simulate a MIPS-like processor, referred to as MIPS-lite, which involves a 5-stage instruction pipeline.<br>
The stages typically include:

a. Instruction Fetch (IF): Retrieve the instruction from memory.<br>
b. Instruction Decode (ID): Decode the instruction and read registers.<br>
c. Execute (EX): Perform the operation or calculate an address.<br>
d. Memory Access (MEM): Access the memory operand.<br>
e. Write Back (WB): Write the result back to the register file.<br>

The MIPS-lite simulator aims to accurately model both the functional behavior of instructions 
(how they modify the state of the machine) and their timing behavior (how long they take to execute through the pipeline).

Through this project, I gain hands-on experience with key concepts in computer architecture, including:

a. Instruction Set Design: Understanding how different instructions influence processor design and performance.<br>
b. Pipeline Simulation: Learning how instructions are processed in overlapping stages to optimize CPU performance.<br>
c. Hazard Detection and Handling: Identifying and resolving conflicts in instruction execution (data hazards, control hazards) that can cause stalls in the pipeline.<br>
d. Performance Analysis: Evaluating how different design choices affect the speed and efficiency of the processor.<br>

## 3. Simulator Input**
Memory Image: Containing both the code and data segments of the simulated program.<br>

## 4. Simulator Output
Program Output: Register values and memory contents after execution.<br>
Statistics: Breakdown of instruction types and execution time in cycles.<br>

## 5. Installation
To set up the simulator, clone the repository and compile the source code using an appropriate compiler for the chosen programming language.<br>

_git clone [repository-link]_
_cd [project-directory]_
_make_ <br>

## 6. Usage
To run the simulator, use the following command:<br>

`./simulator [memory-image-file]`

## 7. Documentation
Detailed project specifications and operational details can be found in the document directory.


## 8. Contact Information
For any inquiries or further information, please contact [rmuttha@pdx]
