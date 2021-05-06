def dec_to_2s(data, digits):
    return (hex(2**(digits*4) - data))

def Twos_to_dec(hex):
    return -(2**((len(hex)-2)*4) - int(hex, 16))



def mem(mem_control, mem_obj, reg_obj, add, l, cache_ob, gui_util_obj):   #data in hex with 0x 
    x = 0
    if(mem_control == 1):
        # sw
        cache_ob.storedata(hex(add), hex(reg_obj.load_reg(reg_obj.get_rs2())))
        mem_obj.sw(add, hex(reg_obj.load_reg(reg_obj.get_rs2())))

        tag, set_no, bo = cache_ob.decode_address(hex(add))
        h, bno = cache_ob.hit_miss(tag, set_no)

        if(h == True):
            copy_set = cache_ob.cache_array[set_no][:]
            temp = ["Store", hex(add), set_no, copy_set]
            tag = None
            set_no = None
            bo = None
            gui_util_obj.task2.append(temp)
            temp = []

        l.append("MEMORY : Store word " + str(hex(reg_obj.load_reg(reg_obj.get_rs2()))) + " in " + str(add))  

    elif(mem_control == 2):
        # sh
        cache_ob.storedata(hex(add), hex(reg_obj.load_reg(reg_obj.get_rs2())))
        mem_obj.sh(add, hex(reg_obj.load_reg(reg_obj.get_rs2())))

        tag, set_no, bo = cache_ob.decode_address(hex(add))
        h, bno = cache_ob.hit_miss(tag, set_no)

        if(h == True):
            copy_set = cache_ob.cache_array[set_no][:]
            temp = ["Store", hex(add), set_no, copy_set]
            tag = None
            set_no = None
            bo = None
            gui_util_obj.task2.append(temp)
            temp = []

        l.append("MEMORY : Store half word " + str(hex(reg_obj.load_reg(reg_obj.get_rs2()))) + " in " + str(add))

    elif(mem_control == 3):
        # sb
        cache_ob.storedata(hex(add), hex(reg_obj.load_reg(reg_obj.get_rs2())))
        mem_obj.sb(add, hex(reg_obj.load_reg(reg_obj.get_rs2())))   #args[0] is the data in hexwith 0x

        tag, set_no, bo = cache_ob.decode_address(hex(add))
        h, bno = cache_ob.hit_miss(tag, set_no)

        if(h == True):
            copy_set = cache_ob.cache_array[set_no][:]
            temp = ["Store", hex(add), set_no, copy_set]
            tag = None
            set_no = None
            bo = None
            gui_util_obj.task2.append(temp)
            temp = []

        l.append("MEMORY : Store byte " + str(hex(reg_obj.load_reg(reg_obj.get_rs2()))) + " in " + str(add))

    elif(mem_control == 4):
        # lw   
        x = cache_ob.read(hex(add), mem_obj, "Load", gui_util_obj) 
        
        tag, set_no, bo = cache_ob.decode_address(hex(add))
        copy_set = cache_ob.cache_array[set_no][:]
        temp = ["Load", hex(add), set_no, copy_set]
        tag = None
        set_no = None
        bo = None
        gui_util_obj.task2.append(temp)
        temp = []

        if(int(x[2],16) > 7):
            x = Twos_to_dec(x)
            # print (x)
        else:
            x = int(x, 16)
        l.append("MEMORY : Load word " + str(hex(x)) + " at " + str(add))   

    elif(mem_control == 5):
        # lh
        x = cache_ob.read(hex(add), mem_obj, "Load", gui_util_obj) 
        
        tag, set_no, bo = cache_ob.decode_address(hex(add))
        copy_set = cache_ob.cache_array[set_no][:]
        temp = ["Load", hex(add), set_no, copy_set]
        tag = None
        set_no = None
        bo = None
        gui_util_obj.task2.append(temp)
        temp = []

        if(int(x[2],16) > 7):
            x = Twos_to_dec(x)
            # print (x)
        else:
            x = int(x, 16)
        l.append("MEMORY : Load half word " + str(hex(x)) + " at " + str(add))

    elif(mem_control == 6):
        x = cache_ob.read(hex(add), mem_obj, "Load", gui_util_obj) 
        
        tag, set_no, bo = cache_ob.decode_address(hex(add))
        copy_set = cache_ob.cache_array[set_no][:]
        temp = ["Load", hex(add), set_no, copy_set]
        tag = None
        set_no = None
        bo = None
        gui_util_obj.task2.append(temp)
        temp = []
        
        if(int(x[2],16) > 7):
            x = Twos_to_dec(x)
            # print (x)
        else:
            x = int(x, 16)
        l.append("MEMORY : Load byte " + str(hex(x)) + " at " + str(add)) 

    else:
        l.append("MEMORY : No memory operation")         
    return x
