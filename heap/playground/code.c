//p &__malloc_hook

int main(int argc,char **argv){
  uint pid;
  int out_sscanf;
  int out_strcmp;
  void *ptr_1;
  int i;
  int num;
  intptr_t long_int_1;
  intptr_t long_int_2;
  void *src_write;
  long *src;
  void *result;
  char buffer [1000];
  char cmd [1000];

  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);//buff flush

  pid = getpid();
  fprintf(stdout,"pid: %d\n",(ulong)pid);
  fprintf(stdout,"main: %p\n",main);//here it prints out addrs

  ptr_1 = malloc(1);//this is important
  min_heap = (ulong)ptr_1 & 0xfffffffffffff000;
  max_heap = min_heap + 0x1000;
  do {
    while( true ) {
      while( true ) {
        while( true ) {
          fwrite(&addr_10201b,1,2,stdout);
          fgets(buffer,1000,stdin);
          out_sscanf = __isoc99_sscanf(buffer,"%s %li %li",cmd,&long_int_1,&long_int_2);
          out_strcmp = strcmp(cmd,"malloc");
          if (out_strcmp != 0) break;
          result = malloc(long_int_1);
          fprintf(stdout,"==> %p\n",result);
        }
        out_strcmp = strcmp(cmd,"free");
        if (out_strcmp != 0) break;
        free((void *)long_int_1);
        fwrite("==> ok\n",1,7,stdout);
      }
      out_strcmp = strcmp(cmd,"show");//funfact : that 0x20fd1 should be the top chunk !
      if (out_strcmp != 0) break;
      if (out_sscanf == 2) {
        long_int_2 = 1;
      }
      src = (long *)long_int_1;
      for (i = 0; i < long_int_2; i = i + 1) {
        fprintf(stdout,"%p: %#16.0lx\n",src + i,src[i]);
      }
    }
    out_strcmp = strcmp(cmd,"write");
    if (out_strcmp == 0) {
      if (out_sscanf == 2) {
        long_int_2 = 1;
      }
      src_write = (void *)long_int_1;
      if (((ulong)long_int_1 < min_heap) || (max_heap <= (ulong)long_int_1)) {
        fwrite("==> fail\n",1,9,stdout);
      }
      else {
        fwrite("==> read\n",1,9,stdout);
        read(0,src_write,long_int_2);
        fwrite("==> done\n",1,9,stdout);
      }
    }
    else {
      puts("Commands: malloc n, free p, show p [n], write p [n]");
    }
  } while( true );
}
