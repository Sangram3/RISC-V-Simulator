from memory import *
from registers import *
from fetch import *
from decode import *
from execute import *
from mem import *
from write_back import *
from buffers import *
from branch_table_buffer import *
import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
    
class gui_util():
    def __init__():
        self.data_hazards = {} # sangram
        self.matrix = [] # sangram
        self.left_pane = [] # sangram
        self.buffers_pane = [] # antara
        self.data_path_taken = [] # nupur
        self.static_prediction = [] # antara
        
        
        
class PipeLine():
    
    def __init__(self):
        self.pipeline = [["F"]]
        self.cycle = 0
        self.forw_d = {"EE": [0,None], "ME": [0,None], "MM": [0,None], "MES": [0,None], "ED": [0,None], "MD": [0,None], "EDS": [0,None], "MDS": [0,None], "MDSS": [0,None]}
        self.prevInsList = []
        self.master_store = [-1 for i in range(32)]
        self.to_stall = 0
        self.data_forwarding_knob = 1
        self.disable_PC = 0
        self.finish = 0

        self.n_inst = -1 # to avoid swi instr counting
        self.cpi = 0
        self.n_datatrans = 0
        self.n_alu_ins = 0
        self.n_cont_ins = 0
        self.nstalls = 0
        self.n_datastalls = 0
        self.n_contstalls = 0
        self.ndhz = 0
        self.nchz = 0
        self.npred = 0 

    def code_ends(self):
        text = ""
        text += "Total number of cycles"
        text += str(self.cycle)
        text+="\n"
        text += "Total instructions executed"
        text += str(self.n_inst)
        text+="\n"
        text += "CPI"
        text += str(self.CPI())
        text+="\n"
        text += "Number of Data-transfer (load and store) instructions executed"
        text += str(self.n_datatrans)
        text+="\n"
        text += "Number of ALU instructions executed"
        text += str(self.n_alu_ins)
        text+="\n"
        text += "Number of Control instructions executed"
        text += str(self.n_cont_ins)
        text+="\n"
        text += "Number of stalls/bubbles in the pipeline"
        text += str(self.nstalls)
        text+="\n"
        text += "Number of data hazards"
        text += str(self.ndhz)
        text+="\n"
        text += "Number of control hazards"
        text += str(self.nchz)
        text+="\n"
        text += "Number of branch mispredictions"
        text += str(self.npred)
        text+="\n"
        text += "Number of stalls due to data hazards"
        text += str(self.n_datastalls)
        text+="\n"
        text += "Number of stalls due to control hazards"
        text += str(self.n_contstalls)
        text+="\n"
        return text

    def CPI(self):
        return self.cycle/self.n_inst

    def clear_pipeline(self):
        self.__init__()
        
    def data_forwarding(self):
        pass
    
    def update_pipeline(self,cycle):
        pass
    
    def call_stalling(self,index): # stall the pipeline by one cycle
        self.nstalls = self.nstalls+1
        self.disable_PC = 1 # PC update stopped
        self.pipeline[self.cycle+1].insert(index,self.pipeline[self.cycle][index]) # inserting the same instruction in the next cycle too
        
        return 
    
    
    def flush(self):
        # make previously fetched instruction NOP
        for i in range(len(self.pipeline[self.cycle])):
            if self.pipeline[self.cycle][i] == 'F':
                self.pipeline[self.cycle][i] ='NOP'
                self.prevInsList.append(['NOP'])
                
    
        
    def check_data_hazard(self,name_rs1,name_rs2):
        if name_rs1!=None:
              if self.master_store[name_rs1] >= self.cycle:
                  return 1
        if name_rs2!=None: 
              if self.master_store[name_rs2] >= self.cycle:
                  return 1
        return 0 # no data hazard case

pipeline_obj = PipeLine()
# pipeline_obj.data_forwarding_knob = 0
mc_file = "test.mc"
mem_mod = memory(mc_file)
reg_mod = registers()
buffers = [InterStateBuffer() for i in range(4)]
btb = BTB()
global_buffers = []

gui_util_obj = gui_util()


#pipe = [  [ "Fetch"] ["Fetch" , "Decode" ] [ "Fetch", "Decode" , "Execute"]       ]

def execute_cycle_util():
    
    while (pipeline_obj.pipeline[pipeline_obj.cycle] != [] and pipeline_obj.cycle!=60 ):
        execute_cycle()
        global_buffers.append(buffers[:])

def execute_cycle():
    global pipeline_obj

    print ("cycle no.=", pipeline_obj.cycle,  ":" , pipeline_obj.pipeline[pipeline_obj.cycle])
    pipeline_obj.pipeline.append([])

    for index in range(len(pipeline_obj.pipeline[pipeline_obj.cycle])):
        if pipeline_obj.pipeline[pipeline_obj.cycle][index] == 'D':
            decode(mem_mod, reg_mod ,pipeline_obj ,buffers , index, btb)
                
        if pipeline_obj.pipeline[pipeline_obj.cycle][index] == 'F':
            fetch(reg_mod, mem_mod, btb, buffers, index, pipeline_obj)
            
        if pipeline_obj.pipeline[pipeline_obj.cycle][index] == 'E':
            execute(reg_mod, pipeline_obj, buffers,index )
            
        if pipeline_obj.pipeline[pipeline_obj.cycle][index] == 'M':
            mem(mem_mod, reg_mod, buffers, index, pipeline_obj)
            
        if pipeline_obj.pipeline[pipeline_obj.cycle][index] == 'W':
            write_back(reg_mod, buffers, pipeline_obj)
                
    if pipeline_obj.to_stall == 0 and pipeline_obj.finish == 0 and pipeline_obj.disable_PC == 0:
        pipeline_obj.pipeline[pipeline_obj.cycle+1].append("F")
    pipeline_obj.cycle+=1


execute_cycle_util()
print(reg_mod.get_regs())
print(mem_mod.print_mem())
print(btb.btb)
print(pipeline_obj.code_ends())
