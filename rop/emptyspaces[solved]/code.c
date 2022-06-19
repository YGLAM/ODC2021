void _start(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  undefined ar_args [8];
  undefined8 arg_one;

  __libc_start_main(main,arg_one,&stack0x00000008,__libc_csu_init,__libc_csu_fini,param_3,ar_args);
  do {
                    /* WARNING: Do nothing block with infinite loop */
  } while( true );
}

undefined8 main(void)

{
  undefined string [64];

  setvbuf((FILE *)stdin,(char *)0x0,2,0);
  setvbuf((FILE *)stdout,(char *)0x0,2,0);
  puts("What shall we use\nTo fill the empty spaces\nWhere we used to pwn?");
  read(0,string,0x89);
  empty(string);//buff overflow here !
  return 0;
}

void empty(long string)

{
  int i;

  for (i = 0; i < 0x12; i = i + 4) {
    *(undefined4 *)(string + (long)i * 4) = 0xc3f48948;//writes something on the stack
  }
  return;
}
