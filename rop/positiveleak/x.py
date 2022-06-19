
from pwn import *
from getpass import *
import logging
import time
#context(log_level='debug')
context.terminal = ['tmux', 'splitw', '-h', '-F' '#{pane_pid}', '-P']

if len(sys.argv)==1:
    #REMOTE EXPLOIT
    site = "training.jinblack.it"
    port = 3003
    c =  remote(site,port)
    process = "./positiveleak"

else:
    script_name, debug = sys.argv

    host = "acidburn"

    ip = "127.0.0.1"

    category = "rop"
    proc = "positiveleak"
    path = "/challenges/"+category+"/"+proc+"/"
    #prt = int(input(" insert "+host+"'s port to connect to:"))
    prt = 3022
    #pwd = getpass("insert "+host+"'s password:")
    pwd = "0607991337"
    print("Connecting to "+host+" at "+ip+" to execute syscall")
    ssh_p = ssh(host,ip,password=pwd,port= prt)

    process = "."+path+proc

    gdbc = '''
               brva 0x148c
               c
           '''
    print(sys.argv)
    if ( debug == 'gdb') :
        c = gdb.debug( [process], ssh = ssh_p, gdbscript = gdbc )
    else:
        c = ssh_p.process(process)

c.interactive()
