def control(decode_array):     #(fmt, mneumonic, imm)
    ins = decode_array[1]
    fmt = decode_array[0]
    l = [0,0]      #write_control, mem_control    # For b type ins
    if(fmt == 1):     #R ins
        l[0] = 1
    elif(fmt == 2):    #I type and load ins
        l[0] = 1
        if(ins == "lw"):
            l[1] = 4
        elif(ins == "lb"):
            l[1] = 6
        elif(ins == "lh"):
            l[1] = 5

    elif(fmt == 3):   #S ins
        if(ins == "sw"):
            l[1] = 1
        elif(ins == "sb"):
            l[1] = 3
        elif(ins == "sh"):
            l[1] = 2

    elif(fmt == 5 or fmt == 6):   #U ins    #UJ ins
        l[0] = 1

    return l    
                