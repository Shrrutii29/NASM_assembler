# NASM_assembler
- nasm assembler supports 32 bit registers only.
- intel manual is used for opcodes.
- SIB is not supported.

---

## Supported Instructions
- mov
- add
- sub
- div
- mul
- xor
- jmp
- jz
- jnz
- cmp
- inc
- dec

---

## opcode table format
sr no. | opcode | instruction | no_of_args | arg1 | arg2 | size | mod_rm | rd | imm_size

---

## Symbol table format 
sr no. | name | address | size | section | value

---

## intermediate file format
address | opcode_srNo | symbol_srNo | hex_value | arg1 | arg2

---

## run program
 python3 assembler.py

---
## input
assembly code is given as input in demo.asm file

---

## output 
output.lst file is generated in following format
### data section
  address value( in little endian format)

### bss section
  address value( as per need)

### text section
  address opcode|mod_rm(optional)|value(optional)

---
