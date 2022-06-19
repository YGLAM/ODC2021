#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/mman.h>

void get_shellcode(char *buffer){
  int i = 0;
  printf("Send shellcode plz?\n");
  read(0, buffer, 1000);
  for (i = 0; i < 1000; i++){
      if ((buffer[i] == 0xcd || buffer[i] == 0x80) || (buffer[i] == 0x0f || buffer[i] == 0x05)){
          printf("Nonono!\n");
          exit(-1);
      }
  }
}

void prog(){
  void (*addr)(void) = mmap(NULL, 0x1000, PROT_READ|PROT_EXEC|PROT_WRITE, MAP_ANON | MAP_SHARED, -1, 0);

  if (addr == MAP_FAILED){
      printf("mmap failed");
      exit(-1);
  }
  get_shellcode(addr);
  addr();
}

int main(){
  setvbuf(stdin, 0, 2, 0);
  setvbuf(stdout, 0, 2, 0);
  printf("   ▄████████ ▄██   ▄      ▄████████  ▄████████    ▄████████    ▄████████  ▄█          ▄████████ \n  ███    ███ ███   ██▄   ███    ███ ███    ███   ███    ███   ███    ███ ███         ███    ███ \n  ███
    █▀  ███▄▄▄███   ███    █▀  ███    █▀    ███    ███   ███    █▀  ███         ███    ███ \n  ███        ▀▀▀▀▀▀███   ███        ███          ███    ███   ███        ███        ▄███▄▄▄▄██▀ \n▀███████████ ▄██   █
██ ▀███████████ ███        ▀███████████ ▀███████████ ███       ▀▀███▀▀▀▀▀   \n         ███ ███   ███          ███ ███    █▄    ███    ███          ███ ███       ▀███████████ \n   ▄█    ███ ███   ███    ▄█    ███
 ███    ███   ███    ███    ▄█    ███ ███▌    ▄   ███    ███ \n ▄████████▀   ▀█████▀   ▄████████▀  ████████▀    ███    █▀   ▄████████▀  █████▄▄██   ███    ███ \n                                                                         ▀           ███    ███ \n");
  prog();
}
