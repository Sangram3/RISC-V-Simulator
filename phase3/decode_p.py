from data_forw import *
from HDU import *


#decode function
#all extractions and decode done in string format and at the end converted everything to decimal, example rs1 = '00110' then rs1 becomes 6 at the end.
from collections import defaultdict

def bin32(num):
    return '{0:032b}'.format(num)


def bin_to_dec(s): # input in two's compliment form
    if s[0] == '1':
        return -1 * (int(''.join('1' if x == '0' else '0' for x in s), 2) + 1)
    else:
        return int(s, 2)  


                          # extra arguments
def decode_p(memory, registers ,pipeline_obj ,buffers , index, btb, gui_util_obj):
    d = defaultdict(lambda: None)
    d = {'0110011': 1, '0010011': 2, '0000011': 2, '1100111': 2, '0100011': 3, '1100011': 4, '0010111': 5, '0110111': 5, '1101111': 6}

    xvar = 0

    inst = None
    op = None
    func3 = None
    func7 = None
    rd = -3
    rs1 = -1
    rs2 = -2
    imm = None
    fmt = None
    mneumonic = None
    PC = buffers[0].PC
    buffers[1].PC = buffers[0].PC

    inst = buffers[0].IR # instruction inside the F-D buffer
    inst = bin32(int(inst,16))
    #opcode extraction
    op = inst[25:]
    #fmt check
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

    
    ins = mneumonic
    
    op = int(op, base=2)
    if func3:
        func3 = int(func3, base=2)
    if func7:
        func7 = int(func7, base=2)
    if rd != -3:
        rd = int(rd, base=2)
    if rs1 != -1:
        rs1 = int(rs1, base=2)
    if rs2 != -2:
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

    # print("mne", mneumonic)

    if pipeline_obj.data_forwarding_knob == 0:
        dh = pipeline_obj.check_data_hazard(rs1,rs2)
        # print(rs1,rs2," rs1 rs2")
        if dh == 1:
            gui_util_obj.data_hazards.update({index:pipeline_obj.cycle })
            # print(pipeline_obj.master_store)
            pipeline_obj.call_stalling(index) # index is the at what index this instruction is present in the cycle
                                              # like ["E" ,"D" ] index of decode in this case is 1
            return
        else:
            pipeline_obj.disable_PC = 0
            # buffers[1] = D-E BUFFER
            
            buffers[1].rs1 = rs1 # THESE ARE JUST ADDRESSES NOT VALUES
            buffers[1].rs2 = rs2
            buffers[1].rd  = rd 
            
            if rs1 != -1:
                buffers[1].operand1 = registers.load_reg(rs1) # setting value of rs1 in buffer
            if rs2 != -2:
                buffers[1].operand2 = registers.load_reg(rs2) # setting value of rs2 in buffer
            if imm != None:
                buffers[1].imm = imm # setting immediate in buffer
            # print(buffers[1].imm,buffers[1].operand1,buffers[1].operand2," operands") 
            
            buffers[1].mne = mneumonic
            buffers[1].fmt = fmt
            # UPDATE MASTER_STORE
            if rd:
                pipeline_obj.master_store[rd] = pipeline_obj.cycle+3
            
