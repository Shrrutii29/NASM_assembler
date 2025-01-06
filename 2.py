import re
import os

opcode_table = [
 {'sr_no' : 1,'opcode': '01', 'instruction': 'add', 'args': 2, 'arg1': 'reg32', 'arg2': 'reg32', 'size': 2, 'mod_rm': 1, '+rd': 0, 'imm_size': None},
 {'sr_no' : 2,'opcode': '83/0', 'instruction': 'add', 'args': 2, 'arg1': 'reg32', 'arg2': 'imm8', 'size': 3, 'mod_rm': 1, '+rd': 0, 'imm_size': 1},
 {'sr_no' : 3,'opcode': '81/0', 'instruction': 'add', 'args': 2, 'arg1': 'reg32', 'arg2': 'imm32', 'size': 6, 'mod_rm': 1, '+rd': 0, 'imm_size': 4},
 {'sr_no' : 4,'opcode': '03', 'instruction': 'add', 'args': 2, 'arg1': 'reg32', 'arg2': 'mem', 'size': 6, 'mod_rm': 1, '+rd': 0, 'imm_size': None},
 {'sr_no' : 5,'opcode': '83/0', 'instruction': 'add', 'args': 2, 'arg1': 'mem', 'arg2': 'imm8', 'size': 7, 'mod_rm': 1, '+rd': 0, 'imm_size': 1},
 {'sr_no' : 6,'opcode': '81/0', 'instruction': 'add', 'args': 2, 'arg1': 'mem', 'arg2': 'imm32', 'size': 10, 'mod_rm': 1, '+rd': 0, 'imm_size': 4},
 {'sr_no' : 7,'opcode': '01', 'instruction': 'add', 'args': 2, 'arg1': 'mem', 'arg2': 'reg32', 'size': 6, 'S': 1, '+rd': 0, 'imm_size': None},
 {'sr_no' : 8,'opcode': '05', 'instruction': 'add', 'args': 2, 'arg1': 'eax', 'arg2': 'imm32', 'size': 5, 'mod_rm': 0, '+rd': 0, 'imm_size': 4},
 {'sr_no' : 9,'opcode': '29', 'instruction': 'sub', 'args': 2, 'arg1': 'reg32', 'arg2': 'reg32', 'size': 2, 'mod_rm': 1, '+rd': 0, 'imm_size': None},
 {'sr_no' : 10,'opcode': '83/5', 'instruction': 'sub', 'args': 2, 'arg1': 'reg32', 'arg2': 'imm8', 'size': 3, 'mod_rm': 1, '+rd': 0, 'imm_size': 1},
 {'sr_no' : 11,'opcode': '81/5', 'instruction': 'sub', 'args': 2, 'arg1': 'reg32', 'arg2': 'imm32', 'size': 6, 'mod_rm': 1, '+rd': 0, 'imm_size': 4},
 {'sr_no' : 12,'opcode': '2B', 'instruction': 'sub', 'args': 2, 'arg1': 'reg32', 'arg2': 'mem', 'size': 2, 'mod_rm': 1, '+rd': 0, 'imm_size': None},
 {'sr_no' : 13,'opcode': '83/5', 'instruction': 'sub', 'args': 2, 'arg1': 'mem', 'arg2': 'imm8', 'size': 7, 'mod_rm': 1, '+rd': 0, 'imm_size': 1},
 {'sr_no' : 14,'opcode': '81', 'instruction': 'sub', 'args': 2, 'arg1': 'mem', 'arg2': 'imm32', 'size': 10, 'mod_rm': 0, '+rd': 0, 'imm_size': 4},
 {'sr_no' : 15,'opcode': '2B', 'instruction': 'sub', 'args': 2, 'arg1': 'mem', 'arg2': 'reg32', 'size': 6, 'mod_rm': 1, '+rd': 0, 'imm_size': None},
 {'sr_no' : 16,'opcode': '29', 'instruction': 'sub', 'args': 2, 'arg1': 'eax', 'arg2': 'imm32', 'size': 5, 'mod_rm': 1, '+rd': 0, 'imm_size': 4},
 {'sr_no' : 17,'opcode': '39', 'instruction': 'cmp', 'args': 2, 'arg1': 'reg32', 'arg2': 'reg32', 'size': 2, 'mod_rm': 1, '+rd': 0, 'imm_size': None},
 {'sr_no' : 18,'opcode': '83/7', 'instruction': 'cmp', 'args': 2, 'arg1': 'reg32', 'arg2': 'imm8', 'size': 3, 'mod_rm': 1, '+rd': 0, 'imm_size': 1},
 {'sr_no' : 19,'opcode': '81/7', 'instruction': 'cmp', 'args': 2, 'arg1': 'reg32', 'arg2': 'imm32', 'size': 6, 'mod_rm': 1, '+rd': 0, 'imm_size': 4},
 {'sr_no' : 20,'opcode': '3B', 'instruction': 'cmp', 'args': 2, 'arg1': 'reg32', 'arg2': 'mem', 'size': 6, 'mod_rm': 1, '+rd': 0, 'imm_size': None},
 {'sr_no' : 21,'opcode': '83/7', 'instruction': 'cmp', 'args': 2, 'arg1': 'mem', 'arg2': 'imm8', 'size': 7, 'mod_rm': 1, '+rd': 0, 'imm_size': 1},
 {'sr_no' : 22,'opcode': '81/7', 'instruction': 'cmp', 'args': 2, 'arg1': 'mem', 'arg2': 'imm32', 'size': 10, 'mod_rm': 1, '+rd': 0, 'imm_size': 4},
 {'sr_no' : 23,'opcode': '39', 'instruction': 'cmp', 'args': 2, 'arg1': 'mem', 'arg2': 'reg32', 'size': 6, 'mod_rm': 1, '+rd': 0, 'imm_size': None},
 {'sr_no' : 24,'opcode': '3D', 'instruction': 'cmp', 'args': 2, 'arg1': 'eax', 'arg2': 'imm32', 'size': 5, 'mod_rm': 0, '+rd': 0, 'imm_size': 4},
 {'sr_no' : 25,'opcode': 'EB', 'instruction': 'jmp', 'args': 1, 'arg1': 'rel8', 'arg2': None, 'size': 2, 'mod_rm': 0, '+rd': 0, 'imm_size': None},
 {'sr_no' : 26,'opcode': 'FF/4', 'instruction': 'jmp', 'args': 1, 'arg1': 'reg32', 'arg2': None, 'size': 2, 'mod_rm': 1, '+rd': 0, 'imm_size': None},
 {'sr_no' : 27,'opcode': 'FF', 'instruction': 'jmp', 'args': 1, 'arg1': 'mem', 'arg2': None, 'size': 6, 'mod_rm': 1, '+rd': 0, 'imm_size': None},
 {'sr_no' : 28,'opcode': '89', 'instruction': 'mov', 'args': 2, 'arg1': 'reg32', 'arg2': 'reg32', 'size': 2, 'mod_rm': 1, '+rd': 0, 'imm_size': None},
 {'sr_no' : 29,'opcode': 'B8', 'instruction': 'mov', 'args': 2, 'arg1': 'reg32', 'arg2': 'imm', 'size': 5, 'mod_rm': 0, '+rd': 1, 'imm_size': None},
 {'sr_no' : 30,'opcode': '8B', 'instruction': 'mov', 'args': 2, 'arg1': 'reg32', 'arg2': 'mem', 'size': 6, 'mod_rm': 1, '+rd': 0, 'imm_size': None},
 {'sr_no' : 31,'opcode': 'C7/0', 'instruction': 'mov', 'args': 2, 'arg1': 'mem', 'arg2': 'imm', 'size': 10, 'mod_rm': 1, '+rd': 0, 'imm_size': None},
 {'sr_no' : 32,'opcode': '89', 'instruction': 'mov', 'args': 2, 'arg1': 'mem', 'arg2': 'reg32', 'size': 6, 'mod_rm': 1, '+rd': 0, 'imm_size': None},
 {'sr_no' : 33,'opcode': 'A3', 'instruction': 'mov', 'args': 2, 'arg1': 'mem', 'arg2': 'eax', 'size': 5, 'mod_rm': 0, '+rd': 0, 'imm_size': None},
 {'sr_no' : 34,'opcode': '40', 'instruction': 'inc', 'args': 1, 'arg1': 'reg32', 'arg2': None, 'size': 1, 'mod_rm': 0, '+rd': 1, 'imm_size': None},
 {'sr_no' : 35,'opcode': 'FF/0', 'instruction': 'inc', 'args': 1, 'arg1': 'mem', 'arg2': None, 'size': 6, 'mod_rm': 1, '+rd': 0, 'imm_size': None},
 {'sr_no' : 36,'opcode': '48', 'instruction': 'dec', 'args': 1, 'arg1': 'reg32', 'arg2': None, 'size': 1, 'mod_rm': 0, '+rd': 1, 'imm_size': None},
 {'sr_no' : 37,'opcode': 'FF/1', 'instruction': 'dec', 'args': 1, 'arg1': 'mem', 'arg2': None, 'size': 6, 'mod_rm': 1, '+rd': 0, 'imm_size': None},
 {'sr_no' : 38,'opcode': '31', 'instruction': 'xor', 'args': 2, 'arg1': 'reg32', 'arg2': 'reg32', 'size': 2, 'mod_rm': 1, '+rd': 0, 'imm_size': None},
 {'sr_no' : 39,'opcode': '83/6', 'instruction': 'xor', 'args': 2, 'arg1': 'reg32', 'arg2': 'imm8', 'size': 3, 'mod_rm': 1, '+rd': 0, 'imm_size': 1},
 {'sr_no' : 40,'opcode': '81/6', 'instruction': 'xor', 'args': 2, 'arg1': 'reg32', 'arg2': 'imm32', 'size': 6, 'mod_rm': 1, '+rd': 0, 'imm_size': 4},
 {'sr_no' : 41,'opcode': '33', 'instruction': 'xor', 'args': 2, 'arg1': 'reg32', 'arg2': 'mem', 'size': 6, 'mod_rm': 1, '+rd': 0, 'imm_size': None},
 {'sr_no' : 42,'opcode': '83/6', 'instruction': 'xor', 'args': 2, 'arg1': 'mem', 'arg2': 'imm8', 'size': 7, 'mod_rm': 1, '+rd': 0, 'imm_size': 1},
 {'sr_no' : 43,'opcode': '81/6', 'instruction': 'xor', 'args': 2, 'arg1': 'mem', 'arg2': 'imm32', 'size': 10, 'mod_rm': 1, '+rd': 0, 'imm_size': 4},
 {'sr_no' : 44,'opcode': '31', 'instruction': 'xor', 'args': 2, 'arg1': 'mem', 'arg2': 'reg32', 'size': 6, 'mod_rm': 1, '+rd': 0, 'imm_size': None},
 {'sr_no' : 45,'opcode': '35', 'instruction': 'xor', 'args': 2, 'arg1': 'eax', 'arg2': 'imm32', 'size': 5, 'mod_rm': 0, '+rd': 0, 'imm_size': 4},
 {'sr_no' : 46,'opcode': 'F7/4', 'instruction': 'mul', 'args': 1, 'arg1': 'reg32', 'arg2': None, 'size': 2, 'mod_rm': 1, '+rd': 0, 'imm_size': None},
 {'sr_no' : 47,'opcode': 'F7/4', 'instruction': 'mul', 'args': 1, 'arg1': 'mem', 'arg2': None, 'size': 6, 'mod_rm': 1, '+rd': 0, 'imm_size': None},
 {'sr_no' : 48,'opcode': 'F7/6', 'instruction': 'div', 'args': 1, 'arg1': 'reg32', 'arg2': None, 'size': 2, 'mod_rm': 1, '+rd': 0, 'imm_size': None},
 {'sr_no' : 49,'opcode': 'F7/6', 'instruction': 'div', 'args': 1, 'arg1': 'mem', 'arg2': None, 'size': 6, 'mod_rm': 1, '+rd': 0, 'imm_size': None},
 {'sr_no' : 50,'opcode': '74', 'instruction': 'jz', 'args': 1, 'arg1': 'rel8', 'arg2': None, 'size': 3, 'mod_rm': 0, '+rd': 0, 'imm_size': None},
 {'sr_no' : 51,'opcode': '75', 'instruction': 'jnz', 'args': 1, 'arg1': 'rel8', 'arg2': None, 'size': 2, 'mod_rm': 0, '+rd': 0, 'imm_size': None}]


