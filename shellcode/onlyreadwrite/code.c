
bool main(void)

{
  int flag;

  alarm(2);//delivers a signal in 2 seconds !
  flag = install_syscall_filter();
  if (flag == 0) {
    setvbuf(stdin,(char *)0x0,2,0);
    setvbuf(stdout,(char *)0x0,2,0);
    puts(
        "  _________.__           .__  .__                   .___      \n /   _____/|  |__   ____ |  | |  |   ____  ____   __| _/____  \n \\_____  \\ |  |  \\_/ __ \\|  | |  | _/ ___\\/  _ \\ / __ |/ __ \\ \n /        \\|   Y  \\  ___/|  |_|  |_\\  \\__(  <_> ) /_/ \\  ___/ \n/_______  /|___|  /\\___  >____/____/\\___  >____/\\____ |\\___  >\n        \\/      \\/     \\/               \\/           \\/    \\/ \n\n\n"
        );
    prog();
  }
  return flag != 0;
}

undefined8 install_syscall_filter(void)
//First idea, couldn't we somehow open the file flag and dump it somewhere ?
// use syscall --> open
// then use syscall -->write to write the flag into some var then
// maybe print it somewhere ?
{
  int number;
  int *error_flag;
  long long_n;
  undefined8 *explorer;
  undefined8 *placeholder;
  undefined2 string [4];
  undefined8 *pointer;
  undefined8 name[18];

  explorer = &global_var;//?
  placeholder = name;//placeholder points to 18 bytes
  //0x11 = 17
  for (index = 0x11; index != 0; index--) {
    *placeholder = *explorer;
    explorer = explorer + 1;
    placeholder = placeholder + 1;
  }
  string[0] = 0x11;
  pointer = name;

  /*
  Ops on a thread
   int option = 0x26 == 38  #define PR_SET_NO_NEW_PRIVS operations granting new privileges WILL either fail or not be granted!
   unsigned long arg2 = 1   promises that execve() WON'T grant privileges to do anything that could not have been done without the execve()call,
                            CANNOT BE UNSET!!! It is inherited by any children !
   unsigned long arg3 = 0
   unsigned long arg4 = 0
   unsigned long arg5 = 0

   https://github.com/torvalds/linux/blob/master/include/uapi/linux/prctl.h
  */
  number = prctl(0x26,1,0,0,0);
  if (number == 0) {//if it succeeds it returns 0
    //check out https://github.com/torvalds/linux/blob/master/include/uapi/linux/seccomp.h for arg2 options
    /*int option = 0x16 == 22 #define PR_SET_SECCOMP set the secure computing mode for the calling thread, to limit available syscalls
      arg2 = #define SECCOMP_MODE_FILTER uses user-supplied filter. Syscalls allowed are defined by a pointer to a Berkely packet filter passed in arg3
      arg3 = string !!! it is a POINTER to struct sock_fprog
    */
    number = prctl(0x16,2,string); //what is inside string ?? the first byte is set to 0x11 == 17, the others are not set ....
    //
    if (number == 0) {
      return 0;
    }
    perror("prctl(SECCOMP)");
  }
  else {
    perror("prctl(NO_NEW_PRIVS)");
  }
  error_flag = __errno_location();
  if (*error_flag == 0x16) {
    fwrite("SECCOMP_FILTER is not available. :(\n",1,0x24,stderr);
  }
  return 1;
}


void prog(void)

{
  undefined long_name [1008];

  get_name(long_name);
  printf("Hello Mr.%s\n",long_name);
  return;
}

void get_name(undefined8 *long_name)
{
  long num_long;
  ulong num_ul;
  undefined8 *exploree;
  undefined8 *placeholder;
  byte v_byte;

  v_byte = 0;
  puts("What is your name?");
  read(0,buffer,0x1000);
  *long_name = buffer._0_8_;
  long_name[0x1ff] = buffer._4088_8_;//at long_name[511]
  num_long = (long)long_name - (long)(undefined8 *)((ulong)(long_name + 1) & 0xfffffffffffffff8);
  exploree = (undefined8 *)(buffer + -num_long);
  placeholder = (undefined8 *)((ulong)(long_name + 1) & 0xfffffffffffffff8);
  for (num_ul = (ulong)((int)num_long + 0x1000U >> 3); num_ul != 0; num_ul = num_ul - 1) {
    *placeholder = *exploree;
    exploree = exploree + (ulong)v_byte * -2 + 1;
    placeholder = placeholder + (ulong)v_byte * -2 + 1;
  }
  return;
}
