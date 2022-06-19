
undefined8 main(void)

{
  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);
  puts(
      "                                                         ,--,    ,--,    \n                                                       ,--.\'|  ,--.\'|    \n                                                       |  | :  |  | :    \n  .--.--.              .--.--.                         :  : \'  :  : \'    \n /  /    \'       .--, /  /    \'     ,---.     ,--.--.  |  \' |  |  \' |    \n|  :  /`./     /_ ./||  :  /`./    /     \\   /       \\ \'  | |  \'  | |    \n|  :  ;_    , \' , \' :|  :  ;_     /    / \'  .--.  .-. ||  | :  |  | :    \n \\  \\    `./___/ \\: | \\  \\    `. .    \' /    \\__\\/: . .\'  : |__\'  : |__  \n  `----.   \\.  \\  \' |  `----.   \\\'   ; :__   ,\" .--.; ||  | \'.\'|  | \'.\'| \n /  /`--\'  / \\  ;   : /  /`--\'  /\'   | \'.\'| /  /  ,.  |;  :    ;  :    ; \n\'--\'.     /   \\  \\  ;\'--\'.     / |   :    :;  :   .\'   \\  ,   /|  ,   /  \n  `--\'---\'     :  \\  \\ `--\'---\'   \\   \\  / |  ,     .-./---`-\'  ---`-\'   \n                \\  \' ;             `----\'   `--`---\'                     \n                 `--`                                                    "
      );
  prog();
  return 0;
}
void prog(void)

{
  undefined string [208];

  get_name(string);
  printf("Hello Mr.%s\n",string);
  return;
}
void get_name(undefined8 *name)

{
  ulong un_long;
  long longn;
  undefined8 *puVar1;
  undefined8 *puVar2;
  byte bVar3;
  int threshold;

  bVar3 = 0;
  puts("What is your name?");
  read(0,buffer,1000);//reads from stdin into global var, surely overflowable
  threshold = 0;
  while( true ) {
    if (threshold > 999) {//if threshold is bigger than 999 meaning we have to overwrite it
      *name = buffer._0_8_;
      name[0x7c] = buffer._992_8_;//name[124]
      longn = (long)name - (long)(undefined8 *)((ulong)(name + 1) & 0xfffffffffffffff8);
      puVar1 = (undefined8 *)(buffer + -longn);
      puVar2 = (undefined8 *)((ulong)(name + 1) & 0xfffffffffffffff8);
      for (un_long = (ulong)((int)longn + 1000U >> 3); un_long != 0; un_long = un_long - 1) {
        *puVar2 = *puVar1;
        puVar1 = puVar1 + (ulong)bVar3 * -2 + 1;
        puVar2 = puVar2 + (ulong)bVar3 * -2 + 1;
      }
      return;//we have to return
    }
    //otherwise if we do not overwrite we go into this call which will break the system
    //the function is broken if the threshold position or its next contain the string "syscall"
    if ((buffer[threshold] == '\x0f') && (buffer[threshold + 1] == '\x05')) break;
    threshold = threshold + 1;
  }
  puts("Nonono!");
                    /* WARNING: Subroutine does not return */
  exit(-1);
}
