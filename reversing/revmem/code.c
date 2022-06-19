

void entry(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  undefined argc [8];
  undefined8 func_ptr;

  __libc_start_main(main_?,func_ptr,&stack0x00000008,second_func,return_func,param_3,argc);
  do {
                    /* WARNING: Do nothing block with infinite loop */
  } while( true );
}

undefined8 main_?(int param_1,long param_2)

{
  int flag;
  char *ptr;

  if (param_1 < 2) {
    puts("Gimme the flag!");
                    /* WARNING: Subroutine does not return */
    exit(-1);
  }
  ptr = (char *)invoke_me();
  flag = strncmp(ptr,*(char **)(param_2 + 8),0x1e); //insert a breakpoint at this address
  if (flag == 0) {
    puts("You got the flag!");
  }
  else {
    puts("Wrong!");
  }
  return 0;
}


/* WARNING: Unknown calling convention yet parameter storage is locked */

void * invoke_me(void)

{
  void *ptr;
  byte number;
  int index;

  ptr = malloc(0x1e);
  number = 0;
  for (index = 0; index < 0x1e; index = index + 1) {
    *(byte *)((long)ptr + (long)index) = PTR_DAT_00104048[index] ^ number;//look it is XORING this stuff
    number = *(byte *)((long)ptr + (long)index);
  }
  return ptr;
}
/*
PTR_DAT_00104048                                XREF[1]:     invoke_me:00101193(R)
00104048 08 20 10        addr       DAT_00102008                                     = 66h    f
00 00 00
00 00

DAT_00102008                                    XREF[2]:     invoke_me:001011a2(R),
                                                             00104048(*)
00102008 66              ??         66h    f

*/
void second_func(undefined4 param_1,undefined8 param_2,undefined8 param_3)

{
  long bool;

  _DT_INIT();
  bool = 0;
  do {
    (*(code *)(&__DT_INIT_ARRAY)[bool])(param_1,param_2,param_3);
    bool = bool + 1;
  } while (bool != 1);
  return;
}

void return_func(void)

{
  return;
}
