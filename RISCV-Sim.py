from memory import *
from registers import *
from fetch import *
from decode import *
from execute import *
from mem import *
from control import *
from write_back import *

def main():

    dic = {}

    mc_file = "test.mc"

    mem_mod = memory(mc_file)
    reg_mod = registers()
    clock = 0
            
    while(1):
        fetch(mem_mod,  reg_mod)
        if(reg_mod.get_IR() == '0xEF000011'):
            mem_mod.code_ends('output.mc')
            break
        return_of_decode = list(decode(bin32(int( reg_mod.get_IR(),16)) ,  mem_mod,  reg_mod))
        control_bits = control(return_of_decode)
        return_of_execute = execute(return_of_decode[0], return_of_decode[1], return_of_decode[2], reg_mod)
        # return_of_mem = mem(control_bits[1], mem_obj, return_of_execute, data)
        if(control_bits[1] != 0):
            return_of_mem = mem(control_bits[1],  mem_mod,  reg_mod, return_of_execute)

        if(return_of_decode[1] == 'lw' or return_of_decode[1] == 'lh' or return_of_decode[1] == 'lb'):
            write_back(control_bits[0],  reg_mod, return_of_mem)

        else:
            write_back(control_bits[0],  reg_mod, return_of_execute)
        clock =  clock+1
        
        regi = [reg_mod.load_reg(i) for i in range(32)]
        memi = mem_mod.dic()
        dic[clock] = [regi, memi, reg_mod.get_PC(), reg_mod.get_IR()]
        print(dic)
    
    return dic


d = main()
