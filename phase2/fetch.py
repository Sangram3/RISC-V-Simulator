def fetch(reg_mod, mem_mod, btb, buffers):

        PC = reg_mod.get_PC()
        inst = mem_mod.lw(PC)
        reg_mod.add_PC(4)
    	
        IR = int(inst, 16)
        opcode = IR & (0x7F)

        # predicting 
		if (opcode == 103 or opcode == 99 or opcode == 111):
			if (btb.ifPresent() and btb.prediction(PC)):
				buffers[0].predict = True
		
        buffers[0].PC = PC
        buffers[0].IR = inst