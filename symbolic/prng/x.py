#Thought process
# Copy seedRand and m_seedRand in python
# Run proc on server and retrieve 1001st entry of array
# run locally until 1001st entry of your array coincides
# then extrapolate the seed that was used to get that value
#
#We need to get the value that fits all the constraints !
import z3
from IPython import embed

#state = [0]* 0x271
class State:
    def __init__(self):
        self.state = [0]*0x270
        self. index = 0

MAG = [ 0x0,0x9908b0df]#it is little endian please note you can find this in Mersenne Twister's page
#If(condition,if_true,if_false)
def mag(i):# i is the condition
    return z3.If(i== 0 , z3.BitVecVal(0x0,32) , z3.BitVecVal(0x9908b0df,32))
    #Without the BitVec casting then 0x0 would be an integer and z3 wouldn't know how to convert it to a BitVec
#def mag(i):
#    return MAG[i]
def print_state(s):
    for i in range( 0x270):
        print("%d\t%#x"%(i,s.state[i]))
#def seedRand(state,input):
#    state[0] = seed & 0xffffffff #masking ??
#    state[0x270] = 1  # we are reusing state+0x270 several times

#    while ((state[0x270] < 0x270) # sounds like a counter
#        state[state[0x270]] =state[state[0x270]-1] * 0x17b5)
#        state[0x270] = state[0x270] + 1
#    return input
def seedRand(s,i):
    s.state[0] = i & 0xffffffff #masking
    s.index = 1  # we are reusing state+0x270 several times

    while (s.index < 0x270): # sounds like a counter
        s.state[s.index] = ( s.state[s.index-1] * 0x17b5 ) & 0xffffffff
        s.index = s.index + 1
    return s

def genRandLong(s):
    if ((0x26f < s.index) or (s.index < 0)):
        if ((0x270 < s.index) or (s.index < 0)):
            seedRand(s,0x1105)

        for jj in range(0xe3):
            p1 = s.state[jj + 0x18d]
            #p2 = ((s.state[jj + 1] & 0x7fffffff) | (s.state[jj] & 0x80000000)) >> 1
            p2 = z3.LShR(((s.state[jj + 1] & 0x7fffffff) | (s.state[jj] & 0x80000000)), 1)

            p3 =  mag((s.state[jj + 1] & 1)) # the index at s.state[jj+1]&1 will either be 0 or 1
            s.state[jj] = (p1 ^ p2 ^ p3) & 0xffffffff
            ### the ampersand will surely get me a 32 bit number, other wise I'd get a 64 bit when shifting left
             #how do I debug this stuff ???
      ## let's try to split this line in several parts


## we have a symbolic value as INDEX of an array !! (ulong)((uint)state[local_14+1] ..&1)
        for jj in range(0xe3 , 0x26f):
            p1 = s.state[jj -0xe3]
            p2 = ((s.state[jj + 1] & 0x7fffffff | s.state[jj] & 0x80000000))# >> 1
            p2 = z3.LShR(p2,1) # faster correction
            p3 = mag((s.state[jj + 1] & 1))
            s.state[jj] = (p1 ^ p2 ^ p3) & 0xffffffff # the index at s.state[jj+1]&1 will either be 0 or 1

        p1 = s.state[0x18c]
        p2 = ((s.state[0] & 0x7fffffff )|( s.state[0x26f] & 0x80000000))# >> 1
        p2 = z3.LShR(p2,1)
        p3 = mag(s.state[0] & 1)
        s.state[0x26f] = (p1^ p2 ^ p3) & 0xffffffff
        s.index = 0

    int_addr = s.index
    s.index = int_addr + 1
    #u_long = (s.state[int_addr] ^ s.state[int_addr] >> 0xb ) & 0xffffffff NO SHIFT CORRECTION
    u_long = (s.state[int_addr] ^ z3.LShR(s.state[int_addr] , 0xb )) & 0xffffffff

    u_long =(u_long ^(u_long << 7) & 0x9d2c5680) & 0xffffffff
    u_long = (u_long ^(u_long << 0xf) & 0xefc60000 ) & 0xffffffff
    #rand_number =  (u_long ^ u_long >> 0x12 ) & 0xffffffff NO SHIFT CORRECTION
    rand_number =  (u_long ^z3.LShR( u_long , 0x12 )) & 0xffffffff

        ## please note that with the right shift z3 is dealing with a sign extension, what should be the first number ? 0 or 1 ? we need to change the right
        ## shifts as in z3 the behaviour of sign extension is NON standard
        ### we use z3.LShR
    return s, rand_number
print(z3.get_version_string())


seed = z3.BitVec('seed',32)#32bit symbolic variable
#seed = 0x30303030
#we are mixing stuff with different types !!!
s = State()
s = seedRand(s, seed)
for i in range(0,1000):
    s,n = genRandLong(s)
    #print(i, hex(n)) this cannot be done with a symbolic value (BitVecVal)
s,n = genRandLong(s)
#now we want to create a solver and add the constraints that n = the printed number from your session
#print(hex(n))

#print_state(s)
solver = z3.Solver()
#solver.add(n == 0xb8d144da)
solver.add(n == 0x4eec90d0)
embed()
### then do m = solver.check()


## how can I understand which algorithm it is ? I must look at the constants
# these are well known values !!
# in the solution I just search 0x9d2c5680 from genRandLong and I see that it comes from mt19937 Mersenne Twister generator
# it generates pseudo random 32-bit numbers with a state size of 19937 bits
