; constants
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0
segment .data
segment .bss ; variables
x_1 RESD 1
y_1 RESD 1
res RESB 1
section .text
global _start
print :  ; print
POP EBX
POP EAX
PUSH EBX
XOR ESI, ESI
print_dec :
MOV EDX, 0
MOV EBX, 0x000A
DIV EBX
ADD EDX, '0'
PUSH EDX
INC ESI
CMP EAX, 0
JZ print_next
JMP print_dec
print_next :
CMP ESI, 0
JZ print_exit
DEC ESI
MOV EAX, SYS_WRITE
MOV EBX, STDOUT
POP ECX
MOV [res], ECX
MOV ECX, res
MOV EDX, 1
INT 0x80
JMP print_next
print_exit :
RET
; subrotinas if/while
binop_je :
JE binop_true
JMP binop_false
binop_jg :
JG binop_true
JMP binop_false
binop_jl :
JL binop_true
JMP binop_false
binop_false :
MOV EBX, False
JMP binop_exit
binop_true :
MOV EBX, True
binop_exit : RET
_start :
MOV EBX, 5
MOV [x_1], EBX
MOV EBX, 0
MOV [y_1], EBX
LOOP_18
MOV EBX, [x_1]
PUSH EBX
MOV EBX, [y_1]
POP EAX
CMP EAX, EBX
CALL binop_jg
CMP EBX, False
JE EXIT_18
MOV EBX, [x_1]
PUSH EBX
MOV EBX, [y_1]
POP EAX
ADD EAX, EBX
MOV EBX, EAX
PUSH EBX
CALL print
JMP LOOP_18
EXIT_18
; end interrupt
MOV EAX, 1
INT 0x80
