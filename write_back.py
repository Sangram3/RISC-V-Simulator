def write_back(write_control, reg_obj, data):      #reg_no is found using reg_obj.get_rd() function, data is in hex (with 0x)
    if(write_control):   
        reg_no = reg_obj.get_rd()                         
        reg_obj.store_reg(reg_no, data)
        reg_obj.make0()