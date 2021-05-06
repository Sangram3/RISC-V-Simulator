from cache import *
from memory import *
from registers import *
from fetch import *
from decode import *
from execute import *
from mem import *
from control import *
from write_back import *
from inputt import *

class gui_util_new():
    def __init__(self):
        self.task2 = []
        self.task3 = []
        self.task4 = []
    
    def reset_gui_util(self):
        self.task2 = []
        self.task3 = []
        self.task4 = []

def bin_to_dec(s): # input in two's compliment form
    if s[0] == '1':
        return -1 * (int(''.join('1' if x == '0' else '0' for x in s), 2) + 1)
    else:
        return int(s, 2)

def basic_code(dec_out, reg, mem):
    code = ""
    if(dec_out[0] == 1): #R
        code = dec_out[1]+ " x" + str(reg.get_rd()) + " x" + str(reg.get_rs1()) + " x"+ str(reg.get_rs2())
    elif(dec_out[0] == 2):
        imm = bin_to_dec(dec_out[2])
        if(dec_out[1] == 'lw' or dec_out[1] == 'lb' or dec_out[1] == 'lh'):
            code = dec_out[1] + " x" + str(reg.get_rd()) + " " + str(imm)+"(x" +str(reg.get_rs1())+")"
        else:    
            code = dec_out[1] + " x" + str(reg.get_rd()) + " x" + str(reg.get_rs1()) + " " +str(imm)
    elif(dec_out[0] == 3):
        imm = bin_to_dec(dec_out[2])
        code = dec_out[1] + " x" + str(reg.get_rs2()) + " " + str(imm)+"(x" +str(reg.get_rs1())+")"
    elif(dec_out[0] == 4):
        imm = bin_to_dec(dec_out[2])
        code = dec_out[1] + " x" + str(reg.get_rs1()) + " x" + str(reg.get_rs2()) + " " +str(imm)
    elif(dec_out[0] == 5 or dec_out[0] == 6):
        imm = bin_to_dec(dec_out[2])
        code = dec_out[1] + " x" + str(reg.get_rd()) +" " +str(imm)
    else:
        code = "Wrong Instruction"
    return code

# mc_file = "temp.mc"
# mem_mod = memory(mc_file)

reg_mod = registers()

# dcache_size = 1024*int(input("Enter cache size for data cache in kilobytes: "))
# #cache_size = int(input("Enter cache size in kilobytes: "))
# dblock_size = int(input("Enter block size for data cache in bytes: "))
# dways = int(input("Enter number of ways for SA for data cache: "))
# icache_size = 1024*int(input("Enter cache size for instruction cache in kilobytes: "))
# #cache_size = int(input("Enter cache size in kilobytes: "))
# iblock_size = int(input("Enter block size for instruction cache in bytes: "))
# iways = int(input("Enter number of ways for SA for instruction cache: "))

# dcache_ob = cache(dcache_size, dblock_size, dways)
# icache_ob = cache(icache_size, iblock_size, iways)

gui_util_obj_new = gui_util_new()

def run(li):  
    d = {}
    global l 
    l=[]
    
    # print("RUNNING")
    while(1):
        fetch(mem_mod,  reg_mod, l, icache_ob, gui_util_obj_new)
        if(reg_mod.get_IR() == '0xEF000011'):
            # mem_mod.code_ends('output.mc')
            break
        ins = reg_mod.get_IR()
        return_of_decode = list(decode(bin32(int( reg_mod.get_IR(),16)) ,  mem_mod,  reg_mod))
        control_bits = control(return_of_decode)
        return_of_execute = execute(return_of_decode[0], return_of_decode[1], return_of_decode[2], reg_mod, l)
        if(control_bits[1] != 0):
            return_of_mem = mem(control_bits[1],  mem_mod,  reg_mod, return_of_execute, l, dcache_ob, gui_util_obj_new)
        elif(control_bits[1]==0):
            l.append("MEMORY : No memory operation ")

        if(return_of_decode[1] == 'lw' or return_of_decode[1] == 'lh' or return_of_decode[1] == 'lb'):
            write_back(control_bits[0],  reg_mod, return_of_mem, l)
        
        else:
            write_back(control_bits[0],  reg_mod, return_of_execute, l)
        reg_mod.add_clock()
        d[reg_mod.get_clock()] = [hex(reg_mod.get_clock()-1), hex(reg_mod.get_PC()-4) ,ins ,basic_code(return_of_decode, reg_mod, mem_mod)]
    li=l
    gui_util_obj_new.task4 = [dcache_ob.memory_accesses+icache_ob.memory_accesses, dcache_ob.cache_accesses+icache_ob.cache_accesses, dcache_ob.cache_hit+icache_ob.cache_hit, dcache_ob.cache_miss+icache_ob.cache_miss]
    return [d,li]

def step(ll):  
    
    l = []
    fetch(mem_mod,  reg_mod, l, icache_ob, gui_util_obj_new)
    if(reg_mod.get_IR() == '0xEF000011'):
        # mem_mod.code_ends('output.mc')
        gui_util_obj_new.task4 = [dcache_ob.memory_accesses+icache_ob.memory_accesses, dcache_ob.cache_accesses+icache_ob.cache_accesses, dcache_ob.cache_hit+icache_ob.cache_hit, dcache_ob.cache_miss+icache_ob.cache_miss]
        return
    else:
        ins = reg_mod.get_IR()
        return_of_decode = list(decode(bin32(int( reg_mod.get_IR(),16)) ,  mem_mod,  reg_mod))
        control_bits = control(return_of_decode)
        return_of_execute = execute(return_of_decode[0], return_of_decode[1], return_of_decode[2], reg_mod,l)
        if(control_bits[1] != 0):
            return_of_mem = mem(control_bits[1],  mem_mod,  reg_mod, return_of_execute, l, dcache_ob, gui_util_obj_new)
        elif(control_bits[1] == 0):
            l.append("MEMORY: No memory operation")

        if(return_of_decode[1] == 'lw' or return_of_decode[1] == 'lh' or return_of_decode[1] == 'lb'):
            write_back(control_bits[0],  reg_mod, return_of_mem,l)
        
        else:
            write_back(control_bits[0],  reg_mod, return_of_execute,l)
        reg_mod.add_clock()
        #print(l)
        ll=l

        return[[hex(reg_mod.get_clock()-1), hex(reg_mod.get_PC()-4) ,ins ,basic_code(return_of_decode, reg_mod, mem_mod)],ll]


def reset():
    mc_file = "test.mc"
    mem_mod.reset_mem()
    reg_mod.reset_regs()
    mem_mod.__init__(mc_file)
    dcache_ob.reset()
    icache_ob.reset()
    gui_util_obj_new.reset_gui_util()
