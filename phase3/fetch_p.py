from data_forw import *
from HDU import *

def fetch_p(reg_mod, mem_mod, btb, buffers, index, pipeline_obj, cache_ob, gui_util_obj):
    
    PC = reg_mod.get_PC()
    inst = cache_ob.read(hex(PC), mem_mod, "Fetch", gui_util_obj)
    
    tag, set_no, bo = cache_ob.decode_address(hex(PC))
    copy_set = cache_ob.cache_array[set_no][:]

    temp = ["Fetch", hex(PC), set_no, copy_set]
    tag = None
    set_no = None
    bo = None
    gui_util_obj.task2.append(temp)
    temp = []

    pipeline_obj.n_inst = pipeline_obj.n_inst + 1

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
    if(inst == "0xEF000011"):
        pipeline_obj.finish = 1
        return
          

		
    buffers[0].PC = PC
    buffers[0].IR = inst
    pipeline_obj.pipeline[pipeline_obj.cycle+1].insert(index,"D")
