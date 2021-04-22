def Twos_to_dec(hex):
    return -(2**((len(hex)-2)*4) - int(hex, 16))

def mem(mem_obj, reg_obj, buffers):   #data in hex with 0x 

    # copying all the values of buffer between execute and memory to buffer between memory and execute stages so that the required information for the instruction which is in memory stage in this cycle and will go to writeback stage in next cycle gets passed
    buffers[3].RZ = buffers[2].RZ   #Output of the ALU. It can be used in data forwarding.
    buffers[3].RY = buffers[2].RY   #The value which is to be written in the writeback stage.
    buffers[3].rs1 = buffers[2].rs1  
    buffers[3].rs2 = buffers[2].rs2 
    buffers[3].rd = buffers[2].rd 
    buffers[3].mne = buffers[2].mne

    x = 0
    if(buffers[2].mne == "sw"):
        # sw
        mem_obj.sw(buffers[2].MAR, hex(buffers[2].RM))  

    elif(buffers[2].mne == "sh"):
        # sh
        mem_obj.sh(buffers[2].MAR, hex(buffers[2].RM))

    elif(buffers[2].mne == "sb"):
        # sb
        mem_obj.sb(buffers[2].MAR, hex(buffers[2].RM))

    elif(buffers[2].mne == "lw"):
        # lw    
        x = mem_obj.lw(buffers[2].MAR)
        if(int(x[2],16) > 7):
            x = Twos_to_dec(x)
        else:
            x = int(x, 16)
        buffers[3].RY = x   
        buffers[3].MDR = x

    elif(buffers[2].mne == "lh"):
        # lh
        x = mem_obj.lh(buffers[2].MAR)
        if(int(x[2],16) > 7):
            x = Twos_to_dec(x)
        else:
            x = int(x, 16)
        buffers[3].RY = x   
        buffers[3].MDR = x

    elif(buffers[2].mne == "lb"):
        #lb
        x = mem_obj.lb(buffers[2].MAR)
        if(int(x[2],16) > 7):
            x = Twos_to_dec(x)
        else:
            x = int(x, 16)
        buffers[3].RY = x   
        buffers[3].MDR = x
