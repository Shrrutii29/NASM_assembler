section .data
	a1 dd 10
	a2 dw 20
	a3 dd 10,20
	
section .bss
	a resd 1
	b resb 8
	j resd 10
	hs resd 6

section .text
	global main
	
main: mul eax
	 add ebx, 12
	 inc eax
	 dec ebx
		
	efg: mul ebx
	cmp eax, 14
	cmp ebx, ecx
	cmp ebx, [ecx]
	cmp [ecx], edx
	jmp sf
	cmp [ecx], eax
	inc eax
	dec ebx
	sub eax, 15
	sub eax, [ebx]
	jmp efg
	abc: inc eax
	sf: sub eax, 123
	eq: inc ebx