########################## COMPARATOR ###########################################################
            if op == 99: # SB : beq, bne, bge, blt 
                imm = bin_to_dec(imm)*2
                
                # if imm<0:
                #     imm//=2
                taken = 0
                if ins =='beq':
                    # print("operand ",buffers[1].operand1,buffers[1].operand2)
                    # print("\nbeq",buffers[1].operand1,buffers[1].operand2,buffers[1].rs1,buffers[1].rs2)
                    if buffers[1].operand1 == buffers[1].operand2:
                        taken = 1
                        
                if ins == 'bne':
                    if buffers[1].operand1 != buffers[1].operand2:
                        taken = 1 
                            
                if ins =='bge':
                    if buffers[1].operand1 >= buffers[1].operand2:
                        taken = 1
                            
                if ins == 'blt':
                    if buffers[1].operand1 < buffers[1].operand2:
                        taken = 1
                        
                if taken == 1: # taken 
                    # print("              shayad",PC,buffers[1].operand1,buffers[1].operand2,buffers[1].rs1,buffers[1].rs2)
                    # registers.add_PC(imm-4) # update PC here don't do it in execute
                    if btb.ifPresent(PC) == False: 
                        registers.add_PC(imm-4) # update PC here don't do it in execute
         # btb does not contain this instruction it means
         # guaranteed wrong instructions are fetched-> we need to flush
            
                        btb.newKey(PC,registers.get_PC(),0)
                        pipeline_obj.flush()
                    else:
                        if btb.prediction(PC) == False:
                    # again this PC was present but
                    # prediction made by BTB was wrong so need to flush
                            pipeline_obj.flush()
                            registers.update_PC(btb.getTarget(PC))
                    
                    
                elif taken == 0: # not taken
                     if btb.ifPresent(PC) == False: 
                        # btb does not contain this instruction so need to update BTB
                        btb.newKey(PC,registers.get_PC()+imm - 4,0)
                     else:
                         if btb.prediction(PC) == True:
                         # again this PC was present but prediction made by BTB was wrong so need to flush
                             pipeline_obj.flush()
                        
                        
            elif ins == 'jal' :# jal
                imm = bin_to_dec(imm)
                imm=imm*2   #omit imm[0]
                PC_var = registers.get_PC()+imm-4
                # registers.add_PC(imm-4)
                if btb.ifPresent(PC) == False:
                    # btb.newKey(PC,registers.get_PC(),1)
                    btb.newKey(PC,PC_var,1)
                    registers.update_PC(PC_var)
                    # as always wrong PC is fetched in the subsequent cycles need to flush
                    pipeline_obj.npred = pipeline_obj.npred+1
                    pipeline_obj.flush()  
                else:
                    # if it is already present in the BTB accurate
                    # prediction was made in FETCH STAGE
                    # no need to flush
                    pass
                
            elif ins == 'jalr':# jalr
                imm = bin_to_dec(imm)
                # ry = registers.get_PC()
                rs1 = buffers[1].operand1
                registers.add_PC(rs1+imm-registers.get_PC())
                
                if btb.ifPresent(PC) == False:
                    btb.newKey(PC, registers.get_PC() ,1)
                    pipeline_obj.flush()
                    
                else:
                    # if it is already present in the BTB accurate
                    # prediction was made in FETCH STAGE
                    # no need to flush
                    pass
                
