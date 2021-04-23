def HDU(buffers, knob_forwarding, prevInsList, d):
    # d = {"EE": [0,0], "ME": [0,0], "MM": [0,0] "MES": [0,0], "ED": [0,0], "MD": [0,0], "EDS": [0,0], "MDS": [0,0]}
    dec_buf = buffers[1]
    prevInsList.append([dec_buf.fmt, dec_buf.mne, dec_buf.rs1, dec_buf.rs2, dec_buf.rd])
    this = prevInsList[-1]

    if(knob_forwarding == 1):  #with data forwaring there can be stalling
        if(this[0] == 5 or this[0] == 6):
            return

        if(this[0] == 4): #branch ins
            check_control_hazard(buffers, prevInsList, d)

        #M to M
        if(len(prevInsList) >=2 and (this[0] == 3 and (prevInsList[-2][0] == 1 or prevInsList[-2][0] == 2))): #store after Rtype/Itype/load/jalr  
            if(this[3] == prevInsList[-2][4]): #rs2 matches
                # d["MM"] = [1,0,1]
                d["MM"] = [1,2]

                if(this[2] == prevInsList[-2][4] and (prevInsList[-2][1] == "lw" or prevInsList[-2][1] == "lb" or prevInsList[-2][1] == "lh")): #rs1 and rd match
                    # d["MES"] = [1,1,1]
                    d["MES"] = [1,3]

        #M to E
        if(len(prevInsList) >=3 and (this[0] == 1 or this[0] == 2 or this[0] == 3)): #R, I, S ins
            if(this[2] == prevInsList[-3][4]):
                # d["ME"] = [1,1,0]
                d["ME"] = [1,1]
                if(this[3] == prevInsList[-3][4]):
                    # d["ME"] = [1,1,1]
                    d["ME"] = [1,3]


            elif(this[3] == prevInsList[-3][4]):
                # d["ME"] = [1,0,1]
                d["ME"] = [1,2]


        #EE
        if(len(prevInsList) >=2 and (this[0] == 1 or this[0] == 2 or this[0] == 3)):
            # if(prevInsList[-2][1] != "lh" and prevInsList[-2][1] != "lw" and prevInsList[-2][1] != "lb"):
                if(this[2] == prevInsList[-2][4]): #rs1 == rd
                    # d["EE"] = [1,1,0]
                    d["EE"] = [1,1]
                    if(this[3] == prevInsList[-2][4] and this[0] !=3): #rs2 == rd
                        # d["EE"] = [1,1,1]
                        d["EE"] = [1,3]
                elif(this[3] == prevInsList[-2][4] and this[0] !=3): #rs2 == rd
                        # d["EE"] = [1,0,1]  
                        d["EE"] = [1,2]  


        #MES 
        if(len(prevInsList) >=2 and (this[0] == 1 or this[0] == 2 or this[0] == 3) and(prevInsList[-2][1] == 'lb' or prevInsList[-2][1] == 'lh' or prevInsList[-2][1] == 'lw')):
            if(this[2] == prevInsList[-2][4]):
                # d["MES"] = [1,1,0]
                d["MES"] = [1,1]
                if(this[3] == prevInsList[-2][4]):
                    # d["MES"] = [1,1,1]
                    d["MES"] = [1,3]

            elif(this[3] == prevInsList[-2][4]):
                # d["MES"] = [1,0,1]
                d["MES"] = [1,2]
        

    else:  #control ins checking is left :(
        #whenever RAW, do_stall == 1
        do_stall = 0
        if(this[0] == 5 or this[0] == 6):   #if U or J ins then no hazards
            do_stall = 0

        elif(this[0] == 1 or this[0] == 2 or this[0] == 3): #R, I, S ins
            if(len(prevInsList) >= 2 and (this[2] == prevInsList[-2][4] or this[3] == prevInsList[-2][4])):
                do_stall = 1
            elif(len(prevInsList) >= 3 and (this[2] == prevInsList[-3][4] or this[3] == prevInsList[-3][4])):
                do_stall = 1

        return do_stall

    prevInsList = prevInsList[-3:]  #prevInsList is never bigger than 3 for control ins. I.e. all things can go wrong only in 3 ins max


def check_control_hazard(buffers, prevInsList, d):
    this = prevInsList[-1]

    #MD
    if(len(prevInsList) >= 4 and (prevInsList[-4][0] == 1 or prevInsList[-4][0] == 2)): #load or R or I type
        if(prevInsList[-4][4] == this[2]): #rs1 same
            d["MD"] = [1,1]
            # if(prevInsList[-4][4] == this[3]): #rs2 and rs1 same
            #     d["MD"] = [1,3]
        elif(prevInsList[-4][4] == this[3]): #rs2 same            
            d["MD"] = [1,2]

    #ED
    if(len(prevInsList) >= 3 and (prevInsList[-3][0] == 1 or prevInsList[-3][0] == 2 and(prevInsList[-3][1] != "lw" and prevInsList[-3][1] != "lh" and prevInsList[-3][1] != "lb"))):
        if(prevInsList[-3][4] == this[2]): #rs1 same
            d["ED"] = [1,1]
            # if(prevInsList[-3][4] == this[3]): #rs2 and rs1 same
            #     d["ED"] = [1,3]
        elif(prevInsList[-3][4] == this[3]): #rs2 same            
            d["ED"] = [1,2]

    #MDS
    if(len(prevInsList) >= 3 and (prevInsList[-3][1] == "lw" or prevInsList[-3][1] == "lh" or prevInsList[-3][1] != "lb")):
        if(prevInsList[-3][4] == this[2]): #rs1 same
            d["MDS"] = [1,1]
            if(d["MD"][0] ==1): #bec this would have already been written back
                d["MD"] = [0,0]
        elif(prevInsList[-3][4] == this[3]): #rs2 same            
            d["MDS"] = [1,2]
            if(d["MD"][0] ==1): #bec this would have already been written back
                d["MD"] = [0,0]

    #EDS
    if(len(prevInsList) >= 2 and (prevInsList[-2][0] == 1 or  prevInsList[-2][0] == 2 and(prevInsList[-2][1] != "lw" and prevInsList[-2][1] != "lh" and prevInsList[-2][1] != "lb"))):
        if(prevInsList[-2][4] == this[2]): #rs1 same
            d["EDS"] = [1,1]
            if(d["ED"][0] == 1):
                d["MD"] = d["ED"]
                d["ED"] = [0,0]    
        elif(prevInsList[-2][4] == this[3]): #rs2 same            
            d["EDS"] = [1,2]
            if(d["ED"][0] == 1):
                d["MD"] = d["ED"]
                d["ED"] = [0,0] 

    #MDSS
    if(len(prevInsList) >= 2 and (prevInsList[-2][1] == "lw" or prevInsList[-2][1] == "lh" or prevInsList[-2][1] != "lb")):
        if(prevInsList[-2][4] == this[2]): #rs1 same
            d["MDSS"] = [2,1]
        elif(prevInsList[-2][4] == this[3]):
            d["MDSS"] = [2,2]