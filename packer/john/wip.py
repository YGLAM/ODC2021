import sys

if len(sys.argv) < 4 :
    print("usage :%s <inputfile> <address> <size> <offset>" %sys.argv[0])
    exit(0)
filepath = sys.argv[1]
address = int(sys.argv[2],16)
size = int(sys.argv[3],16)

#offset = sys.argv[4] we probs don't need it
#KEY = [ 0x01020304, 0x10203040, 0x42303042, 0x44454144, 0xffffffff] # Those are the keys we've.. (errata corrige) check the endianess !
KEY = [ 0x04030201, 0x40302010, 0x42303042, 0x44414544,0xffffffff]# errata corrige , last key is not 0xffffffff but 0x34a0...
#found at PTR_DAT etc etc
ff=open(filepath,"rb")
f = ff.read()
ff.close()

off = address - BEG_BIN
to_decode = f[off:off+size]
## check uint , we see that cur_ptr should go +4 and not +1
k = KEY[address % 5]

for i in range(size):
    decode += p32(u32(to_decode[i*4: (i+1)*4] )^ k) #we are cycling current_ptr and doing the xor

f = f[:off] + decode + f[off+(size*4): ]

ff = open(filepath , "wb")
ff.write(f)
ff.close()
## This will unpack the first function with ./john 0x0804970e 0x53
## You'll open it again with ghidra and you'll find a new unpacked function , revealing 5 more checks !!
## You'll now take all the function addresses and their respective sizes ( you can find them in the first unpacked function )

# But of fucking course not all the functions are unpacked !!
# We'll check again the original and see where the jump happens
# 0x8049329 the bytes are not right so there could be a problem with the key !
# The problem is the endianess !!