######################## COMPARATOR END #########################################################
            pipeline_obj.pipeline[pipeline_obj.cycle+1].insert(index,"E") # Execute this instruction in the next cycle at the same index
            return

    else:
        buffers[1].rs1 = rs1 # THESE ARE JUST ADDRESSES NOT VALUES
        buffers[1].rs2 = rs2
        buffers[1].rd  = rd 

        if(fmt == 4 or mneumonic == 'jalr'):
            if rs1 != -1:
                buffers[0].operand1 = registers.load_reg(rs1) # setting value of rs1 in buffer
            if rs2 != -2:
                buffers[0].operand2 = registers.load_reg(rs2) # setting value of rs2 in buffer
        else:
            if rs1 != -1:
                buffers[1].operand1 = registers.load_reg(rs1) # setting value of rs1 in buffer
            if rs2 != -2:
                buffers[1].operand2 = registers.load_reg(rs2) # setting value of rs2 in buffer

        if imm:
            buffers[1].imm = imm # setting immediate in buffer
            
        buffers[1].mne = mneumonic
        buffers[1].fmt = fmt

        if(pipeline_obj.forw_d["MDSS"][0] == 2):
            pipeline_obj.forw_d["MDSS"][0] = 1
            pipeline_obj.call_stalling(index)
            return
        
        if(pipeline_obj.forw_d["MDSS"][0] == 1 ):
            data_forw(5, pipeline_obj.forw_d["MDSS"][1], buffers)
            pipeline_obj.forw_d["MDSS"][0] = 0
            pipeline_obj.forw_d["MDSS"][1] = None
            pipeline_obj.disable_PC = 0
            xvar = 1

        if(pipeline_obj.forw_d["MDS"][0] == 1 ):
            data_forw(5, pipeline_obj.forw_d["MDS"][1], buffers)
            pipeline_obj.forw_d["MDS"][0] = 0
            pipeline_obj.forw_d["MDS"][1] = None
            pipeline_obj.disable_PC = 0
            xvar = 1

        if(pipeline_obj.forw_d["EDS"][0] == 1):
            if(pipeline_obj.forw_d["MD"][0] == 1):
                data_forw(5, pipeline_obj.forw_d["MD"][1], buffers)
                pipeline_obj.forw_d["MD"][0] = 0
                pipeline_obj.forw_d["MD"][1] = None
            data_forw(4, pipeline_obj.forw_d["EDS"][1], buffers)
            pipeline_obj.forw_d["EDS"][0] = 0
            pipeline_obj.forw_d["EDS"][1] = None
            pipeline_obj.disable_PC = 0
            xvar = 1

        if(pipeline_obj.forw_d["MES"][0] == 1):
            data_forw(2, pipeline_obj.forw_d["MES"][1], buffers)
            pipeline_obj.forw_d["MES"][0] = 0
            pipeline_obj.forw_d["MES"][1] = None
            pipeline_obj.disable_PC = 0
            pipeline_obj.pipeline[pipeline_obj.cycle+1].insert(index,"E")
            return
        
        # here code to check for data_hazard using HDU unit
        # if there is data hazard then:
        if(xvar == 0):
            HDU(buffers, 1, pipeline_obj.prevInsList, pipeline_obj.forw_d, pipeline_obj)
            #print(pipeline_obj.forw_d)
            temp = []
            for k,v in pipeline_obj.forw_d.items():
                if v[0] == 1:
                    temp.append(k)
            if(len(temp) > 0):
                gui_util_obj.data_path_taken[pipeline_obj.n_inst] = temp
            else:
                gui_util_obj.data_path_taken[pipeline_obj.n_inst] = -1
            if(len(temp) > 0):
                gui_util_obj.data_hazards.update({index :pipeline_obj.cycle  })
                                                
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
            if(pipeline_obj.forw_d["MDSS"][0] == 2 or pipeline_obj.forw_d["MDS"][0] == 1 or pipeline_obj.forw_d["EDS"][0] == 1):
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
        
        #change1
       
        # add_comparator here
        if op == 99: # SB : beq, bne, bge, blt 
                imm = bin_to_dec(imm)*2
                
                # if imm<0:
                #     imm//=2
                taken = 0
                if ins =='beq':
                    # print("operand ",buffers[1].operand1,buffers[1].operand2)
                    # print("\nbeq",buffers[1].operand1,buffers[1].operand2,buffers[1].rs1,buffers[1].rs2)
                    if buffers[0].operand1 == buffers[0].operand2:
                        taken = 1
                        
                if ins == 'bne':
                    if buffers[0].operand1 != buffers[0].operand2:
                        taken = 1 
                            
                if ins =='bge':
                    if buffers[0].operand1 >= buffers[0].operand2:
                        taken = 1
                            
                if ins == 'blt':
                    if buffers[0].operand1 < buffers[0].operand2:
                        taken = 1
                        
                if taken == 1: # taken 
                    # print("              shayad",PC,buffers[1].operand1,buffers[1].operand2,buffers[1].rs1,buffers[1].rs2)
                    # registers.add_PC(imm-4) # update PC here don't do it in execute
                    if btb.ifPresent(PC) == False: 
                        registers.add_PC(imm-4) # update PC here don't do it in execute
         # btb does not contain this instruction it means
         # guaranteed wrong instructions are fetched-> we need to flush
            
                        btb.newKey(PC,registers.get_PC(),0)
                        pipeline_obj.npred = pipeline_obj.npred+1
                        pipeline_obj.flush()
                    else:
                        if btb.prediction(PC) == False:
                    # again this PC was present but
                    # prediction made by BTB was wrong so need to flush
                            pipeline_obj.npred = pipeline_obj.npred+1
                            pipeline_obj.flush()
                            registers.update_PC(btb.getTarget(PC))
                    
                    
                elif taken == 0: # not taken
                     if btb.ifPresent(PC) == False: 
                        # btb does not contain this instruction so need to update BTB
                        btb.newKey(PC,registers.get_PC()+imm - 4,0)
                     else:
                         if btb.prediction(PC) == True:
                         # again this PC was present but prediction made by BTB was wrong so need to flush
                             pipeline_obj.npred = pipeline_obj.npred+1
                             pipeline_obj.flush()
                        
                        
        elif ins == 'jal' :# jal
            imm = bin_to_dec(imm)
            imm=imm*2   #omit imm[0]
            PC_var = registers.get_PC()+imm-4
            # registers.add_PC(imm-4)
            if btb.ifPresent(PC) == False:
                # btb.newKey(PC,registers.get_PC(),1)
                btb.newKey(PC,PC_var,1)
                registers.update_PC(PC_var)
                # as always wrong PC is fetched in the subsequent cycles need to flush
                pipeline_obj.npred = pipeline_obj.npred+1
                pipeline_obj.flush()  
            else:
                # if it is already present in the BTB accurate
                # prediction was made in FETCH STAGE
                # no need to flush
                pass
            
        elif ins == 'jalr':# jalr
            imm = bin_to_dec(imm)
            # ry = registers.get_PC()
            rs1 = buffers[0].operand1
            PC_var = rs1+imm
            # registers.add_PC(rs1+imm-registers.get_PC())
            
            if btb.ifPresent(PC) == False:
                # btb.newKey(PC, registers.get_PC() ,1)
                btb.newKey(PC, PC_var ,1)
                registers.update_PC(PC_var)
                pipeline_obj.npred = pipeline_obj.npred+1
                pipeline_obj.flush()
                
            else:
                # if it is already present in the BTB accurate
                # prediction was made in FETCH STAGE
                # no need to flush
                pass
        
        
        pipeline_obj.pipeline[pipeline_obj.cycle+1].insert(index,"E")
        return
