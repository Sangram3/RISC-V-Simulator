class InterStateBuffer:
    def __init__(self):
        self.ResetBuffer()

    #These variables are not protected.
    def ResetBuffer(self):
        self.RZ = 0 
        self.RM = 0 
        self.RY = 0 
        self.rs1 = -1 
        self.rs2 = -1 
        self.rd = -1 
        self.opcode = 0 
        self.PC = 0 
        self.RA = 0 
        self.RB = 0 
        self.MAR = 0 
        self.MDR = 0 
        self.IR = 0 
        self.operand1 = 0 
        self.operand2 = 0 

    # def printbuf(self):
    #     print(self.RZ)
    #     print(self.rd)

# buffers = [InterStateBuffer() for i in range(4)]   #this buffer list consists of 4 buffers, FD, DE, EM, MW.

# print(len(buffers))  
