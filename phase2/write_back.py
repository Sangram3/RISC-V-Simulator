def write_back(reg_obj, buffers):      # data is in hex (with 0x)
    
    if(buffers[3].rd != -1):   
        reg_no = buffers[3].rd 
        data = buffers[3].RY                        
        reg_obj.store_reg(reg_no, data)
        reg_obj.make0()