def write_back(write_control, reg_no, data):      #reg_no is found using get_rd() function
    if(write_control):
        reg_obj.store_reg(reg_no, data)               #reg_obj is the object of the registers class

def memory_access(memory_control, address, reg_no, data):
    if(memory_control == 1):   # for load data control = 1 
        reg_obj.store_reg(reg_no, mem_obj.load_data(address))   #reg_obj is registers class obj and mem_obj is the memory class object
    else if(memory_control == 2):   #for store, control = 2
        mem_obj.store_data(address, data)




#memory access

#create memory class
#create dictionary~CPU Memory
#dictionary <int,int/Byte> ~ <address,value>

#create following class variables:
#code_start ~ text segment
#data_start ~ data segment
#data_stop 
#stack_start ~ stack segment
#heap_start ~ heap segment

#create following methods/functions
#load_data,load_word,load_byte etc.
#store_data,store_word,store_byte etc.
#get_next_instruction
#get_data_at
#add_data_at
#show_memory

#create PC class
#create following methods
#add_PC
#get_PC



#create Registers class:
#create 32 registers
#create following methods
#load_from_register
#store_to_register
#print_register_value

#create ... 

