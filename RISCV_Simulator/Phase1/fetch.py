def fetch(mem_mod, reg_mod, l):
    inst = mem_mod.lw(reg_mod.get_PC())
    reg_mod.set_IR(inst)
    l.append("FETCH: Fetch instruction " + reg_mod.get_IR() + " from address " + hex(reg_mod.get_PC()))
    reg_mod.add_PC(4)
