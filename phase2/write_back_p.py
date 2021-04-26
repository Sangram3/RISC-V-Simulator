def write_back_p(reg_obj, buffers, pipeline_obj):      # data is in hex (with 0x)

    if((buffers[3].fmt == 1 or buffers[3].fmt == 2 or buffers[3].fmt == 5)  and buffers[3].mne != 'lw' and buffers[3].mne != 'lh' and buffers[3].mne != 'lb'):
        pipeline_obj.n_alu_ins = pipeline_obj.n_alu_ins+1
    
    if(buffers[3].fmt == 3 or buffers[3].mne == "lw" or  buffers[3].mne == "lh" or  buffers[3].mne == "lb"):
        pipeline_obj.n_datatrans = pipeline_obj.n_datatrans+1

    if(buffers[3].fmt == 4 or buffers[3].mne == "jalr" or buffers[3].fmt == 6):
        pipeline_obj.n_cont_ins = pipeline_obj.n_cont_ins+1


    if(buffers[3].rd != -3):   
        reg_no = buffers[3].rd 
        data = buffers[3].RY                        
        reg_obj.store_reg(reg_no, data)
        reg_obj.make0()
