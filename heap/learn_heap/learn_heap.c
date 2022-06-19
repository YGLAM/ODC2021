/*
The heap is a memory area used for dynamic allocation, meaning that it allocates
an amount of space which isn't known at compile time!
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void main(void){
  char *ptr;

  ptr = malloc(0x10);
  strcpy(ptr,"panda");
}
//Whenever we call a malloc it will return a POINTER to a CHUNK
//Let's see the memory of the heap chunk here:

─────────────────────────────────────────────────────────────── code:x86:64 ────
   0x55555555514b <main+22>        mov    rax, QWORD PTR [rbp-0x8]
   0x55555555514f <main+26>        mov    DWORD PTR [rax], 0x646e6170
   0x555555555155 <main+32>        mov    WORD PTR [rax+0x4], 0x61
 → 0x55555555515b <main+38>        nop
   0x55555555515c <main+39>        leave
   0x55555555515d <main+40>        ret
   0x55555555515e                  xchg   ax, ax
   0x555555555160 <__libc_csu_init+0> push   r15
   0x555555555162 <__libc_csu_init+2> mov    r15, rdx
─────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "try", stopped, reason: BREAKPOINT
───────────────────────────────────────────────────────────────────── trace ────
[#0] 0x55555555515b → main()
────────────────────────────────────────────────────────────────────────────────
gef➤  search-pattern panda
[+] Searching 'panda' in memory
[+] In '[heap]'(0x555555559000-0x55555557a000), permission=rw-
  0x555555559260 - 0x555555559265  →   "panda"
gef➤  x/4g 0x555555559250
0x555555559250:    0x0    0x21
0x555555559260:    0x61646e6170    0x0

/*0x555555559250 here is our heap chunk, everyone of those has something called
  the HEAP HEADER( or METADATA), in x64 its the previous 0x10 bytes from the
  start of the heap chunk, while on x86 systems it's the previous 0x8 bytes.
  It contains TWO SEPARATE VALUES:
*/
0x0:    0x00        - Previous Chunk Size
0x8:    0x21        - Chunk Size
0x10:   "panda"     - Content of chunk

/*The Previous chunk size(which ISN'T SET HERE) designates the size of the previous
  chunk in the heap layout that HAS BEEN FREE'D. Here the heap size is 0x21

*/
/*What is a bin ? It is a POINTER which holds an account of free chunks of a particular size,
  whenever a chunk is free'd it stays put in memory but gets 'enumerated' and 'added' to a bin
  Free'd chunks are assigned to different ways of being dealt with according to their size.
  There are
  -Fastbins : -maintains a list of freed chunks whose size vary from 16 to 88 bytes
              -singly linked list LIFO
              -a newly freed chunk is always added to the TOP of the fastbin
              -there are 10 fastbins for sizes (16,24,32,40,488,56,64,72,80,88)
              -the "next" pointer is in the USER DATA section of the chunk itself
              -no chunk coalescing happens here
  -Small bins:-hold freed chunk whose size vary from 16 to 512 bytes, there are 62 of them
              -circular double linked list FIFO
              -FD and BK pointers are stored in the USER DATA section of each chunk
              -When adding a new chunk its FD will point to the head of the list
              - One natural question that might pop here is: “The ranges of fastbin and small bin
                COINCIDE, so how does malloc know where to send the freed chunk?”
                I don’t know and wasn’t able to find an answer,
  -Large bins:-62 bins holding chunks of size greater than 512 bytes
              -Circular doubly linked list, addition can happen anywhere
              -each bins don't necessarily hold chunks of the same size, rather,there's
               a range size for each bin:
                -First 32 bins contain chunks in a 64byte range, 512.568,576-632 etc..
                -then 16 bins contain chunks in a 512 byte range
                -then 8 for the 4096byte range
                -then 4 for the 32768byte range
                -then 2 for the 262144byte range
                -the remaining bin for all the bigger ones
              -chunks are stored in DESCENDING order, this is why insert/delete happens
               in arbitrary order, which makes the malloc slow
              -ALL large bins point to NULL (instead of the head)
              -coalescing can occur
   -Unsorted bins:
              -It is just 1 bin, when a NON-fast chunk is freed it is then put
               into the unsorted bin. This gives it a chance to be reused without
               too much malloc overhead.
               Whenever a malloc call occurs, it first goes through this bin to see
               if a chunk with its required sizing is here it takes it, if NOT it
               runs the SORTING algorithm to place all chunks in the unsorted bin
               in their respective bins
The MAIN ARENA :
    Where the original heap segment lies,created when the user makes a call to malloc for
    the first time in a program: A heap memory of 132KB is created from which the memory
    of the desired size is serviced. Subsequent calls for allocation allocate memory
    from this region till it runs out.
    Upon running out a "brk" syscall is done,giving us a new segment (heap) itself
    The top chunk is ALWAYS maintained in the heap CURRENTLY in use.
    It is useful to keep track of the top chunk in order to know which heap is in
    use, and which bins are already full.
    Whenever more than 128KB are requested a call to mmap occurs

The T-CACHE :
    Its purpose ? Optimization, in order for a thread to access a particular MAIN ARENA
    without having to get a lock on it we create a PER-THREAD cache to collect chunks
    accessible without having to lock an arena.
    Structurally , tcache = fastbin : -Singly linked list of same size chunks
                                      -1 bin each from 16 to 88 bytes
                                      -there's a tcache_count var to limit #chunks per bin
                                      -the linked list points to the USER-CONTROLLED chunks area,
                                       not the chunk's real beginning (0x10 bytes ahead,or 0x8)
                                      -IF the bin for a particular size is empty then malloc:
                                        locks an arean, looks into the unsorted bins rather than
                                        taking the next larger chunks
                                      - TCACHE CHUNKS DO NOT COALESCE !!!
*/

/*
  Please note that the bin heads are located in the main arena, more specifically in the
  .bss of the libc;
  Any freed chunk bigger than 0xA0 bytes ends up in the unsorted bin, when a chunk there is not able
  to satisfy a malloc, the chunk is then moved to the appropriate small or large bin
*/
