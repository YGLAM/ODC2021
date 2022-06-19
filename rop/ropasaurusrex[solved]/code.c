
void entry(void)

{
  __libc_start_main(main);
  do {
                    /* WARNING: Do nothing block with infinite loop */
  } while( true );
}
void main(void)

{
  overflow();
  write(1,&constant,4);
  return;
}


void overflow(void)

{
  undefined string [136];

  read(0,string,0x100);
  return;
}
