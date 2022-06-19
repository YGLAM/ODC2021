/*
checksec ./positiveleak
  Arch:     amd64-64-little
  RELRO:    Partial RELRO
  Stack:    Canary found
  NX:       NX enabled
  PIE:      PIE enabled
ldd ./positiveleak
  linux-vdso.so.1 (0x00007fffe77a0000)
  libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f63ef067000)
  /lib64/ld-linux-x86-64.so.2 (0x00007f63ef26f000)
file  ./positiveleak:
  ELF 64-bit LSB pie executable, x86-64,
  version 1 (SYSV),
  dynamically linked,
  interpreter /lib64/ld-linux-x86-64.so.2,
  BuildID[sha1]=912d8a19701b361bef4557afa8276f5970156cc0, for GNU/Linux 3.2.0,
  not stripped
*/
/*
first execution :
I input three numbers : 1 2 3 I get as output
1
2
3
93928973750836  <-- this one is interesting, what is he exactly printing out ?
The print goes on with a hundred zeroes --> something else is going one here

I could try to enter as many numbers as it outputted and then +1 to see if I can overwrite something..  
*/
