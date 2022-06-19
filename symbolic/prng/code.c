
void _start(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  undefined array [8];
  undefined8 stack_0;

  __libc_start_main(main,stack_0,&stack0x00000008,__libc_csu_init,__libc_csu_fini,param_3,array);
  do {
                    /* WARNING: Do nothing block with infinite loop */
  } while( true );
}

undefined8 main(void)

{
  undefined8 rnd_long;
  ulong ulong_input;
  long in_FS_OFFSET;
  uint random_bytes;
  int i;
  int fd_random;//there are two files on linux : u_random (not blocking ,nopn guaranteed entropy)
                // and random ( guaranteed random )
  uint uint_input;
  undefined array [5008];
  char input [104];
  long canary;

  canary = *(long *)(in_FS_OFFSET + 0x28);
  fd_random = open("/dev/random",0);
  read(fd_random,&random_bytes,4);
  close(fd_random);
  seedRand(array,(long)(int)random_bytes);
  for (i = 0; i < 1000; i = i + 1) {
    genRandLong(array);
  }
  rnd_long = genRandLong(array);//after we have printed out 1000 random longs we output the 1001st
// if you were able to fix the seed you would always the same "random" numbers
  printf("%#lx, ",rnd_long);
  puts("guess the seed:");
  read(0,input,99);
  ulong_input = strtoul(input,(char **)0x0,0);//to unsigned long
  uint_input = (uint)ulong_input;
  if (uint_input == random_bytes) {
    memset(input,0,100);//if they are equal it opens the flag
    fd_random = open("./flag",0);
    read(fd_random,input,99);
    puts(input);
    close(fd_random);
  }
  else {
    printf("your guess was %#x, seed was %#x. Bye!",ulong_input & 0xffffffff,(ulong)random_bytes);
  }
  if (canary != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}

ulong genRandLong(undefined8 *i_state)
//i_state is the internal state of pnrg
{
  int jj;
  int int_addr;
  ulong u_long;

  if ((0x26f < *(int *)(i_state + 0x270)) || (*(int *)(i_state + 0x270) < 0)) {
    if ((0x270 < *(int *)(i_state + 0x270)) || (*(int *)(i_state + 0x270) < 0)) {
      m_seedRand(i_state,0x1105);
    }
    for (jj = 0; jj < 0xe3; jj = jj + 1) {
      i_state[jj] = i_state[jj + 0x18d] ^
                    (ulong)(((uint)i_state[jj + 1] & 0x7fffffff | (uint)i_state[jj] & 0x80000000) >>
                           1) ^ *(ulong *)(mag.3808 + (ulong)((uint)i_state[jj + 1] & 1) * 8);//mag.3808 is a global variable
    }
    // the first 8 bytes of mag are all 0's then there's 0xDF 0xB0 0x08 0x99 then
    for (; jj < 0x26f; jj = jj + 1) {
      i_state[jj] = i_state[jj + -0xe3] ^
                    (ulong)(((uint)i_state[jj + 1] & 0x7fffffff | (uint)i_state[jj] & 0x80000000) >>
                           1) ^ *(ulong *)(mag.3808 + (ulong)((uint)i_state[jj + 1] & 1) * 8);
    }
    i_state[0x26f] =
         i_state[0x18c] ^
         (ulong)(((uint)*i_state & 0x7fffffff | (uint)i_state[0x26f] & 0x80000000) >> 1) ^
         *(ulong *)(mag.3808 + (ulong)((uint)*i_state & 1) * 8);
    *(undefined4 *)(i_state + 0x270) = 0;
  }
  int_addr = *(int *)(i_state + 0x270);
  *(int *)(i_state + 0x270) = int_addr + 1;
  u_long = i_state[int_addr] ^ (ulong)i_state[int_addr] >> 0xb;
  u_long = u_long ^ (uint)(u_long << 7) & 0x9d2c5680;
  u_long = u_long ^ (uint)(u_long << 0xf) & 0xefc60000;
  return u_long ^ u_long >> 0x12;
}

undefined8 * seedRand(undefined8 *state,undefined8 seed)

{
  long ii;
  undefined8 *ptr_one;
  undefined8 *ptr_two;
  long in_FS_OFFSET;
  byte j;
  undefined8 smol_array [625];
  long canary;

  j = 0;
  canary = *(long *)(in_FS_OFFSET + 0x28);
  m_seedRand(smol_array,seed);
  ptr_one = smol_array; // I'm copying smol_array into state, so it was a lie, state doesn't actually contain the state, but it will
  ptr_two = state;
  for (ii = 0x271; ii != 0; ii = ii + -1) {
    *ptr_two = *ptr_one;
    ptr_one = ptr_one + (ulong)j * -2 + 1;// these are both just ptr_one++ and ptr_two++
    ptr_two = ptr_two + (ulong)j * -2 + 1;// I'm copying..
  }
  if (canary != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return state;
}
//This is the true generator

void m_seedRand(ulong *state,ulong seed)

{
  *state = seed & 0xffffffff; //masking ??
  *(undefined4 *)(state + 0x270) = 1;  // we are reusing state+0x270 several times
  while (*(int *)(state + 0x270) < 0x270) { // sounds like a counter
    state[*(int *)(state + 0x270)] =
         (ulong)(uint)((int)state[*(int *)(state + 0x270) + -1] * 0x17b5);
    *(int *)(state + 0x270) = *(int *)(state + 0x270) + 1;
  }
  return;
}
//Bruteforcing 4bytes is quite easy locally. it takes almost 40 minutes tho
