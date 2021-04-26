from memory_p import *
from registers_p import *
from fetch_p import *
from decode_p import *
from execute_p import *
from mem_p import *
from write_back_p import *
from buffers import *
from branch_table_buffer import *
from Pipeline import *

class Model_Unit:
    def __init__(self):
        self.is_pipelined = 0
        self.is_data_forwarding = 0


model_unit = Model_Unit()

# model_unit.is_pipeline = int(input("Want Pipelined : "))
# if model_unit.is_pipeline == 1:
    # model_unit.is_data_forwarding = int(input("Want Data Forwarding: "))


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

mc_file = "test.mc"
mem_mod = memory(mc_file)
reg_mod = registers_p()


def run(li):  
    d = {}
    global l 
    l=[]
    while(1):
        fetch_p(mem_mod,  reg_mod, l)
        if(reg_mod.get_IR() == '0xEF000011'):
            # mem_mod.code_ends('output.mc')
            break
        ins = reg_mod.get_IR()
        return_of_decode = list(decode(bin32(int( reg_mod.get_IR(),16)) ,  mem_mod,  reg_mod))
        control_bits = control(return_of_decode)
        return_of_execute = execute(return_of_decode[0], return_of_decode[1], return_of_decode[2], reg_mod, l)
        if(control_bits[1] != 0):
            return_of_mem = mem_p(control_bits[1],  mem_mod,  reg_mod, return_of_execute, l)
        elif(control_bits[1]==0):
            l.append("MEMORY : No memory operation ")

        if(return_of_decode[1] == 'lw' or return_of_decode[1] == 'lh' or return_of_decode[1] == 'lb'):
            write_back(control_bits[0],  reg_mod, return_of_mem, l)
        
        else:
            write_back_p(control_bits[0],  reg_mod, return_of_execute, l)
        reg_mod.add_clock()
        d[reg_mod.get_clock()] = [hex(reg_mod.get_clock()-1), hex(reg_mod.get_PC()-4) ,ins ,basic_code(return_of_decode, reg_mod, mem_mod)]
    li=l
    return [d,li]

def step(ll):  
    
    l = []
    fetch_p(mem_mod,  reg_mod, l)
    if(reg_mod.get_IR() == '0xEF000011'):
        # mem_mod.code_ends('output.mc')
        return
    else:
        ins = reg_mod.get_IR()
        return_of_decode = list(decode_p(bin32(int( reg_mod.get_IR(),16)) ,  mem_mod,  reg_mod))
        control_bits = control(return_of_decode)
        return_of_execute = execute_p(return_of_decode[0], return_of_decode[1], return_of_decode[2], reg_mod,l)
        if(control_bits[1] != 0):
            return_of_mem = mem_p(control_bits[1],  mem_mod,  reg_mod, return_of_execute, l)
        elif(control_bits[1] == 0):
            l.append("MEMORY: No memory operation")

        if(return_of_decode[1] == 'lw' or return_of_decode[1] == 'lh' or return_of_decode[1] == 'lb'):
            write_back_p(control_bits[0],  reg_mod, return_of_mem,l)
        
        else:
            write_back_p(control_bits[0],  reg_mod, return_of_execute,l)
        reg_mod.add_clock()
        #print(l)
        ll=l

        return[[hex(reg_mod.get_clock()-1), hex(reg_mod.get_PC()-4) ,ins ,basic_code(return_of_decode, reg_mod, mem_mod)],ll]


def reset():
    
    mc_file = "test.mc"
    mem_mod.reset_mem()
    reg_mod.reset_regs()
    mem_mod.__init__(mc_file)
    

# execute_cycle_util()
# print(pipeline_obj.master_store)




