from data_forw import *
from HDU import *

def fetch(reg_mod, mem_mod, btb, buffers, index, pipeline_obj):
    
    PC = reg_mod.get_PC()
    inst = mem_mod.lw(PC)
    if pipeline_obj.disable_PC == 0:
        reg_mod.add_PC(4)
    else:
        return
    # print(inst,PC)
    if(inst == "0xEF000011"):
        pipeline_obj.finish = 1
        return
    
    IR = int(inst, 16)
    opcode = IR & (0x7F)

    # data-forwarding = M-D and E-D
    if(opcode == 99 and pipeline_obj.data_forwarding_knob == 1): # SB type
        buffers[0].operand1 = registers.__regs[rs1]
        buffers[0].operand2 = registers.__regs[rs2]
        rs1 = IR & (0xF8000)
        rs1 = rs1 >> 15
        rs2 = IR & (0x1F00000)
        rs2 = rs2 >> 20
        func3 = IR & (0x7000)
        func3 = func3 >> 12
        if(func3 == 0):
            mne = "beq"
        elif(func3 == 1):
            mne = "bne"
        elif(func3 == 4):
            mne = "blt"
        elif(func3 == 5):
            mne = "bge"  
        buffers[0].fmt = 4
        buffers[0].rs1 = rs1
        buffers[0].rs2 = rs2
        buffers[0].mne = mne
    elif(opcode == 103): # jalr
        buffers[0].operand1 = registers.__regs[rs1]
        rd = IR & (0xF80)
        rd = rd//128
        buffers[0].rd = rd
        buffers[0].fmt = 2
        buffers[0].mne = 'jalr'

    if(opcode == 99 or opcode == 103 and pipeline_obj.data_forwarding_knob == 1):

        if(pipeline_obj.forw_d["MDS"][0] == 1 ):
            data_forw(5, pipeline_obj.forw_d["MDS"][1], buffers)
            pipeline_obj.forw_d["MDS"][0] = 0
            pipeline_obj.forw_d["MDS"][1] = None

        elif(pipeline_obj.forw_d["EDS"][0] == 1):
            if(pipeline_obj.forw_d["MD"][0] == 1):
                data_forw(5, pipeline_obj.forw_d["MD"][1], buffers)
                pipeline_obj.forw_d["MD"][0] = 0
                pipeline_obj.forw_d["MD"][1] = None
            data_forw(4, pipeline_obj.forw_d["EDS"][1], buffers)
            pipeline_obj.forw_d["EDS"][0] = 0
            pipeline_obj.forw_d["EDS"][1] = None

        else:
            #check data hazard using HDU Unit
            HDU(buffers, 1, pipeline_obj.prevInsList, pipeline_obj.forw_d)
            if(pipeline_obj.forw_d["MDS"][0] == 1 or pipeline_obj.forw_d["EDS"][0] == 1):
                pipeline_obj.call_stalling(index)
                return
                
            if(pipeline_obj.forw_d["MD"][0] == 1 and pipeline_obj.forw_d["MDS"][0] == 0):
                data_forw(5, pipeline_obj.forw_d["MD"][1], buffers)
                pipeline_obj.forw_d["MD"][0] = 0
                pipeline_obj.forw_d["MD"][1] = None

            if(pipeline_obj.forw_d["ED"][0] == 1 and pipeline_obj.forw_d["EDS"][0] == 0):
                data_forw(4, pipeline_obj.forw_d["ED"][1], buffers)
                pipeline_obj.forw_d["ED"][0] = 0
                pipeline_obj.forw_d["ED"][1] = None          


    # predicting 
	# if(opcode == 103 or opcode == 99 or opcode == 111):
	# 	if (btb.ifPresent(PC) and btb.prediction(PC)):
	# 		buffers[0].predict = True
		
    buffers[0].PC = PC
    buffers[0].IR = inst
    pipeline_obj.pipeline[pipeline_obj.cycle+1].insert(index,"D")
