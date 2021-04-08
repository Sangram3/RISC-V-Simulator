                                                                 __________________________________________________
                                                                 |	 _____       _____    _____		  |
                                                                 |	|     |  |  |        |          \      /  |
                                                                 |	|_____|  |  |_____   |      __   \    /   |
                                                                 |	|   \    |     	  |  |            \  /    |
                                                                 |	|    \   |   _____|  |_____        \/     |
                                                                 |________________________________________________|
                                                                 
Team Members:
2019CSB1076 - Antara Arun Agarwal 
2019CSB1081 - Bharat Sharma 
2019CSB1090 - Himanshi Nim
2019CSB1091 - Jagadale Sangram Rajendra 
2019CSB1104 - Nupur Rathi 

About:
RISC-V Simulator is a python based program which is a simulation to run machine code.

Directories:
RISCV_Simulator
	|
	|--- Phase1
	|	  |--- gui.py
	|	  |--- RISCV_Sim.py
	|	  |--- memory.py
	|	  |--- registers.py
	|	  |--- fetch.py
	|	  |--- decode.py
	|	  |--- execute.py
	|	  |--- mem.py
	|	  |--- write_back.py
	|	  |--- temp.mc
	|
	|--- test
	|	|--- bubblesort_recursive.mc
	|	|--- bubblesort_iterative.mc
	|	|--- factorial_iterative.mc
	|	|--- factorial_recursive.mc
	|	|--- fibonacci_iterative.mc
	|	|--- fibonacci_recursive.mc
	|	|--- test.mc
        |
        |
        |--- Simulator.bat

Installation:
 1. Unzip the RISCV_Simulator
 2. Run the Simulator.bat in RISCV_Simulator or Run gui.py in Phase1 with Python.

Requirements:
  1. Python 3.9.4 installed
  2. PyQt5 5.11.3 installed

How to Run:
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
 11. The dump button will save the Current memory State into a Selected file.
 12. In the input console clock (clk), PC, Machine code and Basic code will be displayed for the instructions which have been executed.
 13. The output console will display the information for all the instructions which have been executed.
 14. It will display about what has been performed in the stages (fetch, decode, execute, memory access and write back) of one instruction.

Note : Sometimes Program may stop responding on Large Tasks due to The large number of print stmts in the output panel. Please wait for it to respond.

Instructions Supported:
R format - add, and, or, sll, slt, sra, srl, sub, xor, mul, div, rem 
I format - addi, andi, ori, lb, lh, lw, jalr 
S format - sb, sw, sh 
SB format - beq, bne, bge, blt 
U format - auipc, lui 
UJ format - jal

Individual Contributions:
 As this was a team project so it is difficult to completely segregate out the work done by each of us.
 But the main focus areas of Team Members were: 
  1. Fetch , Decode, Execute - Jointly Coded by Nupur, Sangram and Himanshi
  2. Main Memory, Memory Access, Writeback - Jointly Coded by Antara and Bharat
  3. GUI - Jointly Coded by Sangram, Himanshi and Bharat
  4. Control and combining the different stages - Jointly Coded by Nupur and Antara





