/*
Chunk Size must be a multiple of 16

check-sec output here:
Arch:     amd64-64-little
RELRO:    Full RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      PIE enabled

file output here:
fastbin_attack: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV),
                dynamically linked,
                interpreter /lib64/ld-linux-x86-64.so.2,
                for GNU/Linux 3.2.0,
                BuildID[sha1]=0dc14507538c6b7a9caf0434eb45d87d215c98f6,
                not stripped

*/
undefined8 main(void)

{
  undefined4 case;
  bool boolean;

  setvbuf(stdout,(char *)0x0,2,0);
  setvbuf(stdin,(char *)0x0,2,0);
  boolean = false;
  while (!boolean) {
    print_menu();
    case = read_integer();
    switch(case) {
    default:
      puts("Invalid option!");
      break;
    case 1:
      alloc();
      break;
    case 2:
      write_entry();
      break;
    case 3:
      read_entry();
      break;
    case 4:
      free_entry();
      break;
    case 5:
      boolean = true;
    }
  }
  return 0;
}


void print_menu(void)

{
  puts("Options:");
  puts("1) Alloc entry");
  puts("2) Write entry");
  puts("3) Read entry");
  puts("4) Free entry");
  puts("5) Quit");
  printf("> ");
  return;
}


int read_integer(void)

