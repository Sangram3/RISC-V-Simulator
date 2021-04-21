#  d = [EE:0, ME:0, MM:0, MES: 0, ED:0, MD:0, EDS:0, MDS:0]
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

    # E-D
    elif(forw_type == 4):
        if(reg == 1):
            buffers[0].operand1 = buffers[2].RZ 
        elif(reg == 2):
            buffers[0].operand2 = buffers[2].RZ
        elif(reg == 3):
            buffers[0].operand1 = buffers[2].RZ
            buffers[0].operand2 = buffers[2].RZ

    # M-D
    elif(forw_type == 5):
        if(reg == 1):
            buffers[0].operand1 = buffers[3].RY 
        elif(reg == 2):
            buffers[0].operand2 = buffers[3].RY
        elif(reg == 3):
            buffers[0].operand1 = buffers[3].RY
            buffers[0].operand2 = buffers[3].RY

    
        

# in execute step:
#     execute()
#     then if data_forwarding is to be done:
#         if(d[MM] == 1):
#             data_forw(MM)
#             d[MM] = 0

# in decode step :
#     decode()
#     then we will check if dfata hazard and which type and update d accordingly
#     then if data hazaerd and data_forwarding is to be done:
#         if(d[ME] == 1):
#             data_forw(ME)
#             d[ME] = 0
#         if(d[EE] == 1):
#             data_forw(EE)
#             d[EE] = 0
#         if(d[MES] == 1):
#             stall by one cycle accordingly
#             d[MES] = 0
