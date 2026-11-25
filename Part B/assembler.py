import sys
from pathlib import Path

# Predefined Hack symbols
SYMBOLS = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "SCREEN": 16384, "KBD": 24576
}

for i in range(16):
    SYMBOLS[f"R{i}"] = i

# Hack computation instructions
COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "M": "1110000",
    "!D": "0001101", "!A": "0110001", "!M": "1110001",
    "-D": "0001111", "-A": "0110011", "-M": "1110011",
    "D+1": "0011111", "A+1": "0110111", "M+1": "1110111",
    "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "D+M": "1000010",
    "D-A": "0010011", "D-M": "1010011",
    "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "D&M": "1000000",
    "D|A": "0010101", "D|M": "1010101"
}

DEST = {
    "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111"
}

JUMP = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
}

def clean_lines(filename):
    instructions = []
    with open(filename, "r") as file:
        for line_number, line in enumerate(file, 1):
            line = line.split("//")[0].strip()
            line = "".join(line.split())
            if line:
                instructions.append((line_number, line))
    return instructions

def assemble(filename):
    global SYMBOLS

    SYMBOLS = {
        "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
        "SCREEN": 16384, "KBD": 24576
    }
    for i in range(16):
        SYMBOLS[f"R{i}"] = i

    instructions = clean_lines(filename)
    labels = {}
    variables = {}
    custom_symbols = {}

    rom_address = 0

    for line_number, instruction in instructions:
        if instruction.startswith("(") and instruction.endswith(")"):
            label = instruction[1:-1]

            if not label or label in SYMBOLS or label in labels:
                raise ValueError(f"Line {line_number}: Invalid or duplicate label {label}")

            labels[label] = rom_address
            custom_symbols[label] = rom_address
        else:
            rom_address += 1

    SYMBOLS.update(labels)

    next_variable = 16
    machine_code = []

    for line_number, instruction in instructions:
        try:
            if instruction.startswith("(") and instruction.endswith(")"):
                continue

            if instruction.startswith("@"):
                symbol = instruction[1:]

                if not symbol:
                    raise ValueError("Missing A-instruction value")

                if symbol.isdigit():
                    address = int(symbol)
                else:
                    if not symbol[0].isalpha() and symbol[0] not in "_.$:":
                        raise ValueError("Invalid symbol")

                    if symbol not in SYMBOLS:
                        SYMBOLS[symbol] = next_variable
                        variables[symbol] = next_variable
                        custom_symbols[symbol] = next_variable
                        next_variable += 1

                    address = SYMBOLS[symbol]

                if not 0 <= address <= 32767:
                    raise ValueError("Address must be between 0 and 32767")

                binary = format(address, "016b")

            else:
                if instruction.count(";") > 1 or instruction.count("=") > 1:
                    raise ValueError("Invalid C-instruction")

                if "=" in instruction:
                    dest, rest = instruction.split("=")
                else:
                    dest, rest = "", instruction

                if ";" in rest:
                    comp, jump = rest.split(";")
                else:
                    comp, jump = rest, ""

                if comp not in COMP:
                    raise ValueError(f"Invalid computation: {comp}")
                if dest not in DEST:
                    raise ValueError(f"Invalid destination: {dest}")
                if jump not in JUMP:
                    raise ValueError(f"Invalid jump: {jump}")

                binary = "111" + COMP[comp] + DEST[dest] + JUMP[jump]

            machine_code.append(binary)

        except (ValueError, IndexError) as error:
            raise ValueError(f"Line {line_number}: {error}") from error

    output_file = Path(filename).with_suffix(".hack")
    output_file.write_text("\n".join(machine_code) + "\n")

    # K = 69
    symbols_file = Path(filename).parent / "symbols.txt"
    with open(symbols_file, "w") as file:
        file.write("Symbol\tAddress\tType\n")
        for name, address in sorted(custom_symbols.items()):
            symbol_type = "Label" if name in labels else "Variable"
            file.write(f"{name}\t{address}\t{symbol_type}\n")

    print(f"Assembly successful!")
    print(f"Input: {filename}")
    print(f"Output: {output_file}")
    print(f"Instructions: {len(machine_code)}")
    print(f"Symbols saved: {symbols_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python assembler.py filename.asm")
        sys.exit(1)

    try:
        assemble(sys.argv[1])
    except (ValueError, FileNotFoundError) as error:
        print(f"Error: {error}")
        sys.exit(1)
