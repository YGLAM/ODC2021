void main(void)

{
  long i;

  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);
  setvbuf(stderr,(char *)0x0,2,0);//clears the buffers
  while( true ) {
    while( true ) {
      menu();
      printf("> ");
      i = get_int();
      if (i != 0) break;
      add_numbers();
    }
    if (i != 1) break;
    print_numbers();
  }
                    /* WARNING: Subroutine does not return */
  exit(0);
}


void menu(void)

{
  puts("");
  puts("**************");
  puts("0. Add Numbers");
  puts("1. Print Numbers");
  puts("2. Exit");
  return;
}

void get_int(void)

{
  long offset;
  char number [200];
  long canary;

  canary = *(long *)(offset + 0x28);
  read(0,number,200);//no overflow as of yet
  atoll(number);//converts a c-type string to a long long integer
  if (canary != *(long *)(offset + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}


void add_numbers(void)

{
  undefined *ptr_8;
  ulong offset_numeric;
  long canary_offset;
  undefined8 constant_k;
  undefined arr_8 [8];
  undefined arr_4 [4];
  uint index_2;
  int index_4;
  int index;
  long number;
  undefined *ptr_4;
  long canary;
  long offset_16;

  ptr_8 = arr_8;
  canary = *(long *)(canary_offset + 0x28);
  constant_k = 0x101219;//not ASCII or integer, in ghidra 0x101219 LEA        RDI,[DAT_0010201c]
  printf("How many would you add?");
  constant_k = 0x10122a;// MOV EAX , 0x0
  printf("> ");
  constant_k = 0x101234;// MOV dword ptr [RBP + index],EAX
  index = get_int();//2

  if ((index < 1) && (200 < index)) {

    constant_k = 0x101252; //JMP        stack_chk_fail
    puts("No one?\n OK!");

  }else {
    offset_numeric = (long)index * 4 + 0x17;//=1F ; 31 (dec)
    offset_16 = (offset_numeric / 0x10) * -0x10;//0x10 = 16

    ptr_8 = arr_8 + offset_16;//arr_8 is uninit? + 0x10 content = 0x7fffffffe990
    ptr_4 = arr_4 + offset_16;//same 0x10 content = 0x7fffffffe99f ; //-0x10 ?

    *(undefined8 *)(arr_8 + offset_16 + -8) = 0x1012a8;// MOV EAX, 0x0

    printf("#> ",0x10,offset_numeric % 0x10);//What is this ? Is it a leak ?
    //printf( %flags,width,precision) precision should be 0 ???

    *(undefined8 *)(arr_8 + offset_16 + -8) = 0x1012b2; // MOV qword ptr [RBP + number], RAX

    number = get_int();
    index_2 = 0;

    while (((int)index_2 < index && (-1 < number))) {
      //ptr_4[index_2] = number
      *(long *)(ptr_4 + (long)(int)index_2 * 8) = number;
      offset_numeric = (ulong)index_2;
      //arr_8[offset_16] = ...
      *(undefined8 *)(arr_8 + offset_16 + -8) = 0x1012f0;// MOV EAX, 0x0
      printf("[%d]#> ",offset_numeric);//this is (ulong)index_2
      //arr_8[offset_16] = ...
      *(undefined8 *)(arr_8 + offset_16 + -8) = 0x1012fa;// MOV qword ptr [RBP + number], RAX
      number = get_int();
      index_2 = index_2 + 1;

    }
    // if index_2 = 2 index_4 = [0 1 2]
    for (index_4 = 0; index_4 <= (int)index_2; index_4 = index_4 + 1) {
      *(long *)(numbers + (long)index_4 * 8) =
           *(long *)(numbers + (long)index_4 * 8) + *(long *)(ptr_4 + (long)index_4 * 8);

      //numbers[index_4] = numbers[index_4] + ptr_4[index_4]
      //pls take care of what you are now actually adding each time
    }
  }
  if (canary != *(long *)(canary_offset + 0x28)) {
                    /* WARNING: Subroutine does not return */
    *(undefined8 *)(ptr_8 + -8) = 0x101385;
    __stack_chk_fail();
  }
  return;
}


void print_numbers(void)

{
  int index;

  for (index = 0; index < 200; index = index + 1) {
    printf("%lld\n",*(undefined8 *)(numbers + (long)index * 8));
  }
  return;
}
