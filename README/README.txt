Team Members :
1. 2019CSB1076 - Antara Agarwal 
2. 2019CSB1081 - Bharat  Sharma
3. 2019CSB1090 - Himanshi Nim
4. 2019CSB1091 - Jagadale Sangram Rajendra 
5. 2019CSB1104 - Nupur Rathi




-------------------------------------------------------------------------------------------------------------------------------


For phase 3 ,instruction and data cache modules were introduced into the RISC-V Simulator.


Installation :
1. Unzip the RISCV_Simulator
2. Run gui.py in Phase3 with Python.


Requirements:
1. Python 3.9.4 installed
2. PyQt5 5.11.3 installed


How to Run :
1. Run gui.py in Phase3 with Python.
2. A prompt will be displayed on the terminal asking you to enter the following details :
   1. Cache size for data cache in kilobytes: 
   2. Block size for data cache in bytes: 
   3. Number of ways for SA for data cache: 
   4. Cache size for instruction cache in kilobytes: 
   5. Block size for instruction cache in bytes: 
   6. Number of ways for SA for instruction cache: 


3. After entering all the values ,a GUI will open.
4. In the Editor tab of GUI, press Select file and browse and select the Input machine code file.
5. The contents of Input.mc will get displayed on Editor tab
6. You’ll notice a number of check boxes for 
   1. pipelining 
   2. forwarding 
   3. printing register values at the end of each cycle
   4. printing pipeline registers
7. Tick the desired box for corresponding result
8. For non-pipeline the execution and gui panes will remain the same as last phase.
9. The new Gui requirements of phase 3 have been added in the right pane of the simulator tab where :
   1. I_CACHES and D_CACHES display the contents of all the sets of the cache  which have non-zero data.
   2. SET shows the set that is accessed for each Fetch, Load, Store.
   3. VB shows the victim block upon a miss.
   4. STATS displays the number of main memory accesses , cache accesses , cache hits and cache misses
10.  Functionalities of Run / Reset / Dump have been provided.






    




Individual contributions -
1. Sangram - GUI, minor corrections in the previous phase code.
2. Himanshi - GUI, minor corrections in the previous phase code.
3. Antara - Integrating cache with pipelined and non-pipelined executions, output stats, testing and debugging, few implementations in cache class, minor corrections in the previous phase code.
4. Nupur - Integrating cache with pipelined and non-pipelined executions, output stats, testing and debugging, few implementations in cache class, minor corrections in the previous phase code.
5. Bharat - Implementation of cache class and LRU policy.