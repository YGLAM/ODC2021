// index is @ 0x600378 is it a global var ?
undefined8 main(void)

{
  ssize_t signed;
  int i;
  int j;
  int array [12];

  len = 0xc3585a5e5f;
  write(1,"Try easyROP!\n",0xd);//Writes to stdout a simple string
                                //is it oversized?
//RBP-0x34 contains the effective address of j. that is put into the RAX
  while (2 < len) {
    len = 0;
    //0x7fffffffea84: 0x61616161 this is the address of j and of its content
    signed = read(0,&j,4);   //puts @ address of j 4bytes RAX = 0x7fffffffea84 //this returns the number of bytes read as signed
      /*  RAX  0x4 ===> this is the content of "signed"
          RCX  0x40016a (read+38) ◂— mov    dword ptr [rbp - 4], eax @ssize_t read
          RSI  0x7fffffffea84 ◂— 0x61616161 // 'aaaa'
          R11  0x202
          RSP  0x7fffffffea78 ◂— 0x0
          ### STACK CONTENTS ###
          │00:0000│ rsp   0x7fffffffea78 ◂— 0x0
          │01:0008│ rsi-4 0x7fffffffea80 ◂— 0x6161616100000000

          This next instruction is crucial (?) what is this thing pointing at ?
          0x40020e <main+86>     mov    rax, qword ptr [rip + 0x20015b] <0x600370>

          x/10wx 0x40020e+0x20015b
          0x600369:       0x00000000      0x00000000      0x00000000      0x00000000
          0x600379 <index+1>:     0x00000000      0x00000000      0x00000000      0x00000000
          0x600389:       0x00000000      0x00000000

      */
    len = len + (int)signed; //adds up written length
    /*  MOVSXD RDX, EAX <signed>
        MOV rax ,qword ptr[len] (its the rip + 20015b ) (what is this ?)
        ADD rax <signed>, rdx < len?>
        MOV qword ptr[rip<0x400218> + 0x200151<len>], rax <signed>

        SURPRISE SURPRISE, rip + 0x200151 is still 0x600369 which is empty, after that last mov it will be
        0x600369:       0x00000000      0x04000000      0x00000000      0x00000000

    */
    signed = read(0,&i,4);   //puts @ addres of i 4bytes
    len = len + (int)signed; //adds up written length
    array[index] = i + j;    //sums up these lengths
    //0x7fffffffea88: 0xc3c3c3c3      0x00000000      0x00000000      0x000

    index = index + 1;
    write(1,&len,4); //It picks them from 0x600370    //I write to stdout the first four bytes found at address of len
  }
  return 0;
}
