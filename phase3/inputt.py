from memory import *
from mem import *
from cache import *
dcache_size = 1024*int(input("Enter cache size for data cache in kilobytes: "))
#cache_size = int(input("Enter cache size in kilobytes: "))
dblock_size = int(input("Enter block size for data cache in bytes: "))
dways = int(input("Enter number of ways for SA for data cache: "))
icache_size = 1024*int(input("Enter cache size for instruction cache in kilobytes: "))
#cache_size = int(input("Enter cache size in kilobytes: "))
iblock_size = int(input("Enter block size for instruction cache in bytes: "))
iways = int(input("Enter number of ways for SA for instruction cache: "))


dcache_ob = cache(dcache_size, dblock_size, dways)
icache_ob = cache(icache_size, iblock_size, iways)

mc_file = "temp.mc"
mem_mod = memory(mc_file)
