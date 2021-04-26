class InterStateBuffer:
    def __init__(self):
        self.ResetBuffer()

    #These variables are not protected.
    def ResetBuffer(self):
        self.RZ = 0   #Output of the ALU. It can be used in data forwarding.
        self.RM = 0   #It has the value for the store ins. This is forwarded to MDR in stage 4(memory access).
        self.RY = 0   #The value which is to be written in the writeback stage.
        self.rs1 = -1  
        self.rs2 = -2 
        self.rd = -3 
        self.opcode = 0 
        self.PC = 0 
        self.RA = 0    # contains the value in rs1
        self.RB = 0    # contains the value in rs2
        self.MAR = 0   #Memory address register
        self.MDR = 0   #Memory data register
        self.IR = 0 
        self.operand1 = 0  #operand1 value
        self.operand2 = 0  #operand2 value
        self.predict = False
        self.fmt = None
        self.mne = None
        self.imm = 0
        

    # def printbuf(self):
    #     print(self.RZ)
    #     print(self.rd)

# buffers = [InterStateBuffer() for i in range(4)]   #this buffer list consists of 4 buffers, FD, DE, EM, MW.
# buffers[3].RZ = 3
# buffers[3].printbuf()
# print(len(buffers))  


