class BTB():

    
    btb = {}
    
    def newKey(self, PC, Target_add,is_jal_jalr):  #FNTBT satic predictor
        if is_jal_jalr == 1:
            self.btb[str(PC)] = [True,Target_add]
            return
        if(Target_add>=PC):  #forward branch not taken  #Imm is >= 0
            self.btb[str(PC)] = [False,Target_add]
        else:
            self.btb[str(PC)] = [True,Target_add]

    def prediction(self, PC):
        return self.btb[str(PC)][0]

    def getTarget(self, PC):
        return self.btb[str(PC)][1]

    def ifPresent(self,PC):
        if str(PC) in self.btb:
            return True
        return False      

# dic = BTB()
# print(dic)
# dic.newKey(12, 84)
# dic.newKey(14, -32)
# print(dic.prediction(14))
# print(dic.getTarget(18))
# print(dic.ifPresent(12))
