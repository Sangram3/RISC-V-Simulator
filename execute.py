# R format - add, and, or, sll, slt, sra, srl, sub, xor, mul, div, rem
# I format - addi, andi, ori, lb, ld, lh, lw, jalr
# S format - sb, sw, sd, sh
# SB format - beq, bne, bge, blt
# U format - auipc, lui
# UJ format - jal

def sra(val, n): 
    return (val % 0x100000000) >> n

def output_message(fmt,inst,*args):
    pass

def bin_to_dec(s): # input in two's compliment form
    if s[0] == '1':
        return -1 * (int(''.join('1' if x == '0' else '0' for x in s), 2) + 1)
    else:
        return int(s, 2)
def execute(fmt,inst,im,registers):
    PC = 0 #just for sake of convinience
    rs1 = None
    rs2 = None
    rd = None
    imm = None
    ry = None
    try:
        rs1 = registers.get_rs1();
        rs2 = registers.get_rs2();
        rd = registers.get_rd();
        imm = im
        rs1 = registers.load_reg(rs1)
        rs2 = registers.load_reg(rs2)
        
    except:
        pass
    if fmt == 1: #R
    #register update necessary
        if inst == 'add': # add
            ry = rs1+rs2
            
        if inst == 'sub': # sub
            ry  = rs1-rs2
            
        if inst == 'mul': # mul
            ry = rs1*rs2
            
        if inst == 'div' : # div
            ry = rs1//rs2
            
        if inst == 'xor': # xor
            ry  = rs1^rs2
            
        if inst == 'or': # or
            ry = rs1|rs2
            
        if inst == 'rem': # rem
            ry =  rs1%rs2
            
        if inst == 'srl': # srl
            ry =  rs1>>rs2
            
        if inst == 'sll':# sll
            ry =  rs1<<rs2
            
        if inst == 'sra': #sra
            ry= sra(rs1,rs2)
            
        if inst == 'slt': # slt
            ry =  rs1<rs2
        if inst == 'and': # and
            ry =  rs1&rs2
        if ry>2147483647 or ry<-2147483648:
            ry = 0
        return ry
            
    elif fmt == 2: #I : addi, andi, ori, lb, lh, lw, jalr
    #register/memory access necessary
        imm = bin_to_dec(imm)
        if imm<-2048  or imm>2047: 
            raise ValueError("Immidiate {} out of range immidiate should be between -2048-2047".format(imm))
            return
        if inst == 'addi' : # addi
            ry =  rs1+imm
            
        if inst == 'ori': # ori
            ry =  rs1|imm
            
        if  inst == 'andi': # andi
            ry =  rs1&imm
            
        if inst == 'lb': # lb
            ry =  rs1+imm
        
        if inst == 'lh': # lh
            ry =  rs1+imm
        
        if inst == 'lw': # lw
            ry =  rs1+imm
        
        if inst == 'jalr': # jalr
        #rd update necessary rd = PC+4
            PC = rs1+imm
            return 
        if ry>2147483647 or ry<-2147483648:
            ry = 0
        return ry
    
    elif fmt == 3: # S : sb, sw, sh
        imm = bin_to_dec(imm)*2
        if imm<0:
            imm//=2
        if imm<-2048  or imm>2047:
            raise ValueError("Immidiate {} out of range immidiate should be between -2048-2047".format(imm))
            return 
        
        return rs1+imm
        
    elif fmt == 4: # SB : beq, bne, bge, blt 
    #Memory access not necessary
        imm = bin_to_dec(imm)*2
        if imm<0:
            imm//=2
        if imm<-2048  or imm>2047:
            raise ValueError("Immidiate {} out of range immidiate should be between -2048-2047".format(imm))
            return 
        if inst =='beq':
            if rs1 == rs2:
                PC = PC+imm-4
        if inst == 'bne':
            if rs1 != rs2:
                PC = PC+imm-4
        if inst =='bge':
            if rs1 >= rs2:
                PC = PC+imm-4
        if inst == 'blt':
            if rs1 < rs2:
                PC = PC+imm-4
        
    elif fmt == 5: # U : auipc, lui
    #Memory access not necessary
        imm = bin_to_dec(imm)
        if imm<-524288  or imm>524287: 
            raise ValueError("Immidiate {} out of range immidiate should be between -524288-524287".format(imm))
            return
        if(inst == 'lui'):
            ry = imm*4096
        if(inst == 'auipc'):
            ry = imm*4096
            ry = PC+ry
        return ry
    
    elif fmt == 6: #UJ : jal
    
        imm = bin_to_dec(imm)
        imm=imm*2   #omit imm[0]
        if imm<-1048576  or imm>1048574: 
            raise ValueError("Immidiate {} out of range immidiate should be between -1048576-1048574".format(imm))
            return
        ry=PC
        PC=PC-4+imm 
        return ry
        
        
    output_message(fmt,inst,*args)
    return "No return type"
    
# print(execute(3, 'sw', [20, 12, None, '000000000001']))