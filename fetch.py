#fetch
#create IR class with following:-

#-IR variable
#-set IR method (fetch step)(sets current instruction according to PC value)
#-get IR method (returns current instruction)

#method to increment PC (PC+4) by calling add_PC in PC class

#code starts here
import sys
from collections import defaultdict
class IR():
    f = "file is empty" # .mc file will be opened in this variable
    inst_reg = defaultdict() #this will contain all the instructions along with the addresses

    def __init__(self): #constructor
        pass
    
    def open_file(self,filename):# opens .mc file and updates Instruction register
        self.f = open(filename) 
        for p in self.f:
            p = p.strip()
            if len(p)>0:
                if p[0]!= '.':
                    p = p.split()
                    IR.inst_reg.update({p[0]: p[1]})
                    
    def print_IR(self): #print Instruction Register
        for key in self.inst_reg:
            print(key,self.inst_reg[key])
            
    def get_instruction(self): #gets next instruction
        pass
        
    def Set_IR(self): #sets PC value
        pass
        
inst_register = IR()
inst_register.open_file("add.mc")
inst_register.print_IR()
