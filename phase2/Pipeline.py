from memory import *
from registers import *
from fetch import *
from decode import *
from execute import *
from mem import *
from write_back import *
from buffers import *
import sys

# if not sys.warnoptions:
#     import warnings
#     warnings.simplefilter("ignore")
    
    
class PipeLine():
    
    def __init__(self):
        self.pipeline = [["F"]]
        self.cycle = 0
        self.forw_d = {"EE": [0,None], "ME": [0,None], "MM": [0,None], "MES": [0,None], "ED": [0,None], "MD": [0,None], "EDS": [0,None], "MDS": [0,None]}
        self.prevInsList = []
        self.master_store = [-1 for i in range(32)]
        self.to_stall = 0
        self.data_forwarding_knob = 0
        self.disable_PC = 0
        self.finish = 0


    def clear_pipeline(self):
        self.__init__()
        
    def data_forwarding(self):
        pass
    
    def update_pipeline(self,cycle):
        pass
    
    def call_stalling(self,index): # stall the pipeline by one cycle
        self.disable_PC = 1 # PC update stopped
        self.pipeline[self.cycle+1].insert(index,self.pipeline[self.cycle][index]) # inserting the same instruction in the next cycle too
        
        return 
    
    
    def flush(self):
        # make previously fetched instruction NOP
        for i in range(len(self.pipeline[self.cycle])):
            if self.pipeline[self.cycle][i] == 'F':
                self.pipeline[self.cycle][i] ='NOP'
                
    
        
    def check_data_hazard(self,name_rs1,name_rs2):
        if name_rs1!=None:
              if self.master_store[name_rs1] >= self.cycle:
                  return 1
        if name_rs2!=None: 
              if self.master_store[name_rs2] >= self.cycle:
                  return 1
        return 0 # no data hazard case

pipeline_obj = PipeLine()
mc_file = "test.mc"
mem_mod = memory(mc_file)
reg_mod = registers()
buffers = [InterStateBuffer() for i in range(4)]
btb = BTB()


#pipe = [  [ "Fetch"] ["Fetch" , "Decode" ] [ "Fetch", "Decode" , "Execute"]       ]

def execute_cycle_util():
    
    while (pipeline_obj.pipeline[pipeline_obj.cycle] != []):
        execute_cycle()

def execute_cycle():
    global pipeline_obj

    print ("cycle no.=", pipeline_obj.cycle,  ":" , pipeline_obj.pipeline[pipeline_obj.cycle])
    pipeline_obj.pipeline.append([])

    for index in range(len(pipeline_obj.pipeline[pipeline_obj.cycle])):

        if pipeline_obj.pipeline[pipeline_obj.cycle][index] == 'D':
            decode(mem_mod, reg_mod ,pipeline_obj ,buffers , index)
                
        if pipeline_obj.pipeline[pipeline_obj.cycle][index] == 'F':
            fetch(reg_mod, mem_mod, btb, buffers, index, pipeline_obj)
            
        if pipeline_obj.pipeline[pipeline_obj.cycle][index] == 'E':
            execute(reg_mod, pipeline_obj, buffers,index )
            
        if pipeline_obj.pipeline[pipeline_obj.cycle][index] == 'M':
            mem(mem_mod, reg_mod, buffers, index, pipeline_obj)
            
        if pipeline_obj.pipeline[pipeline_obj.cycle][index] == 'W':
            write_back(reg_mod, buffers)
                
    if pipeline_obj.to_stall == 0 and pipeline_obj.finish == 0 and pipeline_obj.disable_PC == 0:
        pipeline_obj.pipeline[pipeline_obj.cycle+1].append("F")
    pipeline_obj.cycle+=1


execute_cycle_util()
print(reg_mod.get_regs())
print(mem_mod.print_mem())
