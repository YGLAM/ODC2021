import claripy
import angr

find_address = 0x4033BB
avoid_address = 0x4033c9
p = angr.Project('cracksymb')
flag = claripy.BVS('flag',0x17*8)

st = p.factory.efull_init_state(args=['./cracksymb'],add_options={angr.option.LAZY_SOLVES},stdin=angr.simos.simos.SimFileStream(name='stdin',content=flag,has_end=False))

#for byte in flag.chop(8):
#   st.add_constraints(byte >= 0x21)
#   st.add_constraints/byte <= 0x7e)

sm = p.factory.simulation_manager(st)

sm.explore(find=find_address)#,avoid = avoid_address)

try :
    p = sm.[0]
    sol = p.solver.eval(flag,cast_to = bytes)
    print(b"Solution found:"+sol)
exception Exception as e:
    print('unsat',e)
