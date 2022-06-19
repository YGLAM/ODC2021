//WARNING : Intel 80386 32-bit architecture
undefined4 main(void){
  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);//clears input buffer
  printf(
        "   _____ __    _____ ____                __ _____ _    __ ___\n  / ___// /_  |__  // / /_________  ____/ /|__  /| |  / /|__ \\\n  \\__ \\/ __ \\  /_ </ / // ___/ __ \\/ __  /  /_ < | | / / __/ /\n ___/ / / / /___/ / / // /__/ /_/ / /_/ / ___/ / | |/ / / __/ \n/____/_/ /_//____/_/_/ \\___/\\____/\\__,_/ /____/  |___/ /____/ \n                                                             \n  "
        );
  prog();
  return 0;
}

void prog(void){
  undefined name[208];

  get_name(name);
  printf("Hello Mr.%s\n",name);
  return;
}
//disclaimer the 1000U means unsigned int
void get_name(undefined4 *string){
  int number;
  uint uVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  byte bool;
  int local_20;

  bool = 0;
  puts("What is your name?");
  read(0,buffer,1000);//reads 1000 of what ?
  local_20 = 0;
  while( true ) {
    if (999 < local_20) {//we have to overwrite local_20 with something bigger than 999 otherwise we'll never come out of it
      *string = buffer._0_4_;
      string[0xf9] = buffer._996_4_;
      number = (int)string - (int)(undefined4 *)((uint)(string + 1) & 0xfffffffc);
      puVar3 = (undefined4 *)(buffer + -number);
      puVar4 = (undefined4 *)((uint)(string + 1) & 0xfffffffc);
      for (uVar2 = number + 1000U >> 2; uVar2 != 0; uVar2 = uVar2 - 1) {
        *puVar4 = *puVar3;
        puVar3 = puVar3 + (uint)bool * -2 + 1;
        puVar4 = puVar4 + (uint)bool * -2 + 1;
      }
      return;
    }
    if (buffer[local_20] == '\0') break;
    local_20 = local_20 + 1;
  }
  puts("Nonono!");
                    /* WARNING: Subroutine does not return */
  exit(-1);
}
