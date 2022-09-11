<p align="center">
    <img src="logo.png" alt="Logo" width="580" height="200">
</p>
<br/>

**Team Members:**

Jagadale Sangram Rajendra - 2019CSB1091

Antara Arun Agarwal - 2019CSB1076

Bharat Sharma - 2019CSB1081

Himanshi Nim - 2019CSB1090

Nupur Rathi - 2019CSB1104

**About:**
RISC-V Simulator is a python based program which is a simulation to run machine code

**Directories:**
**RISCV_Simulator**

<p align="center">
    <img src="tree.png" alt="Logo" >
</p>
<br/>
	|
	|--- Phase1
	|	      |--- gui.py
	|	      |--- RISCV_Sim.py
	|	      |--- memory.py
	|	      |--- registers.py
	|	      |--- fetch.py
	|	      |--- decode.py
	|	      |--- execute.py
	|	      |--- mem.py
	|	      |--- write_back.py
	|	      |--- temp.mc
	|
	|--- test
	|	     |--- bubblesort_recursive.mc
	|	     |--- bubblesort_iterative.mc
	|	     |--- factorial_iterative.mc
	|	     |--- factorial_recursive.mc
	|	     |--- fibonacci_iterative.mc
	|	     |--- fibonacci_recursive.mc
	|	     |--- test.mc
  |
  |--- output 
  |	      |--- output.mc
  |
  |--- Simulator.bat
  
**Installation:**
 1. Unzip the RISCV_Simulator
 2. Run the Simulator.bat in RISCV_Simulator or Run gui.py in Phase1 with Python.

**Requirements:**
  1. Python installed
  2. PyQt5 installed

**How to Run:**
 1. Run the Simulator.bat in RISCV_Simulator or Run gui.py in Phase1 with Python.
 2. A GUI will open.
 3. In the Editor tab of GUI, press Select file and browse and select the Input machine code file.
 4. The contents of Input.mc will get displayed on Editor tab
 5. Now Go to the Simulator tab and Click Run to Run all the instructions or click Step to run 1 instruction at a time.
 6. In the  Right side of GUI, there are two tabs: Memory and Register.
 7. Memory tab provides the Values Stored in memory at that moment.
 8. The navigation pane in the memory tab can be used to go to a particular Memory location.
 9. The Register tab shows the current value stored in registers in hex.
 10. The Reset button will Reset the Memory and Registers and Clear the Input output Consoles. You can select another file after this.
 11. The dump button will save the Current memory State into an Output.mc file.
 12. In the input console clock (clk), PC, Machine code and Basic code will be displayed for the instructions which have been executed.
 13. The output console will display the information for all the instructions which have been executed.
 14. It will display about what has been performed in the stages (fetch, decode, execute, memory access and write back) of one instruction.


**Instructions Supported:**
R format - add, and, or, sll, slt, sra, srl, sub, xor, mul, div, rem 

I format - addi, andi, ori, lb, lh, lw, jalr 

S format - sb, sw, sh 

SB format - beq, bne, bge, blt 

U format - auipc, lui 

UJ format - jal

**Individual Contributions:**

Sangram Jagadale     : functionality of execute stage,functionality of stalling ,GUI designing ,testing .

Nupur Rathi          : functionality of decode stage,functionality of data-forwarding ,testing .

Himanshi Nim         : GUI designing ,testing .

Bharat Sharma        : GUI designing , functionality of cache ,memory and write-back stage.

Antara Arun Aggarwal : functinality of memory ,write-back stage ,testing and data forwarding




