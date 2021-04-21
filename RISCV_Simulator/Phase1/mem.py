def dec_to_2s(data, digits):
    return (hex(2**(digits*4) - data))

def Twos_to_dec(hex):
    return -(2**((len(hex)-2)*4) - int(hex, 16))



def mem(mem_control, mem_obj, reg_obj, add, l):   #data in hex with 0x 
    x = 0
    if(mem_control == 1):
        # sw
        mem_obj.sw(add, hex(reg_obj.load_reg(reg_obj.get_rs2())))
        l.append("MEMORY : Store word " + str(hex(reg_obj.load_reg(reg_obj.get_rs2()))) + " in " + str(add))  

    elif(mem_control == 2):
        # sh
        mem_obj.sh(add, hex(reg_obj.load_reg(reg_obj.get_rs2())))
        l.append("MEMORY : Store half word " + str(hex(reg_obj.load_reg(reg_obj.get_rs2()))) + " in " + str(add))

    elif(mem_control == 3):
        # sb
        mem_obj.sb(add, hex(reg_obj.load_reg(reg_obj.get_rs2())))   #args[0] is the data in hexwith 0x
        l.append("MEMORY : Store byte " + str(hex(reg_obj.load_reg(reg_obj.get_rs2()))) + " in " + str(add))

    elif(mem_control == 4):
        # lw    
        x = mem_obj.lw(add)
        # print(x)
        if(int(x[2],16) > 7):
            x = Twos_to_dec(x)
            # print (x)
        else:
            x = int(x, 16)
        l.append("MEMORY : Load word " + str(hex(x)) + " at " + str(add))   

    elif(mem_control == 5):
        # lh
        x = mem_obj.lh(add)
        # print(x)
        if(int(x[2],16) > 7):
            x = Twos_to_dec(x)
            # print (x)
        else:
            x = int(x, 16)
        l.append("MEMORY : Load half word " + str(hex(x)) + " at " + str(add))

    elif(mem_control == 6):
        x = mem_obj.lb(add)
        # print(x)
        if(int(x[2],16) > 7):
            x = Twos_to_dec(x)
            # print (x)
        else:
            x = int(x, 16)
        l.append("MEMORY : Load byte " + str(hex(x)) + " at " + str(add)) 

    else:
        l.append("MEMORY : No memory operation")         
    return x
