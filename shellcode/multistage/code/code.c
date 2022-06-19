
undefined8 main(void){
  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);//these guys are removing the buffer
  printf(
        "   _____ __    _____ ____                __ _____ _    __ ___\n  / ___// /_  |__  // / /_________  ____/ /|__  /| |  / /|__ \\\n  \\__ \\/ __ \\  /_ </ / // ___/ __ \\/ __  /  /_ < | | / / __/ /\n ___/ / / / /___/ / / // /__/ /_/ / /_/ / ___/ / | |/ / / __/ \n/____/_/ /_//____/_/_/ \\___/\\____/\\__,_/ /____/  |___/ /____/ \n                                                             \n  "
        );
  prog();
  printf("Executing you shellcode.");
  (*(code *)buffer)();//I'm executing THAT global buffer!
  return 0;
}

void prog(void){
  undefined string [32];//this is a local variable

  get_name(string);
  printf("Hello Mr.%s\n",string);
  return;
}

void get_name(undefined8 *string){
  undefined8 variable;

  puts("What is your name?");
  read(0,buffer,0x14);//Reading 20 bytes (0x14) from buffer,but where is it? The color in ghidra tells you it is GLOBAL!! IT IS NOT ON STACK
  variable = buffer._8_8_;//It is a "copy", the second 8 bytes from buffer into variable
                          //It is being used when there's a mismatch between type sizes in the decompiled code
                          //and Ghidra cannot show you that the whole variable is being modified.
  *string = buffer._0_8_;//The first 8 bytes from buffer into this other variable
  string[1] = variable;//copying back original parameter in (second 8 bytes?)
  *(undefined4 *)(string + 2) = buffer._16_4_;//copying 4 bytes starting from the third 8 bytes in the buffer @ 4 byte pointer starting from string+2
  //THIS SHOULD BE A LOOP-UNROLLED MEMCPY !!!
  //TLDR: copying 20 bytes from buffer into string !
  return;
}
//The challenge is writing twenty bytes of shellcode!
