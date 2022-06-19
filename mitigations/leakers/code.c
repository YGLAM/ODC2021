undefined8 main(void)
//stack recreation
/* Hi(?) -->   sEBP
            sEIP
            length
            canary_offset
            string[100-103]
            string[..-..]
            string[0-3]
  Lo(?)  -->   canary
  check g_buffer size

PRO TIP : Check ghidra it'll tell you the order on the stack , there you can perform static analysis
          to see where it is on the stack, to perform dynamic analysis use
*/
{
  ssize_t length;
  long canary_offset;
  char string [104];//this can overflow
  long canary;

  canary = *(long *)(canary_offset + 0x28);//setting the canary

  setvbuf(stdin,(char *)0x0,2,0);//clearing of the buffer
  setvbuf(stdout,(char *)0x0,2,0);

  puts("Welcome to Leakers!\n");

  length = read(0,g_buffer,100);//read returns the amount of bytes read
  if (1 < (int)length) {
    g_buffer[(int)length + -1] = 0;//we put a 0 to the last string changing the /n into a /0 'terminator'
  }

  while( true ) {//done on the stack right before canary
    length = read(0,string,200);//this clearly overflows
    if (((int)length == 1) && ((string[0] == '\n' || (string[0] == '\0')))) break;//break if we've read only one byte
    printf("%s> %s",g_buffer,string);//otherwise print everything out
  }
  puts("Bye!");
  if (canary != *(long *)(canary_offset + 0x28)) {
    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
