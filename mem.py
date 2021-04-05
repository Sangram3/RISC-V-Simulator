def dec_to_2s(data, digits):
    return (hex(2**(digits*4) - data))

def Twos_to_dec(hex):
    return -(2**((len(hex)-2)*4) - int(hex, 16))



def mem(mem_control, mem_obj, reg_obj, add):   #data in hex with 0x 
    x = 0
    if(mem_control == 1):
        # sw
        mem_obj.sw(add, hex(reg_obj.load_reg(reg_obj.get_rs2())))
    elif(mem_control == 2):
        # sh
        mem_obj.sh(add, hex(reg_obj.load_reg(reg_obj.get_rs2())))
    elif(mem_control == 3):
        # sb
        mem_obj.sb(add, hex(reg_obj.load_reg(reg_obj.get_rs2())))   #args[0] is the data in hexwith 0x
    elif(mem_control == 4):
        # lw    
        x = mem_obj.lw(add)
        print(x)
        if(int(x[2],16) > 7):
            x = Twos_to_dec(x)
            print (x)
        else:
            x = int(x, 16)
    elif(mem_control == 5):
        # lh
        
        x = mem_obj.lh(add)
        print(x)
        if(int(x[2],16) > 7):
            x = Twos_to_dec(x)
            print (x)
        else:
            x = int(x, 16)
    elif(mem_control == 6):
        x = mem_obj.lb(add)
        print(x)
        if(int(x[2],16) > 7):
            x = Twos_to_dec(x)
            print (x)
        else:
            x = int(x, 16)  
    return x




