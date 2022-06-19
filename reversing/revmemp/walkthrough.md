The first thing I did was to locate all the checks, then I noticed how the function _INIT_1 was loaded
despite not being directly reachable

I've noticed all the exit(-1) calls that interrupt the strace and patched them out using ghex
after that I've noticed that the strace calls ended with a SIGSEGV as such I've switched to gdb

and run it with a brva @ the first address of the main to check what happened
It wasn't useful to investigate further as the flag gets loaded in memory in the RAX register during
the call to alloc_protc 