class SymbolTable:
    def __init__(self):
        self.table = []
        self.sr_no = 0

    def add_symbol(self, name, address=None, size=None, value=None, section=None):
        self.table.append({
            "sr_no": self.sr_no,
            "name": name,
            "address": format(address, '08X') if address is not None else None,
            "size": hex(size) if size is not None else None,
            "value": value,
            "section": section
        })
        # self.sr_no += 1

    def display(self):
        print("\nSymbol Table")
        print("\nSr No.\tName\tAddress\t\tSize\tSection\tValue")

        for entry in self.table:
            print(f"{entry['sr_no']}\t{entry['name']}\t{entry['address']}\t{entry['size']}\t{entry['section']}\t{entry['value']}")


# Pass 1
''' -------------------------------------------------------------------------------------------------------------------------------------- '''

def generate_symbolTable(filename):
    symbol_table = SymbolTable()
    curr_address = 0x0
    curr_section = None

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith(";"):
                with open("intermediate_file.txt", "a") as intermediate_filee:
                     intermediate_filee.write("\n")
                continue

            # Handle section declaration
            if line.startswith("section"):
                parts = line.split()
                if len(parts) != 2:
                    print(f"Error: Invalid section declaration: {line}")
                    continue
                curr_section = parts[1]
                curr_address = 0x0
                continue

            # Handle .data section
            if curr_section == ".data":
                result = data_section(line, curr_address)
                if result:
                    name, size, values = result
                    symbol_table.add_symbol(name=name, address=curr_address, size=size, value=values, section=curr_section)
                    hex_values = []
                    for val in values:
                       hex_values.append(hex(val))
                       
                    intermediate_file(format(curr_address, '08X'), None, symbol_table.sr_no, hex_values, None, None)
                    symbol_table.sr_no += 1
                    
                else:
                    hex_values = ', '.join(format(val, size) for val in values)
                    intermediate_file(format(curr_address, '08X'), None, None, hex_values, None, None)
                curr_address += size
                    
            # Handle .bss section
            elif curr_section == ".bss":
                result = bss_section(line, curr_address)
                if result:
                    name, size = result
                    symbol_table.add_symbol(name=name, address=curr_address, size=size, section=curr_section)
                    

                    intermediate_file(format(curr_address, '08X'), None, symbol_table.sr_no, None, None, None)
                    symbol_table.sr_no += 1

                    
                else:
                
                    intermediate_file(format(curr_address, '08X'), None, symbol_table.sr_no, None, None, None)
                curr_address += size

            # Handle .text section
            elif curr_section == ".text":
                label, curr_address, size, hex_value, opcode, arg1, arg2  = text_section(line, curr_address)
                if label:
                    for entry in symbol_table.table:
                        if entry['name'] == label:
                            print(f"Error: Label '{label}' inconsistently redefined.")
                            break

                    symbol_table.add_symbol(name=label, address=curr_address, section=curr_section)
                    intermediate_file(format(curr_address, '08X'), opcode, symbol_table.sr_no, hex_value, arg1, arg2)
                    
                    symbol_table.sr_no += 1

                else:

                    intermediate_file(format(curr_address, '08X'), opcode, None, hex_value, arg1, arg2)
                curr_address += size
    return symbol_table


