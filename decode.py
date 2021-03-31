#decode function
#all extractions and decode done in string format and at the end converted everything to decimal, example rs1 = '00110' then rs1 becomes 6 at the end.
from collections import defaultdict

def bin32(num):
    return '{0:032b}'.format(num)

def decode(ins):
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

    inst = ins
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

    list = [rs1, rs2, rd, imm]
   
    #below code is for checking code    

    print("op: ",op)
    print("fmt: ",fmt)
    print("func3: ",func3)
    print("func7: ",func7)
    print("rd: ",rd)
    print("rs1: ",rs1)
    print("rs2: ",rs2)
    
    return (fmt, mneumonic, list)
        
    #format of input for decode function = decode('00000001010110100000010010110011')


decode(bin32(0x00A37293))
