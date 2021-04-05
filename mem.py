  
def write_back(write_control, reg_obj, data):      #reg_no is found using reg_obj.get_rd() function, data is in hex (with 0x)
    if(write_control):   
        reg_no = reg_obj.get_rd()                         
        reg_obj.store_reg(reg_no, data) 


def mem(if_needed, mem_control, mem_obj, add, *args):   #data in hex with 0x
    if(if_needed):
        if(mem_control == 1):
            # sw
            sw(add, args[0])
        else if(mem_control == 2):
            # sh
            sh(add,args[0])
        else if(mem_control == 3):
            # sb
            sb(add,args[0])   #args[0] is the data in hexwith 0x
        else if(mem_control == 4):
            # lw    
            lw(add)
        else if(mem_control == 5):
            # lb
            lb(add)
        else if(mem_control == 6):
            lh(add)
            # lh    #     #      



