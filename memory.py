class memory:
    __mem_dict = {}

    #     __code_start=0x00000000
    #     __data_start=0x10000000
    __stack_start=0x7FFFFFFC
    __heap_start=0x10007FE8

    def __init__(self,mc_file):
        f=open(mc_file,"r")
        lines = f.readlines()
        for line in lines:
            line = line.split()
            self.__mem_dict[int(line[0],16) + 0] = line[1][-2:]
            self.__mem_dict[int(line[0],16) + 1] = line[1][-4:-2]
            self.__mem_dict[int(line[0],16) + 2] = line[1][-6:-4]
            self.__mem_dict[int(line[0],16) + 3] = line[1][-8:-6]

    def code_ends(self, mc_output):
        file = open(mc_output,"w")
        done = set()
        for item in self.__mem_dict:
            item = item - item%4
            if item not in done:
                file.write(hex(item).upper() + " " + "0x")
                for i in range(4):
                    file.write(self.__mem_dict.get(item + 3 - i, "00"))
                file.write("\n") 
                done.add(item) 

    def dic(self):
        #print(__mem_dict)
        return self.__mem_dict

    def lw(self, address):
        hex=""
        for i in range(4):
            hex = self.__mem_dict[address+i] + hex
        return "0x"+hex 

    def sw(self, add, data):    #data - hex
        if(len(data) != 10):
            data = "0x"+ ('0'*(10-len(data))) + data[2:]
        self.__mem_dict[add + 0] = data[-2:]
        self.__mem_dict[add + 1] = data[-4:-2]
        self.__mem_dict[add + 2] = data[-6:-4]
        self.__mem_dict[add + 3] = data[-8:-6]

    def lh(self, address):
        hex=""
        for i in range(2):
            hex = self.__mem_dict[address+i] + hex
        return "0x"+hex  

    def sh(self, add, data):
        if(len(data) != 6):
            data = "0x"+ ('0'*(6-len(data))) + data[2:]

        self.__mem_dict[add + 0] = data[-2:]
        self.__mem_dict[add + 1] = data[-4:-2]

    def lb(self, address):
        hex=""
        hex = self.__mem_dict[address] 
        return "0x"+hex  

    def sb(self, add, data):
        if(len(data) != 4):
            data = "0x"+ ('0'*(4-len(data))) + data[2:]
        self.__mem_dict[add + 0] = data[-2:]
        
        
