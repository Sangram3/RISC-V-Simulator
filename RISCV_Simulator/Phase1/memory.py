class memory:
    __mem_dict = {}

    def reset_mem(self):
        self.__mem_dict = {}
    def print_mem(self):
        print(self.__mem_dict)
    
    def get_mem(self):
        return self.__mem_dict

    def __init__(self,mc_file):
        f=open(mc_file,"r")
        lines = f.readlines()
        for line in lines:
            line = line.split()
            if(len(line[1]) != 10):
                line[1] = "0x"+ ('0'*(10-len(line[1]))) + line[1][2:]
            self.__mem_dict[int(line[0],16) + 0] = line[1][-2:]
            self.__mem_dict[int(line[0],16) + 1] = line[1][-4:-2]
            self.__mem_dict[int(line[0],16) + 2] = line[1][-6:-4]
            self.__mem_dict[int(line[0],16) + 3] = line[1][-8:-6]

    def code_ends(self):
        done = set()
        text = ""
        for item in self.__mem_dict:
            item = item - item%4
            if item not in done:
                text+= hex(item).upper() + " " + "0x"
                for i in range(4):
                    text+=self.__mem_dict.get(item + 3 - i, "00")
                text+="\n"
                done.add(item) 
        return text

    def dic(self):
        #print(__mem_dict)
        return self.__mem_dict

    def lw(self, address):
        hex=""
        for i in range(4):
            # hex = self.__mem_dict[address+i] + hex
            hex = self.__mem_dict.get(address+i, "00") + hex
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
            # hex = self.__mem_dict[address+i] + hex
            hex = self.__mem_dict.get(address+i, "00") + hex
        return "0x"+hex  

    def sh(self, add, data):
        if(len(data) != 6):
            data = "0x"+ ('0'*(6-len(data))) + data[2:]

        self.__mem_dict[add + 0] = data[-2:]
        self.__mem_dict[add + 1] = data[-4:-2]

    def lb(self, address):
        hex=""
        # hex = self.__mem_dict[address] 
        hex = self.__mem_dict.get(address, "00") + hex
        return "0x"+hex  

    def sb(self, add, data):
        if(len(data) != 4):
            data = "0x"+ ('0'*(4-len(data))) + data[2:]
        self.__mem_dict[add + 0] = data[-2:]
    def value(self, key):
        return self.__mem_dict[key]
        
