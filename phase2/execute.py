from data_forw import *
def sra(val, n): 
    return (val % 0x100000000) >> n

def output_message(fmt,inst,*args):
    pass

def bin_to_dec(s): # input in two's compliment form
    if s[0] == '1':
        return -1 * (int(''.join('1' if x == '0' else '0' for x in s), 2) + 1)
    else:
        return int(s, 2)    
                                      
def execute(registers, pipeline_obj,buffers,index ):
    # print("execute calling",index)
    buffers[2].RA = buffers[2].RZ
    l=[]
    fmt = buffers[1].fmt
    inst = buffers[1].mne
    im = buffers[1].imm
    buffers[2].mne = buffers[1].mne
    buffers[2].fmt = buffers[1].fmt
    rs1 = None
    rs2 = None
    rd = None
    imm = None
    ry = None
    try:
        rs1 = buffers[1].operand1
        rs2 = buffers[1].operand2
        rd =  buffers[1].rd
        imm = buffers[1].imm
        
    except:
        pass

    
    if fmt == 1: #R
        if inst == 'add': # add
            ry = rs1+rs2
            
        if inst == 'sub': # sub
            ry  = rs1-rs2
            
        if inst == 'mul': # mul
            ry = rs1*rs2
            
        if inst == 'div' : # div
            if rs2 == 0:
                ry = 0
            else:
                ry = rs1//rs2
            
        if inst == 'xor': # xor
            ry  = rs1^rs2
            
        if inst == 'or': # or
            ry = rs1|rs2
            
        if inst == 'rem': # rem
            if rs2 == 0:
                ry = 0
            else:
                ry =  rs1%rs2
            
        if inst == 'srl': # srl
            if rs2<0:
                ry = 0
            else:
                ry =  rs1>>rs2
            
        if inst == 'sll':# sll
            if rs2 <0:
                ry = 0
            else:
                ry =  rs1<<rs2
            
        if inst == 'sra': #sra
            if rs2<0:
                ry = 0
            else:
                ry= sra(rs1,rs2)
            
        if inst == 'slt': # slt
            ry =  int(rs1<rs2)
        if inst == 'and': # and
            ry =  rs1&rs2
        if ry>2147483647 or ry<-2147483648:
            ry = 0

        l.append("DECODE: Operation is " + inst.upper() + ", first operand x" + str(registers.get_rs1()) + ", second operand x" + str(registers.get_rs2()) + ", destination register x" + str(registers.get_rd())) 
        l.append("DECODE: Read registers x" + str(registers.get_rs1()) + " = " + str(rs1) + ", " + str(registers.get_rs2()) + " = " + str(rs2)) 
        l.append("EXECUTE: " + inst.upper() + " " + str(rs1) + " and " + str(rs2))
        # return ry
           
    elif fmt == 2: #I : addi, andi, ori, lb, lh, lw, jalr
        imm = bin_to_dec(imm)
        l.append("DECODE: Operation is " + inst.upper() + ", first operand x" + str(registers.get_rs1()) + ", destination register x" + str(registers.get_rd()) + ", immediate value is " + str(imm)) 
        l.append("DECODE: Read registers x" + str(registers.get_rs1()) + " = " + str(rs1)) 

        if imm<-2048  or imm>2047: 
            raise ValueError("Immidiate {} out of range immidiate should be between -2048-2047".format(imm))
            return

        if inst == 'addi' : # addi
            ry =  rs1+imm
            l.append("EXECUTE: ADD " + str(rs1) + " and " + str(imm))

        if inst == 'ori': # ori
            ry =  rs1|imm
            l.append("EXECUTE: OR " +str(rs1) + " and " + str(imm))
            
        if  inst == 'andi': # andi
            ry =  rs1&imm
            l.append("EXECUTE: AND " + str(rs1) + " and " + str(imm))

        if inst == 'lb': # lb
            ry =  rs1+imm
            l.append("EXECUTE: ADD " + str(rs1) + " and " + str(imm)  + " to calculate the effective address.")
        
        if inst == 'lh': # lh
            ry =  rs1+imm
            l.append("EXECUTE: ADD " + str(rs1) + " and " + str(imm)  + " to calculate the effective address.")

        if inst == 'lw': # lw
            ry =  rs1+imm
            l.append("EXECUTE: ADD " + str(rs1) + " and " + str(imm) + " to calculate the effective address.")
        

        if ry>2147483647 or ry<-2147483648:
            ry = 0

        # return ry
    
    elif fmt == 3: # S : sb, sw, sh
        imm = bin_to_dec(imm)
        l.append("DECODE: Operation is " + inst.upper() + ", first operand x" + str(registers.get_rs1()) + ", destination register x" + str(registers.get_rd()) + ", immediate value is " + str(imm)) 
        l.append("DECODE: Read registers x" + str(registers.get_rs1()) + " = " + str(rs1) + " x" + str(registers.get_rd()) + " = " + str(rd))

        if imm<0:
            imm//=2
        if imm<-2048  or imm>2047:
            raise ValueError("Immidiate {} out of range immidiate should be between -2048-2047".format(imm))
            return 

        l.append("EXECUTE: ADD " + str(rs1) + " and " + str(imm)  + " to calculate the effective address.")
        ry = rs1+imm

        
    elif fmt == 5: # U : auipc, lui
        imm = bin_to_dec(imm)
        l.append("DECODE: Operation is " + inst.upper() + ", destination register x" + str(registers.get_rd()) + ", immediate value is " + str(imm))
        if imm<-524288  or imm>524287: 
            raise ValueError("Immidiate {} out of range immidiate should be between -524288-524287".format(imm))
            return
        if(inst == 'lui'):
            ry = imm*4096
            l.append("EXECUTE: Shift left " + str(imm) + " by 12 bits")
        if(inst == 'auipc'):
            ry = imm*4096
            ry = buffers[1].PC+ry
            l.append("EXECUTE: Shift left " + str(imm) + " by 12 bits and add with PC = " + str(hex(registers.get_PC())))
        # print(ry)
        
        #return ry
    
  
  
    
        
    if ry!= None:
        buffers[2].RZ = ry
        buffers[2].RY = ry
        buffers[2].rd = rd
        if(inst=="sw" or inst=="sh" or inst =="sb" or inst == 'lw' or inst == 'lb' or inst == 'lh'):
            buffers[2].MAR = ry
        if(fmt == 3):
            buffers[2].RM = rs2

    if(pipeline_obj.forw_d["MM"][0] == 1 and pipeline_obj.data_forwarding_knob == 1):
        data_forw(3, pipeline_obj.forw_d["MM"][1], buffers)
        pipeline_obj.forw_d["MM"][0] = 0
        pipeline_obj.forw_d["MM"][1] = None
    
    pipeline_obj.pipeline[pipeline_obj.cycle+1].insert(index,"M")
