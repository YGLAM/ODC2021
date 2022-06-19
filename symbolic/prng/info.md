`$ file pnrg`

pnrg ELF 64-bit LSB pie executable,

       x86-64,

       version 1 (SYSV), dynamically linked,

       interpreter /lib64/ld-linux-x86-64.so.2,

       for GNU/Linux 3.2.0,

       BuildID[sha1]=db02aa9909b2f51a61206f4fa67
       2d97a0295000e, not stripped

### What is a non stripped binary?
We can remove the name of the functions, in this case we are not doing it, officially it is done to reduce the size of the binary,in reality make it harder to read


`$ ./pnrg`

0x5b210c83, guess the seed:

$ 0

your guess was 0, seed was 0x40a2c1e0. Bye!


`$ ltrace ./pnrg`

open("/dev/random",0,020432212250)= 3

read(3,"\024E_<",4)= 4

close(3)= 0

printf("%#lx,",0xa2ae50f9) = 12

puts("guess the seed:"0xa2ae50f9, guess the seed:)= 16

read(0, "\n",99)= 1

strtoul(0x7ffd84691330, 0, 0,0x7fd535679b82)= 0

printf("your guess was %#x, seed was %#x"...,0,0x3c5f4514)= 43

your guess was 0, seed was 0x3c5f4514. Bye!

+++ exited (status 0) +++


One would be tempted to run it with angr but it would be a dead end

we could re-implement the randomic value generator function in python and write a program that let us try for thousands of times 
