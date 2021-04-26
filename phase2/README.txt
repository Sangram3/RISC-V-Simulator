Team Members :
1. 2019CSB1076 - Antara Agarwal 
2. 2019CSB1081 - Bharat  Sharma
3. 2019CSB1090 - Himanshi Nim
4. 2019CSB1091 - Jagadale Sangram Rajendra 
5. 2019CSB1104 - Nupur Rathi




-------------------------------------------------------------------------------------------------------------------------------


For phase 2 , pipelining was introduced into the RISC-V Simulator .
Directories :




Installation :
1. Unzip the RISCV_Simulator
2. Run the Simulator.bat in RISCV_Simulator or Run gui.py in Phase2 with Python.


Requirements:
1. Python 3.9.4 installed
2. PyQt5 5.11.3 installed


How to Run :
1. Run the Simulator.bat in RISCV_Simulator or Run gui.py in Phase2 with Python.
2. A GUI will open.
3. In the Editor tab of GUI, press Select file and browse and select the Input machine code file.
4. The contents of Input.mc will get displayed on Editor tab
5. You’ll notice a number of check boxes for pipelining , forwarding , printing register values at the end of each cycle ….. Tick the desired box for corresponding result
6. For non-pipeline the execution and gui panes will remain the same as last phase.






Individual contributions -
1. 2019CSB1076 - Antara Agarwal :-  HDU Hazard detection unit, BTB (branch table buffer) class, Interstate buffers class, testing the code on various inputs for stalling, data forwarding and data hazards, debugging, getting output stats and general help here and there.
2. 2019CSB1081 - Bharat  Sharma : Graphical User Interface (GUI).
3. 2019CSB1090 - Himanshi Nim : Handling Control instructions, flushing during misprediction , debugging and testing the code on various inputs.
4. 2019CSB1091 - Jagadale Sangram Rajendra : Structure of Pipeline, Data-Stalling, Control Hazard, flushing during misprediction,Testing of Stalling and Data Hazards, stage functions (fetching, decode, execute ), testing the code on various inputs and debugging, and general help here and there.
5. 2019CSB1104 - Nupur Rathi :- Data forwarding all types, HDU Hazard detection unit, all 5 stage functions  (fetching, decoding, execute, mem access, writeback ), testing the code on various inputs and debugging for data forwarding,  getting output stats, and general help here and there.