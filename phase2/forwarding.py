l= [[mne, rd], [mne, rd], [mne, rs1, rs2]]
def forwarding(l, all other buffers as parameters):

    f_reg = None
    f_value = None

    # M-M

    if((l[1][0] == 'lw' || l[1][0] == 'lb' || l[1][0] == 'lh') && ( l[2][0] == 'sw' || l[2][0] == 'sb' || l[2][0] == 'sh')):
        
        if (l[0][1] == l[2][1] || l[0][1] == l[2][2]):
            f_reg = l[0][1]
            f_value = buff_M_W_.get_reg(f_reg)
            buff_E_M_.set_reg(f_reg, f_value)
            
        elif (l[1][1] == l[2][1] || l[1][1] == l[2][2]):
            f_reg = l[1][1]
            f_value = buff_M_W_.get_reg(f_reg)
            buff_E_M_.set_reg(f_reg, f_value)
    
    # E-E
    
    elif (l[1][1] == l[2][1] || l[1][1] == l[2][2]):
        f_reg = l[1][1]
        f_value = buff_E_M_.get_reg(f_reg)
        buff_D_E_.set_reg(f_reg, f_value)

    # M-E

    elif (l[0][1] == l[2][1] || l[0][1] == l[2][2]):
        f_reg = l[0][1]
        f_value = buff_M_W_.get_reg(f_reg)
        buff_D_E_.set_reg(f_reg, f_value)

    