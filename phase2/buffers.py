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
# buffers[3].RZ = 3
# buffers[3].printbuf()
# print(len(buffers))  


class BTB():

    table = {}
    
    def newKey(self, PC, Target_add):  #FNTBT satic predictor
        if(Target_add>=PC):  #forward branch not taken  #Imm is >= 0
            self.table[str(PC)] = [False,Target_add]
        else:
            self.table[str(PC)] = [True,Target_add]

    def prediction(self, PC):
        return self.table[str(PC)][0]

    def getTarget(self, PC):
        return self.table[str(PC)][1]

    def ifPresent(self,PC):
        if(str(PC) in self.table.keys()):
            return True
        else:
            return False        

# dic = BTB()
# print(dic)
# dic.newKey(12, 84)
# dic.newKey(14, -32)
# print(dic.prediction(14))
# print(dic.getTarget(18))
# print(dic.ifPresent(12))
