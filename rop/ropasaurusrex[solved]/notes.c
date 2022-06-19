/*
libs are included only if needed
you can id the libc just by computing the offset between two functions @libc_db
you can use a leak to get those addresses
pwntools does this if you give it an arbitrary read to start with
 Ropasaurus is 32 bit
 ldd <filename> checks which library is being loaded !
 the libs differ from the one which is provided (check sha1sum on provided + ls -lsha <lib> to see hashes and diff them)

 If there is no main check for entry and that will provide you the true main
 we can write whatever we want on the stack but please note that NX IS ACTIVE

 To find a GOT table;
  .go to a read function
  . right click -> preferences -> references to function
  . check all the references

  we would like to jump to a magic gadget to open a bin/sh
  We need to know libc position knowing that .text is not randomized

  On the stack there will be surely , but how do we find it? It is randomized...
  the GOT will surely have it and since this binary is NOT PIE  then
  the code is not randomized !


  TO SEE HOW DEEP WE ARE IN THE STACK USE
  cyclic -n 4 200   32 bit so 4 bit cycle of 200 iterations(?)

  THEN TO GET PRECISE DEPTH SEE WHAT IS THE ADDRESS YOU RECEIVE AND DO
  cyclic -n 4 -l 0x626161616b it will tell @ which number he is

  so to jump to our addr just plant a shellcode with #bytes ->output of 2nd cyclic + your addr of choice

  in order to leak libc's addr we jump inside the write function inside the addr in the got
  in the payload you'll input
  function -> gadget -> parameteres of function

  why do we use p32 (?) to pass as 32 bit sequence

  ... see xr.py for ref...
  now we want to check how the stack frame looked like when exiting
  overflow , we'll do so through ghidra
  we'll go to overflow, then click on return to see its address
  we'll use it as a gdb breakpoint !


   when inspecting the gdb you can see that
   AFTER  returning it calls 0x080482ec , that is the LOADER for the write
   bcs it is the 1st time doin the write

   WE'LL GET .\xec\xf7 printed right before going interactive
   use vmmap to inspect memory
   you'll find libc's addr @ 0xf7ddc000 and 0xf7fb100

   so we reason that .\xec\xf7 is inside libc

    now that we know this we can get addr of magic byte


    ALTERNATIVE METHOD TO GET WRITE'S ADDR WITHOUT GHIDRA
    :  objdump -d -M intel ./ropasaurusrex \ grep write
    grep -C 4 write gives you more context
*/
