class registers:
    __regs=[0 for i in range(32)]
 
    __PC = 0
    __IR = 0
    __rs1 = 0
    __rs2 = 0
    __rd = 0
 
    def print_reg(self):
        print(self.__regs)

    def add_PC(self, x):
        self.__PC += x
 
    def get_PC(self):
        return self.__PC
 
    def set_IR(self,x):
        self.__IR = x
 
    def get_IR(self):
        return self.__IR
 
    def set_rs1(self,x):
        self.__rs1 = x
 
    def get_rs1(self):
        return self.__rs1
 
    def set_rs2(self,x):
        self.__rs2 = x
 
    def get_rs2(self):
        return self.__rs2
 
    def set_rd(self,x):
        self.__rd = x
 
    def get_rd(self):
        return self.__rd
  
    def load_reg(self,reg_num):
        return self.__regs[reg_num]
    
    def store_reg(self,reg_num, data):   #the data is in hex with 0x
        self.__regs[reg_num] = data
