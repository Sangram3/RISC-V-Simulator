from collections import defaultdict
 
class memory:
    __mem_dict= defaultdict(lambda: "Not Present")
    
    __code_start=0x00000000
    __data_start=0x10000000
    # __data_stop=0
    __stack_start=0x7FFFFFFC
    __heap_start=0x10007FE8
 
    def __init__(self,mc_file):
        f=open(mc_file,"r")
        lines = f.readlines()
        for line in lines:
            line = line.split()
            self.__mem_dict[int(line[0],16)] = int(line[1],16)
        # print(self.__mem_dict)    
    
    def dic(self):
        # print(__mem_dict)
        return self.__mem_dict
    
    def load_data(self, add):
        return self.__mem_dict[add]
    
    def store_data(self, add, data):
        self.__mem_dict[add] = data
    
    def code_ends(self, mc_output):    #When swi is intercepted, then this is called to make the output file.
        file = open(mc_output,"w")
        for item in self.__mem_dict:
            file.write(hex(item).upper() + " " + hex(self.__mem_dict[item]).upper() + "\n")




class registers:
    __regs=[0 for i in range(32)]
 
    __PC = 0
    __IR = 0
    __rs1 = 0
    __rs2 = 0
    __rd = 0
 
    def add_PC(x):
        __PC += x
 
    def get_PC():
        return __PC
 
 
    def set_IR(x):
        __IR = x
 
    def get_IR():
        return __IR
 
 
    def set_rs1(x):
        __rs1 = x
 
    def get_rs1():
        return __rs1
 
    
 
    def set_rs2(x):
        __rs2 = x
 
    def get_rs2():
        return __rs2
 
 
    def set_rd(x):
        __rd = x
 
    def get_rd():
        return __rd
 
 
    def load_reg(reg_num):
        return __regs[reg_num]
    
    def store_reg(reg_num, data):   
        __regs[reg_num] = data