def data_section(line, curr_address):
    directiveList = {"db": 1, "dw": 2, "dd": 4, "dq": 8}

    parts = line.split()
    if len(parts) < 3:
        print(f"Error: Invalid data section entry: {line}")
        return None

    name = parts[0]
    directive = parts[1]
    if directive not in directiveList:
        print(f"Error: Unknown directive '{directive}' in data section.")
        return None

    size = directiveList[directive]

    values = []
    for value in parts[2:]:
        for val in value.split(','):
            values.append(int(val.strip()))

    return name, size, values


def bss_section(line, curr_address):
    directiveList = {"resb": 1, "resw": 2, "resd": 4, "resq": 8}

    parts = line.split()
    if len(parts) != 3:
        print(f"Error: Invalid bss section entry: {line}")
        return None

    name = parts[0]
    directive = parts[1]
    if directive not in directiveList:
        print(f"Error: Unknown directive '{directive}' in bss section.")
        return None

    try:
        size = directiveList[directive] * int(parts[2])
    except ValueError:
        print(f"Error: Invalid size value in bss section: {line}")
        return None

    return name, size



def operand_type(operand):
    if operand in ["eax", "ebx", "ecx", "edx", "esp", "ebp", "esi", "edi"]:
        return "reg32"

    if re.match(r"^\d+$", operand) or re.match(r"^0x[0-9a-fA-F]+$", operand):
        if int(operand, 0) <= 255:
            return "imm8"
        else:
            return "imm32"

    if re.match(r"^\[.*\]$", operand):
        return "mem"

    if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", operand):
        return "rel8"
    return None


