$ file revmem

/*revmem:
  ELF 64-bit LSB pie executable,
  x86-64,
  version 1 (SYSV),
  dynamically linked,
  interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0,
  BuildID[sha1]=c37fc2fdcd8b9c8c1d9a1690b4bda27dc165c4d6,
  stripped*/

$ strace ./revmem asdasd

  execve("./revmem", ["./revmem", "asdasd"], 0x7ffee6d1d148 /* 71 vars */) = 0
  brk(NULL) = 0x55a175eba000

  arch_prctl(0x3001 /* ARCH_??? */, 0x7ffec0829ad0) = -1 EINVAL (Invalid argument)
  access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
  openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
  newfstatat(3, "", {st_mode=S_IFREG|0644, st_size=84178, ...}, AT_EMPTY_PATH) = 0
  mmap(NULL, 84178, PROT_READ, MAP_PRIVATE, 3, 0) = 0x7f53db28f000
  close(3)= 0

  openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
  read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\240\206\2\0\0\0\0\0"..., 832) = 832
  pread64(3, "\6\0\0\0\4\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0"..., 784, 64) = 784
  pread64(3, "\4\0\0\0 \0\0\0\5\0\0\0GNU\0\2\0\0\300\4\0\0\0\3\0\0\0\0\0\0\0"..., 48, 848) = 48
  pread64(3, "\4\0\0\0\24\0\0\0\3\0\0\0GNU\0+H)\227\201T\214\233\304R\352\306\3379\220%"..., 68, 896) = 68
  newfstatat(3, "", {st_mode=S_IFREG|0755, st_size=1983576, ...}, AT_EMPTY_PATH) = 0
  mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f53db28d000
  pread64(3, "\6\0\0\0\4\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0"..., 784, 64) = 784

  mmap(NULL, 2012056, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x7f53db0a1000
  mmap(0x7f53db0c7000, 1486848, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x26000) = 0x7f53db0c7000
  mmap(0x7f53db232000, 311296, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x191000) = 0x7f53db232000
  mmap(0x7f53db27e000, 24576, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1dc000) = 0x7f53db27e000
  mmap(0x7f53db284000, 33688, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x7f53db284000
  close(3)= 0

  mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f53db09f000
  arch_prctl(ARCH_SET_FS, 0x7f53db28e580) = 0

  mprotect(0x7f53db27e000, 12288, PROT_READ) = 0
  mprotect(0x55a174f56000, 4096, PROT_READ) = 0
  mprotect(0x7f53db2d6000, 8192, PROT_READ) = 0
  munmap(0x7f53db28f000, 84178)           = 0
  brk(NULL)                               = 0x55a175eba000
  brk(0x55a175edb000)                     = 0x55a175edb000
  newfstatat(1, "", {st_mode=S_IFCHR|0620, st_rdev=makedev(0x88, 0), ...}, AT_EMPTY_PATH) = 0
  write(1, "Wrong!\n", 7Wrong!)  = 7
  exit_group(0)                           = ?
+++ exited with 0 +++

$ strace ./revmem asdasd

malloc(30)                                   = 0x560a8138b2a0
strncmp("flag{this_was_an_easy_reverse}", "asdasd", 30) = 5
puts("Wrong!"Wrong!
)                               = 7
+++ exited (status 0) +++
