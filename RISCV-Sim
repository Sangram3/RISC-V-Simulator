from memory import *
from registers import *
from fetch import *
from decode import *
from execute import *
from mem import *

mc_file = "test.mc"

mem_mod = memory(mc_file)
reg_mod = registers()

while(1):
    fetch(mem_mod, reg_mod)

    return_of_decode = list(decode(bin32(int(reg_mod.get_IR(),16)) , mem_mod, reg_mod))
    return_of_execute = execute(return_of_decode[0], return_of_decode[1], return_of_decode[2],reg_mod)
    write_back(1, reg_mod, return_of_execute)
    


# print(return_of_execute)

    

# reg_mod.print_reg()
# print(decode(bin32(reg_mod.get_IR()[2:]), mem_mod, reg_mod ))
# print(fetch(mem_mod,reg_mod))
# print(reg_mod.get_IR())
# print(reg_mod.get_PC())
