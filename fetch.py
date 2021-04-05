def fetch(mem_mod, reg_mod):
    inst = mem_mod.lw(reg_mod.get_PC())
    reg_mod.set_IR(inst)
    reg_mod.add_PC(4)
    
