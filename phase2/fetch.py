def fetch(reg_mod, mem_mod, btb, buffers, forw_d):
    
    PC = reg_mod.get_PC()
    inst = mem_mod.lw(PC)
    reg_mod.add_PC(4)
    
    IR = int(inst, 16)
    opcode = IR & (0x7F)

    # data-forwarding = M-D and E-D
    if(opcode == 99): # SB type
        buffers[0].operand1 = registers.__regs[rs1]
        buffers[0].operand2 = registers.__regs[rs2]
        #check data hazard using HDU Unit
        if(forw_d["ED"][0] == 1 and forw_d["EDS"][0] == 0):
            data_forw(4, forw_d["ED"][1], buffers)
            forw_d["ED"][0] = 0
            forw_d["ED"][1] = None 

        elif(forw_d["MD"][0] == 1 and forw_d["MDS"][0] == 0):
            data_forw(5, forw_d["MD"][1], buffers)
            forw_d["MD"][0] = 0
            forw_d["MD"][1] = None 

            

    elif(opcode == 103): # jalr
        buffers[0].operand1 = registers.__regs[rs1]
        #check data hazard using HDU Unit
        if(forw_d["ED"][0] == 1 and forw_d["EDS"][0] == 0):
            data_forw(4, forw_d["ED"][1], buffers)
            forw_d["ED"][0] = 0
            forw_d["ED"][1] = None 

        elif(forw_d["MD"][0] == 1 and forw_d["MDS"][0] == 0):
            data_forw(5, forw_d["MD"][1], buffers)
            forw_d["MD"][0] = 0
            forw_d["MD"][1] = None

    # predicting 
	if (opcode == 103 or opcode == 99 or opcode == 111):
		if (btb.ifPresent() and btb.prediction(PC)):
			buffers[0].predict = True
		
    buffers[0].PC = PC
    buffers[0].IR = inst
