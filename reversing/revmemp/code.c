
void entry(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  undefined argc [8];
  undefined8 ptr;

  __libc_start_main(main,ptr,&stack0x00000008,do_code,ret,param_3,argc);
  do {
                    /* WARNING: Do nothing block with infinite loop */
  } while( true );
}


undefined8 main(int uno,long due)

{
  int outcome;
  char *ptr;

  protect_me();
  if (uno < 2) {
    puts("Gimme the flag!");
                    /* WARNING: Subroutine does not return */
    exit(-1);//This will be patched out
  }
  ptr = (char *)alloc_protc();
  protect_me();
  outcome = strncmp(ptr,*(char **)(due + 8),0x21);
  if (outcome == 0) {
    puts("You got the flag!");
  }
  else {
    puts("Wrong!");
  }
  return 0;
}


void protect_me(void)

{
  code *code_ptr;

  code_ptr = entry;
  while( true ) {
    if ((uint *)code_ptr == (uint *)0x101425) {
      return;
    }
    if (((*(uint *)code_ptr & 0xf0) == 0xc0) && ((*(uint *)code_ptr & 0xf) == 0xc)) break;
    code_ptr = (code *)((long)code_ptr + 1);
  }
  puts("do not play with me!");
                    /* WARNING: Subroutine does not return */
  exit(-1);//Thisd needs to be patched out !
}


/* WARNING: Instruction at (ram,0x0010128e) overlaps instruction at (ram,0x0010128d)
    */
/* WARNING: Removing unreachable block (ram,0x0010128d) */

void * alloc_protc(void)

{
  int number;
  void *mem_zone;
  int index;

  mem_zone = malloc(0x21);
  srand(0x1337);
  for (index = 0; index < 0x21; index = index + 1) {
    protect_me();
    number = rand();//It seems to me that we assign to mem_zone[index]
    *(undefined *)((long)mem_zone + (long)index) = PTR_DAT_si00104060[number % 0x539];
  }
  return mem_zone;
}


void do_code(undefined4 param_1,undefined8 param_2,undefined8 param_3)

{
  long index;

  _DT_INIT();
  index = 0;
  do {
    (*(code *)(&__DT_INIT_ARRAY)[index])(param_1,param_2,param_3);//this calls _INIT_1(void)
    index = index + 1;
  } while (index != 2);
  return;
}
void _INIT_1(void)

{
  long lVar1;

  lVar1 = ptrace(PTRACE_TRACEME,0,1,0);//you cannot attach with gdb
  if (lVar1 == -1) {
    puts("plz don\'t!");
                    /* WARNING: Subroutine does not return */
    exit(-1);//this will also be patched out
  }
  return;
}

void _DT_INIT(void)

{
  __gmon_start__();
  return;
}


void ret(void)

{
  return;
}
