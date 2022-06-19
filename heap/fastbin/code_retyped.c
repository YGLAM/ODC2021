typedef struct{
    char* msg;
    int size;
    int is_free;
}entry;

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
  while (((int)index < 100 && (entries[(int)index].msg != (char *)0x0))) {// it is looking for the first empty msg
    index = index + 1;
  }
  if (index == 100) {
    puts("No more entries!");
  }
  else {
    printf("Size: ");
    value_read = read_integer();//upon finding an empty msg it reads its size
    if ((0 < value_read) && (value_read < 0x1000)) {
      entries[(int)index].size = value_read;
      chunk_addr = (char *)malloc((long)value_read);
      entries[(int)index].msg = chunk_addr;
      *(undefined *)&entries[(int)index].is_free = 0;//sets the chunk as occupied
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
    if (*(char *)&entries[choice].is_free == '\x01') {
      puts("Can\'t write on a freed entry!");
    }
    else {
      if (entries[choice].msg == (char *)0x0) {//it is checking that the message is not free
        puts("Not allocated yet!");
      }
      else {
        printf("Content: ");
        read(0,entries[choice].msg,(ulong)(uint)entries[choice].size);
        entries[choice].msg[ entries[choice].size - 1 ] = '\0';//it's terminating the message
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
    puts("Index out of range!");//it does NOT do check on .is_free status, you could do DOUBLE FREES !
  }
  else {
    free(entries[(int)value_read].msg);
    *(undefined *)&entries[(int)value_read].is_free = 1;
    printf("Index %d freed!\n",(ulong)value_read);
  }
  return;
}
// there are 2 global variables inside the libc called free_hook and malloc_hook, you could overwrite these
// these vars are pointers used to monitor and profile memory allocation, you could use these to access the instruction
// pointer

// if you have a pointer to a function inside the free_hook then whenever you call a free() you will
// instead call the functioned pointed at by the free_hook

// for the malloc_hook it is the same thing instead it is don e to malloc() allocations

// we have a plan using the 2 vulnerabilities we have found:

// 1. in read_entry it is printing chunks that are free because it is not checking whether the chunk has been freed or not
// 2. in free_entry I could do double frees

// we want to leak libc and then find a way to overwrite free_hook and malloc_hook, that'll give us code execution
