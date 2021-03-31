#decode function
#all extractions and decode done in string format and at the end converted everything to decimal, example rs1 = '00110' then rs1 becomes 6 at the end.
from collections import defaultdict

def bin32(num):
    return '{0:032b}'.format(num)

def decode(ins):
    d = defaultdict(lambda: None)
    d = {'0110011': ['R', '000', '0000000', 'add']  ,'0000011' : ['I', " for lb,lw,lh,ld "],'0010011' : ['I',"for addi andi ori "] ,'0100011':['S'],'1100111' : ['I',"for jalr"] ,'1101111' : ['UJ'] ,'1100011' : ['SB']}

    inst = None
    op = None
    func3 = None
    func7 = None
    rd = None
    rs1 = None
    rs2 = None
    imm = None
    fmt = None
    pne = None

    inst = ins
    op = inst[25:]
    fmt = (d[op])[0]

    if (fmt != 'U' and fmt != 'UJ'):
        func3 = inst[17:20]

    if(fmt == 'R'):
        func7 = inst[0:7]

    if(fmt == 'R' or fmt == 'I' or 'S' or 'SB'):
        rs1 = inst[12:17]

    if(fmt == 'R' or fmt == 'S' or fmt == 'SB'):
        rs2 = inst[7:12]

    if(fmt == 'R' or fmt == 'I' or fmt == 'U' or fmt =='UJ'):
        rd = inst[20:25]

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
        
    #below code is for checking code    

    print("op: ",op)
    print("fmt: ",fmt)
    print("func3: ",func3)
    print("func7: ",func7)
    print("rd: ",rd)
    print("rs1: ",rs1)
    print("rs2: ",rs2)
    
    
    


decode(bin32(0x00A37293))
