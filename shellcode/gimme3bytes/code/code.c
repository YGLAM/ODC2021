
undefined8 main(void)

{
  code *funcall;

  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);
  printf(
        "  ________.__                         ________   ___.            __                 \n /  _____/|__| _____   _____   ____   \\_____  \\  \\_ |__ ___.__._/  |_  ____   ______\n/   \\  ___|  |/     \\ /     \\_/ __ \\    _(__  <   | __ <   |  |\\   __\\/ __ \\ /  ___/\n\\    \\_\\  \\  |  Y Y  \\  Y Y  \\  ___/   /       \\  | \\_\\ \\___  | |  | \\  ___/ \\___ \\ \n \\______  /__|__|_|  /__|_|  /\\___  > /______  /  |___  / ____| |__|  \\___  >____  >\n        \\/         \\/      \\/     \\/         \\/       \\/\\/                \\/     \\/ \n>"
        );
  // 4096 allocated bytes
  funcall = (code *)mmap((void *)0x0,0x1000,7,0x22,-1,0);
  read(0,funcall,3);//This is eerily similiar to back_to_shell, but yo, here I'm writing only 3 bytes..
                    // WTF should I do with only 3 bytes? 
  (*funcall)();
  return 0;
}
