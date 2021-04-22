from data_forw import *
from HDU import *

#decode function
#all extractions and decode done in string format and at the end converted everything to decimal, example rs1 = '00110' then rs1 becomes 6 at the end.
from collections import defaultdict

def bin32(num):
    return '{0:032b}'.format(num)

                                       # extra arguments
def decode(memory, registers ,pipeline_obj ,buffers , index):
    d = defaultdict(lambda: None)
    d = {'0110011': 1, '0010011': 2, '0000011': 2, '1100111': 2, '0100011': 3, '1100011': 4, '0010111': 5, '0110111': 5, '1101111': 6}

    inst = None
    op = None
    func3 = None
    func7 = None
    rd = None
    rs1 = None
    rs2 = None
    imm = None
    fmt = None
    mneumonic = None

    inst = buffers[0].IR # instruction inside the F-D buffer
    inst = bin32(int(inst,16))

    #opcode extraction
    op = inst[25:]
    #fmt check
    # print(op)
    fmt = d[op]

    #func3 extraction if present
    if (fmt != 5 and fmt != 6):
        func3 = inst[17:20]

    #func7 extraction if present
    if(fmt == 1):
        func7 = inst[0:7]

    #rs1 extraction if present
    if(fmt == 1 or fmt == 2 or fmt == 3 or fmt == 4):
        rs1 = inst[12:17]

    #rs2 extraction if present
    if(fmt == 1 or fmt == 3 or fmt == 4):
        rs2 = inst[7:12]

    #rd extraction if present
    if(fmt == 1 or fmt == 2 or fmt == 5 or fmt == 6):
        rd = inst[20:25]
        
    
    #mneumonic extraction if present
    if(fmt == 5 and op == '0010111'):
        mneumonic = 'auipc'
    if(fmt == 5 and op == '0110111'):
        mneumonic = 'lui'
    if(fmt == 6):
        mneumonic = 'jal'
    if(op == '1100111'):
        mneumonic = 'jalr'
    if(fmt == 4):
        if(func3 == '000'):
            mneumonic = 'beq'
        if(func3 == '001'):
            mneumonic = 'bne'
        if(func3 == '100'):
            mneumonic = 'blt'
        if(func3 == '101'):
            mneumonic = 'bge'
    if(fmt == 3):
        if(func3 == '000'):
            mneumonic = 'sb'
        if(func3 == '001'):
            mneumonic = 'sh'
        if(func3 == '010'):
            mneumonic = 'sw'
    if(op == '0000011'):
        if(func3 == '000'):
            mneumonic = 'lb'
        if(func3 == '001'):
            mneumonic = 'lh'
        if(func3 == '010'):
            mneumonic = 'lw'
    if(op == '0010011'):
        if(func3 == '000'):
            mneumonic = 'addi'
        if(func3 == '110'):
            mneumonic = 'ori'
        if(func3 == '111'):
            mneumonic = 'andi'
    if(fmt == 1):
        if(func3 == '000' and func7 == '0000000'):
            mneumonic = 'add'
        if(func3 == '000' and func7 == '0100000'):
            mneumonic = 'sub'
        if(func3 == '001' and func7 == '0000000'):
            mneumonic = 'sll'
        if(func3 == '010' and func7 == '0000000'):
            mneumonic = 'slt'
        if(func3 == '100' and func7 == '0000000'):
            mneumonic = 'xor'
        if(func3 == '101' and func7 == '0000000'):
            mneumonic = 'srl'
        if(func3 == '101' and func7 == '0100000'):
            mneumonic = 'sra'
        if(func3 == '110' and func7 == '0000000'):
            mneumonic = 'or'
        if(func3 == '111' and func7 == '0000000'):
            mneumonic = 'and' 
        if(func3 == '000' and func7 == '0000001'):
            mneumonic = 'mul'
        if(func3 == '100' and func7 == '0000001'):
            mneumonic = 'div'
        if(func3 == '110' and func7 == '0000001'):
            mneumonic = 'rem'

    op = int(op, base=2)
    if func3:
        func3 = int(func3, base=2)
    if func7:
        func7 = int(func7, base=2)
    if rd:
        rd = int(rd, base=2)
    if rs1:
        rs1 = int(rs1, base=2)
    if rs2:
        rs2 = int(rs2, base=2)
        
    if(fmt==2): #I
        imm=inst[0:12]
    
    elif(fmt==3): #S
        imm=(inst[0:7]+inst[20:25])
    
    elif(fmt==4): #SB
        imm=(inst[0]+inst[24]+inst[1:7]+inst[20:24])
        
    elif(fmt==5): #U
        imm=inst[0:20]
        
    elif(fmt==6): #UJ
        imm=(inst[0]+inst[12:20]+inst[11]+inst[1:11])

    # registers.set_rs1(rs1)
    # registers.set_rs2(rs2)
    # registers.set_rd(rd)
    
    # registers.set_name_rs1(rs1)
    # registers.set_name_rs2(rs2)
    # registers.set_name_rd(rd)
    
    # FOR CHECKING DATA DEPENDENCY
    # dh = pipeline_obj.check_data_hazard(rs1,rs2)
    # if dh == 1:
    #     if pipeline_obj.data_forwarding_knob ==0:
    #         pipeline_obj.call_stalling(index) # index is the at what index this instruction is present in the cycle
    #                                           # like ["E" ,"D" ] index of decode in this case is 1
    #     else:
    #         # handle by data forwarding

    #         pass
    #     return 
    # else:
    #     # buffers[1] = D-E BUFFER
        
    #     buffers[1].rs1 = rs1 # THESE ARE JUST ADDRESSES NOT VALUES
    #     buffers[1].rs2 = rs2
    #     buffers[1].rd  = rd 
        
    #     if rs1:
    #         buffers[1].operand1 = registers.__regs[rs1] # setting value of rs1 in buffer
    #     if rs2:
    #         buffers[1].operand2 = registers.__regs[rs2] # setting value of rs2 in buffer
    #     if imm:
    #         buffers[1].imm = imm # setting immediate in buffer
            
    #     buffers[1].mne = mneumonic
    #     buffers[1].fmt = fmt
    #     # UPDATE MASTER_STORE
    #     if rd:
    #         pipeline_obj.master_store[rd] = pipeline_obj.cycle+3
            
    #     pipeline_obj.pipeline[pipeline_obj.cycle+1].insert(index,"E") # Execute this instruction in the next cycle at the same index
    #     return (fmt, mneumonic, imm)

    if pipeline_obj.data_forwarding_knob == 0:
        dh = pipeline_obj.check_data_hazard(rs1,rs2)
        if dh == 1:
            pipeline_obj.call_stalling(index) # index is the at what index this instruction is present in the cycle
                                              # like ["E" ,"D" ] index of decode in this case is 1
            return
        else:
            # buffers[1] = D-E BUFFER
            
            buffers[1].rs1 = rs1 # THESE ARE JUST ADDRESSES NOT VALUES
            buffers[1].rs2 = rs2
            buffers[1].rd  = rd 
            
            if rs1:
                buffers[1].operand1 = registers.__regs[rs1] # setting value of rs1 in buffer
            if rs2:
                buffers[1].operand2 = registers.__regs[rs2] # setting value of rs2 in buffer
            if imm:
                buffers[1].imm = imm # setting immediate in buffer
                
            buffers[1].mne = mneumonic
            buffers[1].fmt = fmt
            # UPDATE MASTER_STORE
            if rd:
                pipeline_obj.master_store[rd] = pipeline_obj.cycle+3
                
            pipeline_obj.pipeline[pipeline_obj.cycle+1].insert(index,"E") # Execute this instruction in the next cycle at the same index
            return

    else:
        buffers[1].rs1 = rs1 # THESE ARE JUST ADDRESSES NOT VALUES
        buffers[1].rs2 = rs2
        buffers[1].rd  = rd 

        if(mneumonic == 'beq' or mneumonic == 'bge' or mneumonic == 'bne' or mneumonic == 'blt' or mneumonic == 'jalr'):
            if rs1:
                buffers[1].operand1 = buffers[0].operand1 # setting value of rs1 in buffer
            if rs2:
                buffers[1].operand2 = buffers[0].operand2 # setting value of rs2 in buffer 
        else:   
            if rs1:
                buffers[1].operand1 = registers.__regs[rs1] # setting value of rs1 in buffer
            if rs2:
                buffers[1].operand2 = registers.__regs[rs2] # setting value of rs2 in buffer

        if imm:
            buffers[1].imm = imm # setting immediate in buffer
            
        buffers[1].mne = mneumonic
        buffers[1].fmt = fmt

        if(pipeline_obj.forw_d["MES"][0] == 1):
            data_forw(2, pipeline_obj.forw_d["MES"][1], buffers)
            pipeline_obj.forw_d["MES"][0] = 0
            pipeline_obj.forw_d["MES"][1] = None
            pipeline_obj.pipeline[pipeline_obj.cycle+1].insert(index,"E")
            return
        
        # here code to check for data_hazard using HDU unit
        # if there is data hazard then:
        if(fmt != 4 and mneumonic != 'jalr'):
            HDU(buffers, 1, pipeline_obj.prevInsList, pipeline_obj.forw_d)
        if (pipeline_obj.forw_d["ME"][0] == 1):
            data_forw(2, pipeline_obj.forw_d["ME"][1], buffers)
            pipeline_obj.forw_d["ME"][0] = 0
            pipeline_obj.forw_d["ME"][1] = None
        if (pipeline_obj.forw_d["EE"][0] == 1):
            data_forw(1, pipeline_obj.forw_d["EE"][1], buffers)
            pipeline_obj.forw_d["EE"][0] = 0
            pipeline_obj.forw_d["EE"][1] = None
        if (pipeline_obj.forw_d["MES"][0] == 1):
            pipeline_obj.call_stalling(index)
            return
        
        pipeline_obj.pipeline[pipeline_obj.cycle+1].insert(index,"E")
        return
