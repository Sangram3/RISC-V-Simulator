def sra(val, n): 
    return (val % 0x100000000) >> n

def output_message(fmt,inst,*args):
    pass

def bin_to_dec(s): # input in two's compliment form
    if s[0] == '1':
        return -1 * (int(''.join('1' if x == '0' else '0' for x in s), 2) + 1)
    else:
        return int(s, 2)
def execute(fmt,inst,im,registers, l):
    rs1 = None
    rs2 = None
    rd = None
    imm = None
    ry = None
    try:
        rs1 = registers.get_rs1()
        rs2 = registers.get_rs2()
        rd = registers.get_rd()
        imm = im
        rs1 = registers.load_reg(rs1)
        rs2 = registers.load_reg(rs2)
        
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
        return ry
            
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
            l.append("EXECUTE: OR " + str(rs1) + " and " + str(imm))
            
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
        
        if inst == 'jalr': # jalr
            ry = registers.get_PC()
            registers.add_PC(rs1+imm-registers.get_PC())
            l.append("EXECUTE: ADD " + str(rs1) + " and " + str(imm)  + " to calculate the effective PC.")

        if ry>2147483647 or ry<-2147483648:
            ry = 0

        return ry
    
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
        return rs1+imm
        
    elif fmt == 4: # SB : beq, bne, bge, blt 
        imm = bin_to_dec(imm)*2
        l.append("DECODE: Operation is " + inst.upper() + ", first operand x" + str(registers.get_rs1()) + ", second operand x" + str(registers.get_rs2()) + ", immediate value is " + str(imm)) 
        l.append("DECODE: Read registers x" + str(registers.get_rs1()) + " = " + str(rs1) + " x" + str(registers.get_rs2()) + " = " + str(rs2))
        
        if imm<0:
            imm//=2
        if imm<-2048  or imm>2047:
            raise ValueError("Immidiate {} out of range immidiate should be between -2048-2047".format(imm))
            return 
        if inst =='beq':
            if rs1 == rs2:
                registers.add_PC(imm-4)
                l.append("EXECUTE: " + str(rs1) + " equal to " + str(rs2)  + " to calculate the effective PC")       
                # PC = PC+imm-4
        if inst == 'bne':
            if rs1 != rs2:
                registers.add_PC(imm-4)
                l.append("EXECUTE: " + str(rs1) + " not equal to " + str(rs2)  + " to calculate the effective PC")   
                # PC = PC+imm-4
        if inst =='bge':
            if rs1 >= rs2:
                registers.add_PC(imm-4)
                l.append("EXECUTE: " + str(rs1) + " greater than or equal to " + str(rs2)  + " to calculate the effective PC")   
        if inst == 'blt':
            if rs1 < rs2:
                registers.add_PC(imm-4)
                l.append("EXECUTE: " + str(rs1) + " less than " + str(rs2)  + " to calculate the effective PC")   
                # PC = PC+imm-4
        
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
            ry = registers.get_PC()+ry-4
            l.append("EXECUTE: Shift left " + str(imm) + " by 12 bits and add with PC = " + str(hex(registers.get_PC())))
        # print(ry)
        
        return ry
    
    elif fmt == 6: #UJ : jal
        imm = bin_to_dec(imm)
        imm=imm*2   #omit imm[0]
        l.append("DECODE: Operation is " + inst.upper() + ", destination register x" + str(registers.get_rd()) + ", immediate value is " + str(imm))
        if imm<-1048576  or imm>1048574: 
            raise ValueError("Immidiate {} out of range immidiate should be between -1048576-1048574".format(imm))
            return
        ry=registers.get_PC()
        k = registers.get_PC() - 4
        l.append("EXECUTE: Add " + str(imm) + "  to the PC = " + str(hex(k)))
        registers.add_PC(imm-4)
        return ry
        

    return "No return type"
