import math

class cache:
    ways = 0
    block_size = 0
    cache_size = 0
    block_count = 0
    set_count = 0

    accesses = 0
    hit = 0

    bo_len = 0
    index_len = 0
    tag_len = 0

    def __init__(self, cache_size, block_size, ways):
        
        #self.mem_mod = mem_mod

        self.cache_size = cache_size
        self.block_size = block_size
        self.ways = ways

        self.block_count = int(cache_size/block_size)
        self.set_count = int(self.block_count / ways)
        
        self.bo_len = math.ceil(math.log2(block_size))
        self.index_len = math.ceil(math.log2(self.set_count))

        initial_data = "0"*int(block_size/4)
        self.cache_array = [[["", 0, initial_data] for _ways in range(ways)] for _set in range(self.set_count)]
        self.pref_array = [[0 for _ways in range(ways) ]  for _set in range(self.set_count)]
        
    
    def decode_address(self, address):
        bo = int(address, 16)%(2**self.bo_len)
        index = (int(address, 16)%(2**(self.index_len+self.bo_len)) - bo) >> self.bo_len
        tag = (int(address, 16) - int(address, 16)%(2**(self.index_len+self.bo_len))) >> (self.index_len+self.bo_len)
        return tag, index, bo

    def read(self, address):
        self.accesses+=1
        tag, index, bo = self.decode_address(address)
        hit, way_no = self.hit_miss(tag, index)
        if(hit):
            self.hit+=1
            return self.read_from_block(self.cache_array[index][way_no][2], bo, 32)    #BO would be used here

        else:
            #data = mem_mod.lw(address)
            data = 0
            self.write(address, data)
            return data

    def read_from_block(self, block, bo, size):
        if(self.block_size == size):
            return block
        elif(self.block_size > size):
            x = (bo - bo % size) / 4
            return block[int(x) : int(x+int(size/4))]

    

    def hit_miss(self, tag, index):
        _set = self.cache_array[index]
        for i in range(len(_set)):
            if(_set[i][0] == tag and _set[i][1] == 1):
                return True, i
            else:
                return False, 0

    def dec_to_2s(self, data, digits):
        return (hex(2**(digits*4) + data))[2:]
    
    def extend_hex(self,data, digits):
        ans =hex(data)[2:]
        if(len(hex(data)) < digits+2):
            for i in range(digits+2- len(hex(data))):
                ans = "0"+ans

            return  ans
        else:
            return hex(data)[2:]

    def write_to_block(self, index, _way, bo, data, size):
        print(data)
        initial_data = self.cache_array[index][_way][2]
    
        if(data > 0):
            data = self.extend_hex(data, int(size/4))
        else:
            data = self.dec_to_2s(data, int(size/4))

        #print(data, type(data))
        if(self.block_size == size):
            return data
        elif(self.block_size > size):
            x = (bo - bo % size) / 4
            #print("a",initial_data[:int(x+2)] ,data ,initial_data[int(x+2+int(size/4)):])
            
            return initial_data[:int(x)] + data + initial_data[int(x+int(size/4)):] 


    def write(self, address, data):
        tag, index, bo = self.decode_address(address)
        for _way in range(len(self.cache_array[index])):
            if(self.cache_array[index][_way][1] == 0):
                self.cache_array[index][_way][0] = tag
                self.cache_array[index][_way][1] = 1
                #print(self.cache_array[index][_way][2])
                self.cache_array[index][_way][2] = self.write_to_block(index, _way, bo, data, 32)
                #print(self.cache_array[index][_way][2])
                self.set_pref(index, _way)
                #mem_mod.write(address, data)
                return

        _way = self.pref_array[index].index(min(self.pref_array[index]))
        self.cache_array[index][_way][0] = tag
        self.cache_array[index][_way][1] = 1
        self.cache_array[index][_way][2] = self.write_to_block(index, _way, bo, data, 32)
        self.set_pref(index, _way)
        #mem_mod.write(address, data)
        return

    def set_pref(self, index, way_no):
        for i in range(len(self.pref_array[index])):
            if(i == way_no):
                self.pref_array[index][i] = self.ways
            else:
                if(self.pref_array[index][i] != 0):
                    self.pref_array[index][i]-=1

    


x = cache(1256, 64, 4)
x.write("ABC", 56)
x.write("1BC", 12)
x.write("200", -15)
x.write("ABb", 18)
x.write("fBa", 19)
for i in x.cache_array:
    print(i)
print(x.pref_array)
print(int(x.read("200"), 16))