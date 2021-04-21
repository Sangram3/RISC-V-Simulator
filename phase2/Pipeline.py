from registers import *

class PipeLine():
    
    def __init__(self):
        self.pipeline = []
        self.cycle = 0
        self.d = {"EE": [0,None], "ME": [0,None], "MM": [0,None], "MES": [0,None], "ED": [0,None], "MD": [0,None], "EDS": [0,None], "MDS": [0,None]}
        self.master_store = [[] for i in range(32)]
        self.to_stall = 0
        self.data_forawarding_knob = 0
        self.disable_PC = 0

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
        
    def check_data_hazard(self,name_rs1,name_rs2):
        if name_rs1:
              if self.master_store[name_rs2] >= self.cycle:
                  return 1
        if name_rs2: 
              if self.master_store[name_rs2] >= self.cycle:
                  return 1
        return 0 # no data hazard case

pipeline_obj = PipeLine()


#pipe = [  [ "Fetch"] ["Fetch" , "Decode" ] [ "Fetch", "Decode" , "Execute"]       ]

def execute_cycle_util():
    while True:
        execute_cycle()

def execute_cycle():
    global pipeline_obj
    
    for index in range(len(pipeline_obj.pipeline[pipeline_obj.cycle])):

        if pipeline_obj.pipeline[pipeline_obj.cycle][index] == 'D':
            decode( memory, registers ,pipeline_obj ,buffers ,index)
                
        if pipeline_obj.pipeline[pipeline_obj.cycle][index] == 'F':
            fetch(registers, memory, btb, pipeline_obj,buffers,index)
            
        if pipeline_obj.pipeline[pipeline_obj.cycle][index] == 'E':
            execute()
            # NOT DONE YET
            
        if pipeline_obj.pipeline[pipeline_obj.cycle][index] == 'M':
            memory()
            #NOT DONE YET
            
        if pipeline_obj.pipeline[pipeline_obj.cycle][index] == 'W':
            writeback()
            #NOT DONE YET
                
        # if pipeline_obj.to_stall == 0:
        #     pipeline_obj[pipeline_obj.cycle+1].append("F")
        # pipeline_obj.cycle+=1
                

            
        
        
    
        
