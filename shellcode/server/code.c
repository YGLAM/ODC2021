//The htons() function converts the unsigned short integer hostshort from host byte order to network byte order.
/*  int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
        Upon creating a socket with socket(2), the socket exists in a name space (address family)
        but has no address assigned to it.
        Bind() assigns the address specified by addr to the socket referred to by the file descriptor sockfd.
        addrlen specifies the size, in bytes, of the address structure pointed to by addr.
        On success it returns 0
*/
/*  int accept(int sockfd, struct sockaddr *restrict addr,socklen_t *restrict addrlen);
      It extracts the first connection request on the queue of pending connections for the
      listening socket, sockfd, creates a new connected socket, and returns a new file descriptor
      referring to that socket.  The newly created socket is not in the listening state.
      The original socket sockfd is unaffected by this call.
        int sockfd : it is a socket created by socket(),then bound to a local addr with bind()
                     and is currently listening for connections after a listen()
        struct sockaddr *restrict addr : is a pointer to a sockaddr struct.This is filled with
                     the addr of the peer socket
        socklen_t *restrict addrlen : is a value-result arg, the caller must init it to contain
                     the size [Bytes] of the struct pointed by addr
*/
/*  pid_t fork(void):
      fork() creates a new process by duplicating the calling process.
      The new process is referred to as the child process.  The calling
      process is referred to as the parent process.

      The child process and the parent process run in separate memory
      spaces.  At the time of fork() both memory spaces have the same
      content.  Memory writes, file mappings (mmap(2)), and unmappings
      (munmap(2)) performed by one of the processes do not affect the
      other.

*/

void main(void)

{
  __pid_t _Var1;
  sockaddr addr;
  undefined sck_addr [4];
  uint32_t htonl_zero;
  socklen_t addrlen;
  int sock_fd;
  undefined4 0xten;
  int socket;

  socket = ::socket(2,1,0);
  sck_addr._0_2_ = 2;
  htonl_zero = htonl(0);
  sck_addr._2_2_ = htons(0x7d5);
  0xten = 0x10;
  bind(socket,(sockaddr *)sck_addr,0x10);
  listen(socket,5);
  signal(0x11,(__sighandler_t)0x1);
  while( true ) {
    puts("server waiting");
    addrlen = 0x10;
    sock_fd = accept(socket,&addr,&addrlen);
    _Var1 = fork();
    if (_Var1 == 0) break;
    close(sock_fd);
  }
  write(sock_fd,
        "  _________                                \n /   _____/ ______________  __ ___________ \n \\_____  \\_/ __ \\_  __ \\  \\/ // __ \\_  __ \\\n /        \\  ___/|  | \\/\\   /\\  ___/|  | \\/\n/_______  /\\___  >__|    \\_/  \\___  >__|   \n        \\/     \\/                 \\/       \n\n\n"
        ,0x10a);
  prog();
  close(sock_fd);
                    /* WARNING: Subroutine does not return */
  exit(0);
}


void prog(int param_1)

{
  size_t length;
  char string [1008];

  get_name(param_1,string);
  write(param_1,"Hello Mr.",9);
  length = strlen(string);
  write(param_1,string,length);
  write(param_1,&DAT_00402027,1);
  return;
}


void get_name(int null,undefined8 *string)
{
  long mask;
  ulong index;
  undefined8 *bufferoff;
  undefined8 *masker;
  byte zeroptr;

  zeroptr = 0;
  printf("What is your name?\\n");
  read(null,buffer,0x1000);
  *string = buffer._0_8_;
  string[0x1ff] = buffer._4088_8_;
  mask = (long)string - (long)(undefined8 *)((ulong)(string + 1) & 0xfffffffffffffff8);
  bufferoff = (undefined8 *)(buffer + -mask);
  masker = (undefined8 *)((ulong)(string + 1) & 0xfffffffffffffff8);
  for (index = (ulong)((int)mask + 0x1000U >> 3); index != 0; index = index - 1) {
    *masker = *bufferoff;
    bufferoff = bufferoff + (ulong)zeroptr * -2 + 1;
    masker = masker + (ulong)zeroptr * -2 + 1;//remember this pattern as an unrolled memcpy
  }
  return;
}