{
  int value
  long canary_offset;
  char string [99];
  undefined unknown;
  long canary_addr;

  canary_addr = *(long *)(canary_offset + 0x28);
  read(0,string,100);
  unknown = 0;//used to end string
  value = atoi(string);
  if (canary_addr != *(long *)(canary_offset + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return value;
}


void alloc(void)
//please note, entries is a global variable used as undefined1[1600], seeing it used here tells us
//that in truth it indicates an address and so it should be retyped to
// undefined8[200]
{
  int value_read;
  void *chunk_addr;
  uint index;

  index = 0;
  while (((int)index < 100 && (*(long *)(entries + (long)(int)index * 2) != 0))) { //it is also looking for something in the memory
    index = index + 1; //we are accessing only the EVEN entries of the array
  }
  if (index == 100) {
    puts("No more entries!");
  }
  else {
    printf("Size: ");
    value_read = read_integer();
    if ((0 < value_read) && (value_read < 0x1000)) {  //0x1000 is the size of a page !
      *(int *)(entries + (long)(int)index * 2 + 1) = value_read; // it is setting the second "slot" (indicated by the +1)
      chunk_addr = malloc((long)value_read);
      entries[(long)(int)index * 2] = chunk_addr; //it is stored in the other slot
      *(undefined *)((long)entries + (long)(int)index * 0x10 + 0xc) = 0;
    }
    printf("Allocated at index %d!\n",(ulong)index);
  }
  return;
}


void write_entry(void)

{
  int choice;

  printf("Index: ");
  choice = read_integer();
  if ((choice < 0) || (99 < choice)) {
    puts("Index out of range!");
  }
  else {
    //Unlike read_entry here it does check whether the chunk is free or not
    if (*(char *)((long)entries + (long)choice * 0x10 + 0xc) == '\x01') {//Same access seen on alloc
      puts("Can\'t write on a freed entry!");
    }
    else {
      if (entries[(long)choice * 2] == 0) {
        puts("Not allocated yet!");
      }
      else {//if it is not zero it is going to read inside the entry
        printf("Content: ");
        read(0,(void *)entries[(long)choice * 2],(ulong)*(uint *)(entries + (long)choice * 2 + 1));
        *(undefined *)// ???
         ((ulong)(*(int *)(entries + (long)choice * 2 + 1) - 1) + entries[(long)choice * 2]) = 0;
        puts("Done!");
      }
    }
  }
  return;
}



void read_entry(void)

{
  int value_read;

  printf("Index: ");
  value_read = read_integer();
  if ((value_read < 0) || (99 < value_read)) {
    puts("Index out of range!");
  }
  else {
    if (entries[(long)value_read * 2] == 0) {//It does NOT check if the pointer is free or not !!
      puts("Not allocated yet!");
    }
    else {
      puts((char *)entries[(long)value_read * 2]); //it just prints the address
    }
  }
  return;
}




void free_entry(void)

{
  uint value_read;

  printf("Index: ");
  value_read = read_integer();
  if (((int)value_read < 0) || (99 < (int)value_read)) {
    puts("Index out of range!");
  }
  else {
    free(*(void **)(entries + (long)(int)value_read * 0x10));
    entries[(long)(int)value_read * 0x10 + 0xc] = 1;//It writes the valid bit ?
    printf("Index %d freed!\n",(ulong)value_read);
  }
  return;
}
//We'll need to create a new structure in ghidra

typedef struct{
  char* msg;
  long size;
}entry

//after we've done so the code appearance will change dramatically

undefined8 main(void)

{
  undefined4 case;
  bool boolean;

  setvbuf(stdout,(char *)0x0,2,0);
  setvbuf(stdin,(char *)0x0,2,0);
  boolean = false;
  while (!boolean) {
    print_menu();
    case = read_integer();
    switch(case) {
    default:
      puts("Invalid option!");
      break;
    case 1:
      alloc();
      break;
    case 2:
      write_entry();
      break;
    case 3:
      read_entry();
      break;
    case 4:
      free_entry();
      break;
    case 5:
      boolean = true;
    }
  }
  return 0;
}

void print_menu(void)

{
  puts("Options:");
  puts("1) Alloc entry");
  puts("2) Write entry");
  puts("3) Read entry");
  puts("4) Free entry");
  puts("5) Quit");
  printf("> ");
  return;
}


void read_integer(void)

{
  long canary_offset;
  char string [99];
  undefined unknown;
  long canary_addr;

  canary_addr = *(long *)(canary_offset + 0x28);
  read(0,string,100);
  unknown = 0;
  atoi(string);
  if (canary_addr != *(long *)(canary_offset + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}


void alloc(void)

{
  int value_read;
  char *chunk_addr;
  uint index;

  index = 0;
  while (((int)index < 100 && (entries[(int)index].msg != (char *)0x0))) {
    index = index + 1;
  }
  if (index == 100) {
    puts("No more entries!");
  }
  else {
    printf("Size: ");
    value_read = read_integer();
    if ((0 < value_read) && (value_read < 0x1000)) {
      *(int *)&entries[(int)index].size = value_read;
      chunk_addr = (char *)malloc((long)value_read);
      entries[(int)index].msg = chunk_addr;
      *(undefined *)((long)&entries[(int)index].size + 4) = 0;
    }
    printf("Allocated at index %d!\n",(ulong)index);
  }
  return;
}


void write_entry(void)

{
  int choice;

  printf("Index: ");
  choice = read_integer();
  if ((choice < 0) || (99 < choice)) {
    puts("Index out of range!");
  }
  else {
    if (*(char *)((long)&entries[choice].size + 4) == '\x01') {
      puts("Can\'t write on a freed entry!");
    }
    else {
      if (entries[choice].msg == (char *)0x0) {
        puts("Not allocated yet!");
      }
      else {
        printf("Content: ");
        read(0,entries[choice].msg,(ulong)*(uint *)&entries[choice].size);
        entries[choice].msg[*(int *)&entries[choice].size - 1] = '\0';
        puts("Done!");
      }
    }
  }
  return;
}

void read_entry(void)

{
  int value_read;

  printf("Index: ");
  value_read = read_integer();
  if ((value_read < 0) || (99 < value_read)) {
    puts("Index out of range!");
  }
  else {
    if (entries[value_read].msg == (char *)0x0) {
      puts("Not allocated yet!");
    }
    else {
      puts(entries[value_read].msg);
    }
  }
  return;
}

void free_entry(void)

{
  uint value_read;

  printf("Index: ");
  value_read = read_integer();
  if (((int)value_read < 0) || (99 < (int)value_read)) {
    puts("Index out of range!");
  }
  else {
    free(entries[(int)value_read].msg);
    *(undefined *)((long)&entries[(int)value_read].size + 4) = 1;//seeing the +4 let's you understand that there are other entries in the chunk, we'll edit the type
    printf("Index %d freed!\n",(ulong)value_read);
  }
  return;
}
