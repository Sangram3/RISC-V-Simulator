from data_forw import *
from HDU import *

def fetch_p(reg_mod, mem_mod, btb, buffers, index, pipeline_obj, cache_ob, gui_util_obj):
    """
        PC: Program Counter
        reg_mod : register module
        mem_mod : memory module
        btb : branch target buffer
        pipeline_obj : pipeline object
        cache_ob : cache_object
    """
    PC = reg_mod.get_PC() # get program counter
    inst = cache_ob.read(hex(PC), mem_mod, "Fetch", gui_util_obj) # get next instruction 
    
    tag, set_no, bo = cache_ob.decode_address(hex(PC)) # get set number
    copy_set = cache_ob.cache_array[set_no][:] # copy of the set

    temp = ["Fetch", hex(PC), set_no, copy_set]
    set_no = None
    gui_util_obj.task2.append(temp)
    temp = []

    pipeline_obj.n_inst += 1

    # PC is disabled
    if pipeline_obj.disable_PC == 0:
        if btb.ifPresent(PC) == False:
            reg_mod.add_PC(4)
        else:
            if btb.prediction(PC) == True:
                gui_util_obj.static_prediction.append( [pipeline_obj.cycle,PC,"True"])
                reg_mod.update_PC(btb.getTarget(PC) )
            else:
                gui_util_obj.static_prediction.append( [pipeline_obj.cycle,PC,"False"])
                reg_mod.add_PC(4)
                
    else:
        return

    # Exit instruction.
    if(inst == "0xEF000011"):
        pipeline_obj.finish = 1
        return
    

    buffers[0].PC = PC
    buffers[0].IR = inst
    # Insert Decode for current instruction
    pipeline_obj.pipeline[pipeline_obj.cycle+1].insert(index,"D")
