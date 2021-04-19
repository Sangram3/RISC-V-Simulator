from registers import *

class PipeLine():
    
    def __init__(self):
        self.pipeline = []
        self.cycle = 0
        self.master_store = [[] for i in range(32)]
        

    def data_forwarding(self):
        pass
    
    def update_pipeline(self,cycle):
        pass
    
    def call_stall(self): # stall the pipeline by one cycle
    
        self.pipeline.insert(self.cycle,[]) # inserting bubble
        self.cycle+=1
        return 
        
    def check_data_hazard(self,fmt):
         if fmt == 1 or fmt == 4: 
              rs1_name = registers.get_name_rs1()
              rs2_name = registers.get_name_rs2()
              if master_store[rs1_name] >= self.cycle or master_store[rs2_name]>= self.cycle:
                  return 1 # data hazard case
         
         if fmt == 2 or fmt == 3 : 
              rs1_name = registers.get_name_rs1()
              if self.master_store[rs1_name] >= self.cycle:
                  return 1
         return 0 # no data hazard case

pipeline_obj = PipeLine()


def execute_cycle_util():
    while True:
        execute_cycle()

def execute_cycle():
    global pipeline_obj
    flag = 0
    for stage in pipeline_obj.pipeline:
        if stage[0] == "Execute":
            flag = pipeline_obj.check_data_hazard()
            if flag == 1:
                break
    if flag == 1:
        pipeline_obj.call_stalling()
    else:
        for stage in pipeline_obj.pipeline:
                
            if stage[0] == "Execute":
                pass
                # execute()
            if stage[0] == "Decode":
                pass
                # decode()
            if stage[0]  == "MemoryAccess":
                pass
                # memory()
            if stage[0] == "WriteBack":
                pass
                # writeback()
                
            
            
        
        
    
        