def instruction_size(instruction, args):
    for entry in opcode_table:
        if entry["instruction"] == instruction and entry["args"] == len(args):
            if len(args) == 1:
                arg_matches = operand_type(args[0]) == entry["arg1"]
            elif len(args) == 2:
                arg_matches = (
                    operand_type(args[0]) == entry["arg1"] and
                    operand_type(args[1]) == entry["arg2"]
                )
            else:
                arg_matches = False

            if arg_matches:
                return entry["size"]

    print(f"Error: Unknown instruction or operand combination '{instruction} {args}'.")
    return 0


def text_section(line, curr_address):
    label = None
    size = 0
    hex_value = None
    opcode = None
    rd = None
    arg1 = None
    arg2 = None
    line = line.strip()
    
    if not line or line.startswith(";"):
        return None, curr_address, size, hex_value, opcode, arg1, arg2

    parts = re.split(r"[ ,\t]+", line)
    if ":" in parts[0]:
        label = parts[0].strip(":")
        parts = parts[1:]

    if not parts:
        return label, curr_address, size, hex_value, opcode, arg1, arg2

    instruction = parts[0]
    args = parts[1:]
    
    for arg in args:
        if arg.startswith("0x"):
            hex_value = arg
        elif re.match(r"^\d+$", arg):
            hex_value = hex(int(arg))[2:].zfill(2)

    if instruction in ["global", "extern"]:
        return label, curr_address, size, hex_value, opcode, arg1, arg2

    size = instruction_size(instruction, args)

    for entry in opcode_table:
        if entry["instruction"] == instruction and entry["args"] == len(args):
            
            if len(args) == 1 and operand_type(args[0]) == entry["arg1"]:
                opcode = entry["sr_no"]
                arg1 = args[0]
                arg2 = None
                    

            elif len(args) == 2 and operand_type(args[0]) == entry["arg1"] and operand_type(args[1]) == entry["arg2"] :
                opcode = entry["sr_no"]
                
                if entry["mod_rm"]:
                    arg1 = args[0]
                    arg2 = args[1]
                    
            if entry["+rd"]:
                arg1 = args[0]

                                
    if opcode is None:
        print(f"Unknown instruction '{instruction}' at address {hex(curr_address)}")
                
    return label, curr_address, size, hex_value, opcode, arg1, arg2


