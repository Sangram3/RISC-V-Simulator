from data_forw import *
from HDU import *

def fetch(reg_mod, mem_mod, btb, buffers, index, pipeline_obj):
    
    PC = reg_mod.get_PC()
    inst = mem_mod.lw(PC)
    
    if pipeline_obj.disable_PC == 0:
        if btb.ifPresent(PC) == False:
            
            reg_mod.add_PC(4)
        else:
            reg_mod.update_PC(btb.table[str(PC)][1] )
    else:
        return
    # print(inst,PC)
    if(inst == "0xEF000011"):
        pipeline_obj.finish = 1
        return
          

		
    buffers[0].PC = PC
    buffers[0].IR = inst
    pipeline_obj.pipeline[pipeline_obj.cycle+1].insert(index,"D")
