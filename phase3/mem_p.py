def Twos_to_dec(hex):
    return -(2**((len(hex)-2)*4) - int(hex, 16))

def mem_p(mem_obj, reg_obj, buffers, index, pipeline_obj, cache_ob, gui_util_obj):   #data in hex with 0x 

    buffers[3].RB = buffers[3].RY

    buffers[3].RZ = buffers[2].RZ   #Output of the ALU. It can be used in data forwarding.
    buffers[3].RM = buffers[2].RM   #It has the value for the store ins. This is forwarded to MDR in stage 4(memory access).
    buffers[3].RY = buffers[2].RY   #The value which is to be written in the writeback stage.
    buffers[3].rs1 = buffers[2].rs1  
    buffers[3].rs2 = buffers[2].rs2 
    buffers[3].rd = buffers[2].rd
    buffers[3].MAR = buffers[2].MAR
    buffers[3].MDR = buffers[2].MDR
    buffers[3].operand1 = buffers[2].operand1
    buffers[3].operand2 = buffers[2].operand2
    buffers[3].fmt = buffers[2].fmt
    buffers[3].mne = buffers[2].mne

    x = 0
    if(buffers[2].mne == "sw"):
        # sw
        cache_ob.storedata(hex(buffers[2].MAR), hex(buffers[2].RM))
        mem_obj.sw(buffers[2].MAR, hex(buffers[2].RM))


        tag, set_no, bo = cache_ob.decode_address(hex(buffers[2].MAR))
        h, bno = cache_ob.hit_miss(tag, set_no)

        if(h == True):
            copy_set = cache_ob.cache_array[set_no][:]
            temp = ["Store", hex(buffers[2].MAR), set_no, copy_set]
            tag = None
            set_no = None
            bo = None
            gui_util_obj.task2.append(temp)
            temp = []
         

    elif(buffers[2].mne == "sh"):
        # sh
        cache_ob.storedata(hex(buffers[2].MAR), hex(buffers[2].RM))
        mem_obj.sh(buffers[2].MAR, hex(buffers[2].RM))

        tag, set_no, bo = cache_ob.decode_address(hex(buffers[2].MAR))
        h, bno = cache_ob.hit_miss(tag, set_no)

        if(h == True):
            copy_set = cache_ob.cache_array[set_no][:]
            temp = ["Store", hex(buffers[2].MAR), set_no, copy_set]
            tag = None
            set_no = None
            bo = None
            gui_util_obj.task2.append(temp)
            temp = []

    elif(buffers[2].mne == "sb"):
        # sb
        cache_ob.storedata(hex(buffers[2].MAR), hex(buffers[2].RM))
        mem_obj.sb(buffers[2].MAR, hex(buffers[2].RM))

        tag, set_no, bo = cache_ob.decode_address(hex(buffers[2].MAR))
        h, bno = cache_ob.hit_miss(tag, set_no)

        if(h == True):
            copy_set = cache_ob.cache_array[set_no][:]
            temp = ["Store", hex(buffers[2].MAR), set_no, copy_set]
            tag = None
            set_no = None
            bo = None
            gui_util_obj.task2.append(temp)
            temp = []

    elif(buffers[2].mne == "lw"):
        # lw  
        x = cache_ob.read(hex(buffers[2].MAR), mem_obj, "Load", gui_util_obj)
        
        tag, set_no, bo = cache_ob.decode_address(hex(buffers[2].MAR))
        copy_set = cache_ob.cache_array[set_no][:]
        temp = ["Load", hex(buffers[2].MAR), set_no, copy_set]
        tag = None
        set_no = None
        bo = None
        gui_util_obj.task2.append(temp)
        temp = []

        if(int(x[2],16) > 7):
            x = Twos_to_dec(x)
        else:
            x = int(x, 16)
        buffers[3].RY = x   
        buffers[3].MDR = x

    elif(buffers[2].mne == "lh"):
        # lh
        x = cache_ob.read(hex(buffers[2].MAR), mem_obj, "Load", gui_util_obj)
        tag, set_no, bo = cache_ob.decode_address(hex(buffers[2].MAR))
        copy_set = cache_ob.cache_array[set_no][:]
        temp = ["Load", hex(buffers[2].MAR), set_no, copy_set]
        tag = None
        set_no = None
        bo = None
        gui_util_obj.task2.append(temp)
        temp = []

        if(int(x[2],16) > 7):
            x = Twos_to_dec(x)
        else:
            x = int(x, 16)
        buffers[3].RY = x   
        buffers[3].MDR = x

    elif(buffers[2].mne == "lb"):
        #lb
        x = cache_ob.read(hex(buffers[2].MAR), mem_obj, "Load", gui_util_obj)
        
        tag, set_no, bo = cache_ob.decode_address(hex(buffers[2].MAR))
        copy_set = cache_ob.cache_array[set_no][:]
        temp = ["Load", hex(buffers[2].MAR), set_no, copy_set]
        tag = None
        set_no = None
        bo = None
        gui_util_obj.task2.append(temp)
        temp = []

        if(int(x[2],16) > 7):
            x = Twos_to_dec(x)
        else:
            x = int(x, 16)
        buffers[3].RY = x   
        buffers[3].MDR = x

    pipeline_obj.pipeline[pipeline_obj.cycle+1].insert(index,"W")