def intermediate_file(curr_address, opcode, symbol, hex_value, arg1, arg2):
    file_empty = not os.path.exists("intermediate_file.txt") or os.stat("intermediate_file.txt").st_size == 0

    with open("intermediate_file.txt", "a") as intermediate_file:
        
        '''if file_empty:
            intermediate_file.write("Address\t\tOpcode\tSymbol\tHex_value\targ1\targ2\n\n")
        '''
        intermediate_file.write(f"{curr_address}\t{opcode}\t{symbol}\t{hex_value}\t{arg1}\t{arg2}\n")
        
        
# Pass 2
'''-----------------------------------------------------------------------------------------------------------------------------------'''

def generate_listing():
    symbol_table = generate_symbolTable("demo.asm")
    symboltable = symbol_table.table
    symbol_table.display()
    
    with open("intermediate_file.txt", 'r') as file:
        lines = file.readlines()

    if not lines:
        print("No lines to process")
        return

    processed_lines = []

    for line in lines:
        if line.strip() == '':
            continue
        
        parts = re.split(r"[\t]", line.strip())
        addr = parts[0]
        opcode = parts[1]
        sym_srno = parts[2]
        value = parts[3]
        arg1 = parts[4]
        arg2 = parts[5]
        
        if sym_srno != 'None':
            for entry in symboltable:
                if entry["sr_no"] == int(sym_srno):
        
                    if entry["section"] == ".data":
                        size = entry["size"]
                        result = process_data(value, size)
                        processed_lines.append(f"{entry['address']} {result}")

                        
                    elif entry["section"] == ".bss":
                        size = entry["size"]
                        result = process_bss(size)
                        processed_lines.append(f"{entry['address']} {result}")
                    
                            
        if opcode != 'None':
            result = process_text(addr, value, opcode,symboltable, arg1, arg2)
            processed_lines.append(f"{addr} {result}")
    
    with open("output.lst", 'w') as output_file:
        output_file.write("\n".join(processed_lines))
        
    os.remove("intermediate_file.txt")
        
    

