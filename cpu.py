class cpu_registers:
    a = 0
    f = 0
    b = 0
    c = 0
    d = 0
    e = 0
    h = 0
    l = 0
    pc = 0
    sp = 0

class cpu_context:
    fetch_data = 0
    mem_dest = 0
    cur_opcode = 0
    halted = False
    stepping = False

def cpu_init():
    pass

def cpu_step():
    pass