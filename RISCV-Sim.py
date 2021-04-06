from memory import *
from registers import *
from fetch import *
from decode import *
from execute import *
from mem import *
from control import *
from write_back import *

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

def main():

    dic = {}

    mc_file = "test.mc"

    mem_mod = memory(mc_file)
    reg_mod = registers()
    clock = 0
    regi = [reg_mod.load_reg(i) for i in range(32)]
    memi = mem_mod.get_mem()
    dic[clock] = [regi, memi, reg_mod.get_PC(), reg_mod.get_IR()]
            
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
        memi = mem_mod.get_mem()
        code = basic_code(return_of_decode, reg_mod, mem_mod)
        print(code)
        dic[clock] = [regi, memi, reg_mod.get_PC(), reg_mod.get_IR(), code]
        #print(dic)
        print(reg_mod.get_PC())
        mem_mod.print_mem()
        reg_mod.print_reg()
    
    return dic


d = main()