def process_data(value, size):
    size = int(size, 16)
    value = eval(value)
    for i in range(len(value)):
        hex_value = value[i].lstrip("0x").upper()
        total_bits = size * 2                     
        value[i] = hex_value.zfill(total_bits)     
            
    reversed_pairs = ''
    for val in value:   
        pairs = []
        for i in range(0, len(val), 2):
            pairs.append(val[i:i+2])
        reversed_pairs += ''.join(pairs[::-1])
    return reversed_pairs

   
def process_bss(size):
    
    hex_size = size.lstrip("0x").upper()

    int_size = int(size,16)
    if int_size <= 8:
        return "?" * (2 * int_size)
    else:
        return f"<res {hex_size}h>"


def process_text(addr, value, opcode, symboltable, arg1, arg2):
    reg_arr = {'eax':0, 'ecx':1, 'edx':2, 'ebx':3, 'esp':4, 'ebp':5, 'esi':6, 'edi':7}
    jmp_inst = {'jmp', 'jz', 'jnz'}
    
    mod_rm = None
    digit = None
    arg1 = arg1.strip()
    arg2 = arg2.strip()
    
    if opcode != 'None':
        instruction = opcode_table[int(opcode) - 1]
        opcode = instruction['opcode']
        
        if '/' in opcode:
            parts = opcode.split('/')
            opcode = parts[0]
            digit = parts[1]
        
        if instruction['instruction'] in jmp_inst:
            
            if arg1 in reg_arr:
                mod_rm = (3 << 6) | (4 << 3) | reg_arr[arg1]
                mod_rm = format(mod_rm, '02X')
                return opcode + mod_rm
            
            else:
                label_addr = None
                for entry in symboltable:
                    if entry['name'] == arg1:
                        label_addr = entry['address']
                        break
                

                if label_addr is None:
                    print(f"Label '{arg1}' not found in symbol table.")
                    
                diff = int(label_addr, 16) - int(addr, 16) - 2
                
                if diff < 0:
                    diff = diff & 0xFF
                return opcode + format(diff, '02X')
                        
            
        if value != 'None':
            size = instruction['imm_size']
            hex_value = value.lstrip("0x").upper()
            total_bits = size * 2                     
            value = hex_value.zfill(total_bits)
            
        if instruction["+rd"]:
            sum = int(opcode, 16) + reg_arr[arg1]
            opcode = format(sum, '02X')
            
        if instruction["mod_rm"]:
            
            if arg1.startswith("["):
                argg1 = ''
                for i in arg1:
                    if i.isalpha():
                        argg1 += i
                arg1 = argg1
            
            if arg2.startswith("["):
                argg2 = ''
                for i in arg2:
                    if i.isalpha():
                        argg2 += i
                arg2 = argg2
                
            if digit:
                dest = reg_arr[arg1]
                src = int(digit)
            else:
                dest = reg_arr[arg1]
                src = reg_arr[arg2]
                
            if instruction['arg1'] == "reg32" and instruction['arg2'] == "reg32":
                rm = 3
                mod_rm = (rm << 6) | (src << 3) | dest

            elif (instruction['arg1'] == "reg32" and instruction['arg2'] == "mem") or (instruction['arg2'] == "reg32" and instruction['arg1'] == "mem"):
                rm = 0
                mod_rm = (rm << 6) | (dest << 3) | src

            else:
                rm = 3
                mod_rm = (rm << 6) | (src << 3) | dest
                
            mod_rm = format(mod_rm, '02X')

        result = opcode
        
        if mod_rm:
            result += mod_rm
            
        if value != 'None':
            result += value
            
        return result

filename = "demo.asm"
generate_listing()
