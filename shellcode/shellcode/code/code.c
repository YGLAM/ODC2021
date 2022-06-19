//YOU MUST JUMP to .data section of memory
//somehow the stack is a bit different from local to remote, what gives?
undefined8 main(void)

{
  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);//cleaning buffer
  puts(
      "  _________.__           .__  .__                   .___      \n /   _____/|  |__   ____ |  | |  |   ____  ____   __| _/____  \n \\_____  \\ |  |  \\_/ __ \\|  | |  | _/ ___\\/  _ \\ / __ |/ __ \\ \n /        \\|   Y  \\  ___/|  |_|  |_\\  \\__(  <_> ) /_/ \\  ___/ \n/_______  /|___|  /\\___  >____/____/\\___  >____/\\____ |\\___  >\n        \\/      \\/     \\/               \\/           \\/    \\/ \n\n\n"
      );
  prog();
  return 0;
}

void prog(void)

{
  undefined string [1008];

  get_name(string);
  printf("Hello Mr.%s\n",string);
  return;
}

void get_name(undefined8 *string){
  //please remember that string[1008]
  long long1;//long 8 bytes -9223372036854775808 to 9223372036854775807
  ulong unsig_l;//unsigned long 8 bytes 0 to 18446744073709551615
  undefined8 *buff_pointer;
  undefined8 *mask;
  byte bool;//single byte could go from 0 to 255

  bool = 0;// bool = false
  puts("What is your name?");
  //0x1000 = 4096 while buffer is 4088 you just have your jump
  read(0,buffer,0x1000);//reading from stdin into buffer, which is a global variable @ 0x601080
  //there is PLENTY of space to write our call to a execve, why should we jump to .data ?
  //please note that buffer stays within .bss and not .data
  *string = buffer._0_8_;//string points to address contained in the first 8 bytes of buffer
  string[0x1ff/*511*/] = buffer._4088_8_;//assigns the last 8 bytes of the buffer to half way to string

  // the address is 0b1111111111111111111111111111111111111111111111111111111111111000
  // so I'm setting the last 3 bits of
  // the casted to unsigned long  string + 1, meaning I'm removing at most 7 to the string pointer,
  // is it pointless ?
  long1 = (long)string - (long)(undefined8 *)((ulong)(string + 1) & 0xfffffffffffffff8);//what is this mask in an AND ?

  buff_pointer = (undefined8 *)(buffer + -long1);//I'm pointing to buffer minus something

  // I'm again setting to zero the last three bits found in the casted string + 1
  mask = (undefined8 *)((ulong)(string + 1) & 0xfffffffffffffff8);

  //un ciclo for che va da "lunghezza del buffer +1" a 0 escluso
  for (unsig_l = (ulong)((int)long1 + 0x1000U >> 3); unsig_l != 0; unsig_l--) {
    *mask = *buff_pointer; // I assign the mask
    buff_pointer = buff_pointer + (ulong)bool * -2 + 1;
    mask = mask + (ulong)bool * -2 + 1;
  }
  return;
}
