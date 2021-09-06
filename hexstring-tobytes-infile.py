import sys
import time
# srcipt.py target-file hexstring


def write_to_file(data):
    f = open(filename, 'wb')
    f.write(data)
    f.close()


# get hexstring: xxd -p file | tr -d '\n'4
filename = sys.argv[1]
hexadecimal_string = sys.argv[2]
parsed_hexadecimal_string = ""

first_part_without_x = None
try:
    first_x_index = hexadecimal_string.index("\\x")
    if first_x_index == 0:
        # do nothing, starts with \\x wont cause problems
        time.sleep(0.1)
    else:
        first_part = hexadecimal_string[:first_x_index]
        first_part_without_x = first_part

except ValueError:
    write_to_file(bytes(hexadecimal_string, "utf-8"))
    exit(0)

parts = hexadecimal_string.split("\\x")

parts_index = 0
skip = False

for part in parts:
    parts_index += 1
    if part == "":
        continue
    if parts_index == 1 and first_part_without_x:
        for c in first_part_without_x:
            hex_c = hex(ord(c)).replace("0x", "")
            parsed_hexadecimal_string += hex_c
        continue
    parsed_hexadecimal_string += part[:2]
    for i in range(len(part)-2):
        if skip:
            skip = False
            continue
        unparsed = part[i+2]
        # newline does not work, maybe convert to bytes in this special case
        # and get hex from that, and reconvert to hex string with hex function
        if unparsed == '\\':
            skip = True
            unparsed += part[i + 3]
            # \\n in unparsed
            unparsed = unparsed[1:]
            if unparsed == 'a':
                unparsed = "\a"
            if unparsed == 'b':
                unparsed = "\b"
            if unparsed == 't':
                unparsed = "\t"
            if unparsed == 'n':
                unparsed = "\n"
            if unparsed == 'v':
                unparsed = "\v"
            if unparsed == 'f':
                unparsed = "\f"
            if unparsed == 'r':
                unparsed = "\r"
            i+=2
        unparsed = hex(ord(unparsed)).replace("0x", "")
        if len(unparsed) == 1:
            unparsed = "0"+unparsed
        parsed_hexadecimal_string += unparsed

data = bytearray.fromhex(parsed_hexadecimal_string)
write_to_file(data)