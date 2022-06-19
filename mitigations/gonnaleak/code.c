
undefined8 main(void)

{
  ssize_t size;
  long in_FS_OFFSET;
  char string [104];
  long canary;

  canary = *(long *)(in_FS_OFFSET + 0x28); // is the canary static or does it change ? YESS IT CHANGES !!!
  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);
  puts("Leakers gonna leak!\n");
  while( true ) {//This is the key part, It continues to read stuff into string
    size = read(0,string,200);//I could push this out but
    if (((int)size == 1) && ((string[0] == '\n' || (string[0] == '\0')))) break;
    printf("> %s",string);//and it stops if the string has a newline or it is empty
  }
  puts("Bye!");
  if (canary != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
