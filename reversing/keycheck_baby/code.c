
void _start(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  undefined stack_array [8];
  undefined8 arg;
//stack0x00000008 seems 8 bytes after the stack ?
  __libc_start_main(main,arg,&stack0x00000008,__libc_csu_init,__libc_csu_fini,param_3,stack_array);
  do {
                    /* WARNING: Do nothing block with infinite loop */
  } while( true );
}


void __libc_csu_init(EVP_PKEY_CTX *uno,undefined8 due,undefined8 tre)
{
  long index;

  _init(uno);
  index = 0;
  do {//__frame_dummy_init_array_entry is found at 0x00103de8
    (*(code *)(&__frame_dummy_init_array_entry)[index])((ulong)uno & 0xffffffff,due,tre);
    //it loads the function @ frame_dummy[index] and passes only the first 4 bytes of uno, alongside due and tre
    index = index + 1;
  } while (index != 1);
  return;
}

int _init(EVP_PKEY_CTX *ctx)
{//ctx is never actually used (??)
  int start_var;

  start_var = __gmon_start__();
  return start_var;
}


void __gmon_start__(void){
  /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();//ghidra doesn't reach any function here, what does it mean that it is a bad instruction ?
}


void __libc_csu_fini(void){  return; } //self explanatory return function..


undefined8 main(void)
//It seems that we will have to patch out all the sleeps and the stack_check_fail
//Where does LAB_00101487 go to ?
//What are magic0 and magic1 ?
{
  int cmp_outcome;
  size_t mem_length;
  long in_FS_OFFSET;
  char offset;
  uint index;
  undefined8 stack_addr;
  char mem_zone [5];
  byte stack_array [99];//this is UNINITIALIZED !!!
  long canary;

  canary = *(long *)(in_FS_OFFSET + 0x28);
  memset(mem_zone,0,100);
  fwrite("flag> ",1,6,stdout);
  fgets(mem_zone,100,stdin);//saves your input into mem_zone, please note that it is only 5 bytes !!!!
  //This is easily overflowable
  puts("\n\nI\'m just a crackme, nobody solves me");
  mem_length = strlen(mem_zone);
  if (mem_zone[mem_length - 1] == '\n') {
    mem_length = strlen(mem_zone);
    mem_zone[mem_length - 1] = '\0';//it puts a terminator into the string, can I do a 1 byte overflow ?
  }
  cmp_outcome = strncmp(mem_zone,"flag{",5);
  if (cmp_outcome == 0) {
    puts("He\'s just a poor n00b, from a poor ctf team");
    mem_length = strlen(mem_zone);
    if (mem_zone[mem_length - 1] == '}') {//If the penultimate is }
      puts("Spare him his life from this engineering");
      stack_addr = stack_array;//this thing is pointing to that 
      for (index = 0; index < 0xd; index = index + 1) {
        if ((byte)(stack_addr[(int)index] ^ "babuzz"[(ulong)(long)(int)index % 6]) !=
            magic0[(int)index]) goto LAB_00101487;
      }
      puts("Easy rev");
      usleep(500000);
      puts("Easy crack");
      usleep(500000);
      puts("Will you let me solve?");
      usleep(500000);
      stack_addr = stack_addr + 0xd;
      offset = -0x45;
      for (index = 0; index < 0xc; index = index + 1) {
        offset = offset + *stack_addr;
        stack_addr = stack_addr + 1;
        if (offset != magic1[(int)index]) goto LAB_00101487;
      }
      puts("Use Ghidra!");
      stack_addr = stack_addr + 1;
      if (*stack_addr == 0) {
        for (index = 0; (int)index < 10; index = index + 1) {
          usleep(200000);
          putc(0x2e,stdout);
          fflush(stdout);
        }
        puts("\n\n\n\n");
        usleep(500000);
        puts("Apparently we let go (:");
        puts("Your input looks like the correct flag \\(^o^)/");
      }
    }
  }
LAB_00101487:
  if (canary == *(long *)(in_FS_OFFSET + 0x28)) {
    return 0;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}
