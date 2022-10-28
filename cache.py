import math

"""
    K-way set associative mapping used.
    LRU Replacement policy is used.
"""
class cache:
    ways = 0 # k- way set associative mapping
    block_size = 0 # size of one line in cache 
    cache_size = 0 # total number of words in cache
    block_count = 0 # number of lines in cache
    set_count = 0 # number of sets
    words_per_block = 0

    cache_accesses = 0
    cache_hit = 0
    cache_miss = 0
    memory_accesses = 0

    bo_len = 0
    index_len = 0
    tag_len = 0

    def __init__(self, cache_size, block_size, ways):
        """
            cache_size: size of cache
            block_size : size of one block in cache
            ways: k-way set associative mapping

        """
        self.cache_size = cache_size
        self.block_size = block_size
        self.ways = ways
        self.block_count = int(cache_size/block_size) # number of blocks
        self.set_count = int(self.block_count / ways) # number of sets
        self.words_per_block = int(block_size/4)
        
        self.bo_len = math.ceil(math.log2(block_size)) # number of bits in block offset
        self.index_len = math.ceil(math.log2(self.set_count)) # number of bits in block number

        self.cache_array = [[["tag", 0, ["data" for x in range(self.words_per_block)]] for _ways in range(ways)] for _set in range(self.set_count)]
        self.pref_array = [[0 for _ways in range(ways) ]  for _set in range(self.set_count)]

    def reset_cache(self):
        """
            Erase all the entries in the k-way set asso. cache.
        """
        self.cache_array = [[["tag", 0, ["data" for x in range(self.words_per_block)]] for _ways in range(self.ways)] for _set in range(self.set_count)]
        self.pref_array = [[0 for _ways in range(self.ways) ]  for _set in range(self.set_count)] 
        # preference array, stores the priority of each block in the cache. 
        # Whenever there is over flow the block with least preference is removed from the set.
        
    def decode_address(self, address):
        """
            Find the line number in the cache and the position of the word in that line.
        """
        bo = int(address, 16)%(2**self.bo_len)
        index = (int(address, 16)%(2**(self.index_len+self.bo_len)) - bo) >> self.bo_len
        tag = (int(address, 16) - int(address, 16)%(2**(self.index_len+self.bo_len))) >> (self.index_len+self.bo_len)
        return tag, index, bo # tag bit, set number , block offset.

    def read(self, address, mem_mod, k, gui_util_obj):
        """
            Read the word at given position in the cache.
        """
        self.cache_accesses+=1
        tag, index, bo = self.decode_address(address) # tag bit, set index , block offset
        # print(tag, index, bo)
        hit, way_no = self.hit_miss(tag, index)

        if(hit):
            self.cache_hit+=1
            return self.cache_array[index][way_no][2][int(bo/4)]  #BO would be used here
        else:
            self.cache_miss+=1
            data = []
            for i in range(self.words_per_block):
                # print("address ", int(address,16))
                temp = mem_mod.lw(int(address,16)+4*i)
                data.append(temp)
            # data = mem_mod.lw(int(address,16))
            self.write(address, data, mem_mod, k, gui_util_obj) #data is an array of words
            return data[int(bo/4)]

    def hit_miss(self, tag, index):
        """
            Check if the cache hit or miss is occuring.
            Returns [bool, block/line number]
        """
        _set = self.cache_array[index] # Fetch Set 
        for i in range(len(_set)):
            if(_set[i][0] == tag and _set[i][1] == 1):
                return True, i
        return False, 0
    
    #this is for block replacement policy that is write from the memory to the cache
    def write(self, address, data, mem_mod, k, gui_util_obj):
        """ Write the value of word in its corresponding block in the cache. """
        self.memory_accesses+=1
        tag, index, bo = self.decode_address(address)
        #if empty block present then write there
        for _way in range(len(self.cache_array[index])): 
            if(self.cache_array[index][_way][1] == 0):
                self.cache_array[index][_way][0] = tag
                self.cache_array[index][_way][1] = 1
                self.cache_array[index][_way][2] = data
                self.set_pref(index, _way)
                return

        #if all blocks are filled then use lru
        _way = self.pref_array[index].index(min(self.pref_array[index]))
        """ get the block with least preference/priority to remove"""

        # Victim block
        victim_bl = self.cache_array[index][_way][:]

        temp = [k, index, _way, address, victim_bl]

        # print in the front end
        gui_util_obj.task3.append(temp)
        temp = []
        

        self.cache_array[index][_way][0] = tag
        self.cache_array[index][_way][1] = 1
        self.cache_array[index][_way][2] = data
        self.set_pref(index, _way)
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
        self.memory_accesses+=1 #for write through
        self.cache_accesses+=1
        tag, index, bo = self.decode_address(address)
        h, ind = self.hit_miss(tag, index)
        if(h == True):
            self.cache_hit+=1
            # for i in range(len(self.cache_array[index])):
            for _way in range(len(self.cache_array[index])):
                if(self.cache_array[index][_way][0] == tag):
                    if(len(data) != 10):
                        data = "0x"+ ('0'*(10-len(data))) + data[2:]
                    self.cache_array[index][_way][2][int(bo/4)] = data
                    return
        self.cache_miss+=1
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
