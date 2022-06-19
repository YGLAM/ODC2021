 //we could try to look at the strncmp in main and put a brva there

// brva 0x136d

// but upon continue I'll get
/*
Continuing.
plz don't!
[Inferior 1 (process 53280) exited with code 0377]
*/

//but I don't see any "plz don't" string in my code..
//Where could they be ?

//in Ghidra do a search Memory to find it

//Location :: 00102557
//Label :: s_plz_don't!..
//Code Unit :: ds "plz don't!"

//Then check the references to this string

//Location :: 001012ea
//Label :: ...
//Code Unit :: LEA RDI,[s_plz_don't]..
//context :: DATA

//I'll see from the decompiled code that this belongs to a function that wasn't there to begin with

void _INIT_1(void)

{
  long lVar1;

  lVar1 = ptrace(PTRACE_TRACEME,0,1,0);//you cannot attach with gdb
  if (lVar1 == -1) {
    puts("plz don\'t!");
                    /* WARNING: Subroutine does not return */
    exit(-1);
  }
  return;
}

//or was it ? If we check the references then we'll find a CALL qword that is present in...

//void do_code !!!



void do_code(undefined4 param_1,undefined8 param_2,undefined8 param_3)

{
  long index;

  _DT_INIT();
  index = 0;
  do {
    (*(code *)(&__DT_INIT_ARRAY)[index])(param_1,param_2,param_3);//here !!!
    index = index + 1;
  } while (index != 2);
  return;
}

// so what do I do ?
//How do you catch syscalls if you are not attached?
//we modify the binary by punching OUT all of _INIT_1
// that's a bit exaggerated, instead
// you can go at the address of exit
// 0x001012fb and sub the 5 bytes of CALL <EXTERNAL>::exit with 5 nops

//another point

void protect_me(void)

{
  code *code_ptr;

  code_ptr = entry;
  while( true ) {
    if ((uint *)code_ptr == (uint *)0x101425) {//If this is false it will get OUT of the while
      return;
    }
    if (((*(uint *)code_ptr & 0xf0) == 0xc0) && ((*(uint *)code_ptr & 0xf) == 0xc)) break;//this looks
    code_ptr = (code *)((long)code_ptr + 1);
  }
  puts("do not play with me!");
                    /* WARNING: Subroutine does not return */
  exit(-1);//This one needs to be patched out !
}

//code_ptr is the program's entry

//idea 2 : we could modify the check to 0x101425 as to invalidate it somehow
