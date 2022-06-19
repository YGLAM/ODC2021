The first thing we do is to simply run the program through
./keycheck_baby

flag> (I_dunno_guess_it) <- this is my input


I'm just a crackme, nobody solves me

After that I use
strace ./keycheck_baby

execve("./keycheck_baby", ["./keycheck_baby"], 0x7fffb0b2c690 /* 78 vars */) = 0
brk(NULL) = 0x55e280351000
arch_prctl(0x3001 /* ARCH_??? */, 0x7fff29266120) = -1 EINVAL (Invalid argument)
access("/etc/ld.so.preload", R_OK) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
newfstatat(3, "", {st_mode=S_IFREG|0644, st_size=84870, ...}, AT_EMPTY_PATH) = 0
mmap(NULL, 84870, PROT_READ, MAP_PRIVATE, 3, 0) = 0x7f26fcf1b000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\240\206\2\0\0\0\0\0"..., 832) = 832

pread64(3, "\6\0\0\0\4\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0"..., 784, 64) = 784
pread64(3, "\4\0\0\0 \0\0\0\5\0\0\0GNU\0\2\0\0\300\4\0\0\0\3\0\0\0\0\0\0\0"..., 48, 848) = 48
pread64(3, "\4\0\0\0\24\0\0\0\3\0\0\0GNU\0+H)\227\201T\214\233\304R\352\306\3379\220%"..., 68, 896) = 68

newfstatat(3, "", {st_mode=S_IFREG|0755, st_size=1983576, ...}, AT_EMPTY_PATH) = 0
mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f26fcf19000

pread64(3, "\6\0\0\0\4\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0"..., 784, 64) = 784
mmap(NULL, 2012056, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x7f26fcd2d000
mmap(0x7f26fcd53000, 1486848, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x26000) = 0x7f26fcd53000

mmap(0x7f26fcebe000, 311296, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x191000) = 0x7f26fcebe000

mmap(0x7f26fcf0a000, 24576, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1dc000) = 0x7f26fcf0a000

mmap(0x7f26fcf10000, 33688, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x7f26fcf10000

close(3)                                = 0

mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f26fcd2b000
arch_prctl(ARCH_SET_FS, 0x7f26fcf1a580) = 0

mprotect(0x7f26fcf0a000, 12288, PROT_READ) = 0
mprotect(0x55e27f150000, 4096, PROT_READ) = 0
mprotect(0x7f26fcf62000, 8192, PROT_READ) = 0
munmap(0x7f26fcf1b000, 84870)           = 0
newfstatat(1, "", {st_mode=S_IFCHR|0620, st_rdev=makedev(0x88, 0), ...}, AT_EMPTY_PATH) = 0
brk(NULL)                               = 0x55e280351000
brk(0x55e280372000)                     = 0x55e280372000
newfstatat(0, "", {st_mode=S_IFCHR|0620, st_rdev=makedev(0x88, 0), ...}, AT_EMPTY_PATH) = 0
write(1, "flag> ", 6flag> )                   = 6
read(0, keycheckbaby
"keycheckbaby\n", 1024)         = 13
write(1, "\n\n", 2

)                     = 2
write(1, "I'm just a crackme, nobody solve"..., 37I'm just a crackme, nobody solves me
) = 37
exit_group(0)                           = ?
+++ exited with 0 +++

Nothing interesting is seen at first with the strace , let's try
ltrace ./keycheck_baby

  memset(0x7ffc33b36b50, '\0', 100)            = 0x7ffc33b36b50
  fwrite("flag> ", 1, 6, 0x7f6ec02e46c0)       = 6
  fgets(flag> keycheck_babeeee
  "keycheck_babeeee\n", 100, 0x7f6ec02e39a0) = 0x7ffc33b36b50
  puts("\n\nI'm just a crackme, nobody sol"...

  I'm just a crackme, nobody solves me  ) = 39
  strlen("keycheck_babeeee\n")                 = 17
  strlen("keycheck_babeeee\n")                 = 17
  strncmp("keycheck_babeeee", "flag{", 5)      = 5
  +++ exited (status 0) +++

here we can see an interesting strncmp, is it comparing only the first 5 chars ? Yes, the last parameter
is "num" and it is the maximum number of chars to compare

What happens if I write "flag{" ???? Something cool happens , here's the diff with the initial ltrace

  trncmp("flag{keycheck_babeeee}", "flag{", 5) = 0
  puts("He's just a poor n00b, from a po"...He's just a poor n00b, from a poor ctf team)  = 44
  strlen("flag{keycheck_babeeee}")             = 22
  puts("Spare him his life from this eng"...Spare him his life from this engineering )  = 41
+++ exited (status 0) +++

Nothing of interest can be seen with the strace, let's inspect the code
...
After having patched out all the sleeps we thought we could go and inspect with ltrace and find the puts("Easy rev") but this isn't the case, as we are jumping to LAB_00101487

I have to also patch this thing out , but first let me inspect with gdb to see if something unexpected happens
It seems that the problem is found at
JZ LAB_0010149b that lets me do a LEAVE and RET,
I have to avoid jumping to LAB_00101487, I cannot simply patch out the LEAVE and RET since the control flow doesn't bring me back there
I'll patch out
goto LAB_00101487

All those patches were useless as we didn't need to bypass anything, we just needed to understand how the algorithm worked, as such we examined both the contents of magic0 and magic1

Also please note that "babuzz"[(ulong)(long)(int)index] referred to the single digits of the word "babuzz" and not something pointed by an hypothetical babuzz array

after that the first part of the flag is obtained by simply XORing the contents of magic0 with "babuzzbabuzz" (please note the module of 6)  we can move on to the second part,

please note that we are not required to add 0xbb ( as seen on Ghidra ) instead we have to subtract
the SUCCESSIVE byte with the result of the PREVIOUS BYTE , but we start with 0xeb - 0xbb
(please note that this DOESN'T WORK with the successive but resumes working the next one, summation is simpler yet more tedious)
