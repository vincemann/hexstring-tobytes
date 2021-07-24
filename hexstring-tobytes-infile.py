import sys

# srcipt.py target-file hexstring

# get hexstring: xxd -p file | tr -d '\n'
filename = sys.argv[1]
hexadecimal_string = sys.argv[2]
parsed_hexadecimal_string = ""
parts = hexadecimal_string.split("\\x")
index = 0
skip = False
for part in parts:
    if part == "":
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
f = open(filename, 'wb')
f.write(data)
f.close()