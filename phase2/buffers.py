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


class BTB():

    table = {}
    
    def newKey(self, PC, Target_add,is_jal_jalr):  #FNTBT satic predictor
        if is_jal_jalr == 1:
            self.table[str(PC)] = [True,Target_add]
            return
        if(Target_add>=PC):  #forward branch not taken  #Imm is >= 0
            self.table[str(PC)] = [False,Target_add]
        else:
            self.table[str(PC)] = [True,Target_add]

    def prediction(self, PC):
        return self.table[str(PC)][0]

    def getTarget(self, PC):
        return self.table[str(PC)][1]

    def ifPresent(self,PC):
        if str(PC) in self.table:
            print(self.table[str(PC)])
            return True
        return False
        # if(str(PC) in self.table.keys()):
            # return True
        # return False        

# dic = BTB()
# print(dic)
# dic.newKey(12, 84)
# dic.newKey(14, -32)
# print(dic.prediction(14))
# print(dic.getTarget(18))
# print(dic.ifPresent(12))
