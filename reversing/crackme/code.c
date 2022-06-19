//breakpoints
//when to call sigtrap = 0x111c or 0x11c
//breakpoint for continue in catch = 0x75a

void _start(undefined8 param_1,undefined8 param_2,undefined8 param_3){
  undefined stackArgs [8];
  undefined8 stack;

  __libc_start_main(main,stack,&stack0x00000008,__libc_csu_init,__libc_csu_fini,param_3,stackArgs);
  do {
                    /* WARNING: Do nothing block with infinite loop */
  } while( true );
}

undefined8 main(int uno,long due){
  code *code_ptr;
  undefined8 result;

  signal(5,catch_function);//per arrivare la devi attivare signal ( numero )
  if (uno < 2) {
    puts("USAGE: ./crackme FLAG!");
    return 1;
  }
  input = *(undefined8 *)(due + 8);
  code_ptr = (code *)swi(3);
  result = (*code_ptr)();
  return result;
}


void catch_function(void){
  long in_FS_OFFSET;
  int index;
  undefined8 *index_two;
  undefined8 k;
  undefined8 l;
  undefined4 m;
  undefined2 n;
  long canary;
  bool outcome;
  //What are these constants ?
  canary = *(long *)(in_FS_OFFSET + 0x28);
  outcome = true;
  k = 0x233f6b67232a2e12;//not found in google
  l = 0x6b32266b386c3f2a;//not found in google
  m = 0x2c2a272d;//not found in google
  n = 0x6a;//6a means j in ASCII and is = 106
  // input is also a global variable
  //key1 = 0x58 09 10 00 00 00 00 00 global variable  X ? ?
  //DAT_00100980 = 0x7f 0xef 0xe8 0xb5 0x15 0x73 0xb4 0x6a 0xa7 0x7d 0x48 0xdd 0xea 0x6a 0x9d 0xaa
  //           ... 0x82 0xfa 0x6e 0xe4 0xf6 0x23 0x9b 0xd9 0x78 0xab 0x1b 0x9b 0x16 0x96 0x9c 0x2e
  //           ... 0x6f 0xb2 0xc7 0x0c 0x17 0x00 0x00
  //index + input = 0x27 0xe6 0xf8
  //input = 0x27 0xe5 0xf6 .. cannot be converted to ascii..
  //input comes from = *(undefined8*)(due+8)
  for (index = 0; key1[index] != '\0'; index = index + 1) {//does it stop after 3 iterations ?
    if ((*(byte *)(index + input) ^ key1[index]) != (&DAT_00100980)[index]) {
      outcome = false;//The XOR needs to be different from DAT
    }
  }
  for (index_two = &k; *(byte *)index_two != 0; index_two = (undefined8 *)((long)index_two + 1)) {
    *(byte *)index_two = *(byte *)index_two ^ 0x4b;//then I XOR index two with 0x4b
     //but please keep in mind that I'm XORING the address of k
  }
  if (outcome) {
    puts((char *)&k);//then I'd print it !
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  if (canary != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
