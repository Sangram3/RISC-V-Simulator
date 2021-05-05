import math

class cache:
    ways = 0
    block_size = 0
    cache_size = 0
    block_count = 0
    set_count = 0
    words_per_block = 0

    accesses = 0
    hit = 0
    miss = 0

    bo_len = 0
    index_len = 0
    tag_len = 0

    def __init__(self, cache_size, block_size, ways):
        
        self.cache_size = cache_size
        self.block_size = block_size
        self.ways = ways
        self.block_count = int(cache_size/block_size)
        self.set_count = int(self.block_count / ways)
        self.words_per_block = int(block_size/4)
        
        self.bo_len = math.ceil(math.log2(block_size))
        self.index_len = math.ceil(math.log2(self.set_count))

        self.cache_array = [[["tag", 0, ["data" for x in range(self.words_per_block)]] for _ways in range(ways)] for _set in range(self.set_count)]
        self.pref_array = [[0 for _ways in range(ways) ]  for _set in range(self.set_count)]
        
    
    def decode_address(self, address):
        bo = int(address, 16)%(2**self.bo_len)
        index = (int(address, 16)%(2**(self.index_len+self.bo_len)) - bo) >> self.bo_len
        tag = (int(address, 16) - int(address, 16)%(2**(self.index_len+self.bo_len))) >> (self.index_len+self.bo_len)
        return tag, index, bo

    def read(self, address, mem_mod):
        self.accesses+=1
        tag, index, bo = self.decode_address(address)
        # print(tag, index, bo)
        hit, way_no = self.hit_miss(tag, index)
        if(hit):
            self.hit+=1
            return self.cache_array[index][way_no][2][int(bo/4)]    #BO would be used here

        else:
            self.miss+=1
            data = []
            for i in range(self.words_per_block):
                # print("address ", int(address,16))
                temp = mem_mod.lw(int(address,16)+4*i)
                data.append(temp)
            # data = mem_mod.lw(int(address,16))
            self.write(address, data, mem_mod) #data is an array of words
            return data[int(bo/4)]

    def hit_miss(self, tag, index):
        _set = self.cache_array[index]
        for i in range(len(_set)):
            if(_set[i][0] == tag and _set[i][1] == 1):
                return True, i
            
        return False, 0
    #this is for block replacement policy that is write from the memory to the cache
    def write(self, address, data, mem_mod):
        self.accesses+=1
        tag, index, bo = self.decode_address(address)
        for _way in range(len(self.cache_array[index])):
            if(self.cache_array[index][_way][1] == 0):
                self.cache_array[index][_way][0] = tag
                self.cache_array[index][_way][1] = 1
                self.cache_array[index][_way][2] = data
                self.set_pref(index, _way)
                # print("data: ", data)
                # for i in range(self.words_per_block):
                #     mem_mod.sw(int(address,16)+4*i, data[i])
                # mem_mod.sw(int(address,16), data)
                return

        _way = self.pref_array[index].index(min(self.pref_array[index]))
        self.cache_array[index][_way][0] = tag
        self.cache_array[index][_way][1] = 1
        self.cache_array[index][_way][2] = data
        self.set_pref(index, _way)
        # print("data: ", data)
        # for i in range(self.words_per_block):
        #     mem_mod.sw(int(address,16)+4*i, data[i])
        return

    def set_pref(self, index, way_no):
        for i in range(len(self.pref_array[index])):
            if(i == way_no):
                self.pref_array[index][i] = self.ways
            else:
                if(self.pref_array[index][i] != 0):
                    self.pref_array[index][i]-=1

    def print_cache(self):
        for i in range(self.set_count):
            print(self.cache_array[i])

    #Storedata is used in the write through policy to write in the cache if the block containing that data is present 

    def storedata(self, address, data): #data is a word
        tag, index, bo = self.decode_address(address)
        h, ind = self.hit_miss(tag, index)
        if(h == True):
            # for i in range(len(self.cache_array[index])):
            for _way in range(len(self.cache_array[index])):
                if(self.cache_array[index][_way][0] == tag):
                    if(len(data) != 10):
                        data = "0x"+ ('0'*(10-len(data))) + data[2:]
                    self.cache_array[index][_way][2][int(bo/4)] = data
                    return
        return
    


# x = cache(1256, 64, 4)
# x.write("ABC", 56)
# x.write("1BC", 12)
# x.write("2Ba", 15)
# x.write("ABb", 18)
# x.write("fBa", 19)
# print(x.cache_array)
# print(x.pref_array)
# print(x.read("ABC"))
