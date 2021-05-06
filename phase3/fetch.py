def fetch(mem_mod, reg_mod, l, cache_ob, gui_util_obj):
    # inst = mem_mod.lw(reg_mod.get_PC())
    PC = reg_mod.get_PC()
    inst = cache_ob.read(hex(PC), mem_mod, "Fetch", gui_util_obj)

    tag, set_no, bo = cache_ob.decode_address(hex(PC))
    copy_set = cache_ob.cache_array[set_no][:]

    temp = ["Fetch", hex(PC), set_no, copy_set]
    gui_util_obj.task2.append(temp)
    tag = None
    set_no = None
    bo = None

    temp = []

    reg_mod.set_IR(inst)
    l.append("FETCH: Fetch instruction " + reg_mod.get_IR() + " from address " + hex(reg_mod.get_PC()))
    reg_mod.add_PC(4)
