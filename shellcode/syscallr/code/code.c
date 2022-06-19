
undefined8 main(void)

{
  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);
  puts(&sys_sprite);
  prog();
  return 0;
}
/*
mmap() creates a new mapping in the virtual address space of the calling process.
_void *addr: starting address for new mapping
             if addr== NULL then the kernel chooses a page aligned address @ which to create the mapping
_size_t length: specifies length of mapping
_int prot : specifies the desired memory protection of the mapping between:
            -PROT_EXEC ; -PROT_READ ; -PROT_WRITE ; PROT_NONE;
            A value of 7 means that we are "adding up" EXEC,READ,WRITE values ( if checked on manual these are constants for 3,2,1,0 ) we have full rights to exec,read,write
_int flags: determine whether updates to the mapping are visible to other processes mapping the same region, and whether updates are carried through to the underlying file.
        here it should be
        MAP_SHARED
        Share this mapping.  Updates to the mapping are visible to other processes mapping the same region, and (in the case of  file-backed
              mappings) are carried through to the underlying file.  (To precisely control when updates are carried through to the underlying file
              requires the use of msync(2).

        MAP_ANONYMOUS
           The  mapping is not backed by any file; its contents are initialized to zero.  The fd argument is ignored; however, some implementa‐
           tions require fd to be -1 if MAP_ANONYMOUS (or MAP_ANON) is specified, and portable applications should ensure this.  The offset ar‐
           gument should be zero.  The use of MAP_ANONYMOUS in conjunction with MAP_SHARED is supported on Linux only since kernel 2.4.

https://sites.uclouvain.be/SystInfo/usr/include/bits/mman.h.html
check it for further info
*/

void prog(void)

{
  code *j_table;

  //allocates 4096 bytes 
  j_table = (code *)mmap((void *)0x0,0x1000,7,0x21,-1,0);
  if (j_table == (code *)0xffffffffffffffff) {
    printf("mmap failed");
                    /* WARNING: Subroutine does not return */
    exit(-1);
  }
  get_shellcode(j_table);
  (*j_table)();
  return;
}

void get_shellcode(void *container)

{
  int threshold;

  puts("Send shellcode plz?");
  read(0,container,1000);
  threshold = 0;
  while( true ) {
    if (999 < threshold) {
      return;
    }
    if ((*(char *)((long)container + (long)threshold) == '\x0f') ||
       (*(char *)((long)container + (long)threshold) == '\x05')) break;
    threshold = threshold + 1;
  }
  puts("Nonono!");
                    /* WARNING: Subroutine does not return */
  exit(-1);
}
