from memory import *
from mem import *
from cache import *
# dcache_size = 1024*int(input("Enter cache size for data cache in kilobytes: "))
dcache_size = 1024

#cache_size = int(input("Enter cache size in kilobytes: "))

# dblock_size = int(input("Enter block size for data cache in bytes: "))
dblock_size = 32

# dways = int(input("Enter number of ways for SA for data cache: "))
dways = 4

# icache_size = 1024*int(input("Enter cache size for instruction cache in kilobytes: "))
icache_size = 1024
#cache_size = int(input("Enter cache size in kilobytes: "))
# iblock_size = int(input("Enter block size for instruction cache in bytes: "))
iblock_size = 32
# iways = int(input("Enter number of ways for SA for instruction cache: "))
iways = 4


dcache_ob = cache(dcache_size, dblock_size, dways)
icache_ob = cache(icache_size, iblock_size, iways)

mc_file = "temp.mc"
mem_mod = memory(mc_file)
