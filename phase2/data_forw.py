# d = {"EE": [0,0], "ME": [0,0], "MM": [0,0] "MES": [0,0], "ED": [0,0], "MD": [0,0], "EDS": [0,0], "MDS": [0,0]}
# EE = 1, ME = 2, MM = 3, ED = 4, MD = 5, MES = 6, EDS = 7, MDS = 8
# reg = which register acts as hazard, that is rs1 or rs2 or both # 1 for rs1, 2 for rs2, 3 for both
# in below example both rs1 and rs2 acts as a hazard :
# addi x12 x1 x0
# add x14 x12 x12

def data_forw(forw_type, reg, buffers):

    # E-E
    if(forw_type == 1):
        if(reg == 1):
            buffers[1].operand1 = buffers[2].RZ 
        elif(reg == 2):
            buffers[1].operand2 = buffers[2].RZ
        elif(reg == 3):
            buffers[1].operand1 = buffers[2].RZ
            buffers[1].operand2 = buffers[2].RZ

    # M-E
    elif(forw_type == 2):
        if(reg == 1):
            buffers[1].operand1 = buffers[3].RY 
        elif(reg == 2):
            buffers[1].operand2 = buffers[3].RY
        elif(reg == 3):
            buffers[1].operand1 = buffers[3].RY
            buffers[1].operand2 = buffers[3].RY

    # M-M
    elif(forw_type == 3):
        if(reg == 1):
            buffers[2].operand1 = buffers[3].RY 
        elif(reg == 2):
            buffers[2].operand2 = buffers[3].RY
        elif(reg == 3):
            buffers[2].operand1 = buffers[3].RY
            buffers[2].operand2 = buffers[3].RY
        buffers[2].MDR = buffers[3].RY
        buffers[2].RM = buffers[3].RY
 
    # E-D
    elif(forw_type == 4):
        if(reg == 1):
            buffers[0].operand1 = buffers[2].RA 
        elif(reg == 2):
            buffers[0].operand2 = buffers[2].RA
        elif(reg == 3):
            buffers[0].operand1 = buffers[2].RA
            buffers[0].operand2 = buffers[2].RA

    # M-D
    elif(forw_type == 5):
        if(reg == 1):
            buffers[0].operand1 = buffers[3].RB 
        elif(reg == 2):
            buffers[0].operand2 = buffers[3].RB
        elif(reg == 3):
            buffers[0].operand1 = buffers[3].RB
            buffers[0].operand2 = buffers[3].RB
