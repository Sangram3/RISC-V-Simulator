def write_back(write_control, reg_obj, data, l):      #reg_no is found using reg_obj.get_rd() function, data is in hex (with 0x)
    if(write_control):   
        reg_no = reg_obj.get_rd()                         
        reg_obj.store_reg(reg_no, data)
        if(reg_no != 0):
            l.append("WRITEBACK: " + str(data) + " in x" + str(reg_no))
        else:
            l.append("WRITEBACK: Destination register is x0 so it remains unchanged")    
        reg_obj.make0()
    else:
        l.append("WRITEBACK: no writeback")
