from data_forw import *
from HDU import *

def fetch_p(reg_mod, mem_mod, btb, buffers, index, pipeline_obj):
    
    PC = reg_mod.get_PC()
    inst = mem_mod.lw(PC)
    pipeline_obj.n_inst = pipeline_obj.n_inst + 1
    print()
    print(PC,inst)
    print()
    if pipeline_obj.disable_PC == 0:
        if btb.ifPresent(PC) == False:
            reg_mod.add_PC(4)
        else:
            if btb.prediction(PC) == True:
                # print(PC,"friends")
                gui_util_obj.static_prediction.append( [pipeline_obj.cycle,PC,"True"])
                reg_mod.update_PC(btb.getTarget(PC) )
                # print(reg_mod.get_PC())
            else:
                gui_util_obj.static_prediction.append( [pipeline_obj.cycle,PC,"False"])
                reg_mod.add_PC(4)
                
    else:
        return
    # print(inst,PC)
    if(inst == "0xEF000011"):
        pipeline_obj.finish = 1
        return
          

		
    buffers[0].PC = PC
    buffers[0].IR = inst
    pipeline_obj.pipeline[pipeline_obj.cycle+1].insert(index,"D")
