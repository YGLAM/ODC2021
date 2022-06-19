from angr import *
import claripy
KEY_LENGTH = 29

proj = Project('./prodkey')
key = [claripy.BVS('c{}'.format(i),8) for i in range(KEY_LENGTH)]
input_str = claripy.Concat(*key + [claripy.BVV(b'\n')])
state = proj.factory.entry_state(stdin = input_str)

for c in key:
	state.solver.add(c >= 0x20, c <= 0x7e)

simgr = proj.factory.simgr(state)

simgr.explore(find = 0x00400e58)

if simgr.found:
	found = simgr.found[0]
	print(found.posix.dumps(0))
