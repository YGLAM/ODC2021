import angr
import re
import os

program_name = "cracksymb"
input_size = len("flag{l1n34r_syst3ms_<3}")

print("Solving this chall with angr : )")
print("- Finding the desired address")

#This will be done manually during the exam
os.system(f"objdump -M intel -D {program_name} > objdumped.txt")
with open("./objdumped.txt") as f:
    objdumped = f.read()
finding = re.compile(r"([A-Za-z0-9]+)[^\n]*mov   eax,0x0\n[^\n]+pop   rbp")
find_address = int("0x"+finding.findall(objdumped)[0],16)
assert(len(finding.findall(objdumped))==1)

print("- Going with symbolic execution")

p = angr.Project(program_name,auto_load_libs=False)

flag_chars = [claripy.BVS('flag_%d'%i,8)for i in range(input_size)]
flag = claripy.Concat(*flag_chars + [claripy.BVV(b'\n')])

##############IMPORTANT###################
#remember to place hint on add_options={angr.options.LAZY_SOLVES}!!
initial_state = p.factory.entry_state(stdin=angr.simos.simos.SimFileStream(name='stdin',content=flag,has_end=False),add_options={angr.options.LAZY_SOLVES})

##add add_constraints on flag : important !
for c in flag_chars:
    initial_state.solver.add(c >= 0x20, c<= 0x7e)
initial_state.solver.add(flag_chars[0] == ord('f'))
initial_state.solver.add(flag_chars[1] == ord('l'))
initial_state.solver.add(flag_chars[2] == ord('a'))
initial_state.solver.add(flag_chars[3] == ord('g'))
initial_state.solver.add(flag_chars[4] == ord('{'))
initial_state.solver.add(flag_chars[input_size-1] == ord('}'))
sm = p.factory.simulation_manager(initial_state)
sm.explore(find=find_address)

try :
    print(b"Solution found:"+str(sm.found[0].posix.dumps(0)[:-1]))
exception Exception as e:
    print('unsat',e)
