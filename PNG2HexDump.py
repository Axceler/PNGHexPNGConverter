#!/usr/bin/env python3
"""
Convert a PNG (or any binary file) into a hexdump.
Optionally choose plain or xxd-style formatted output.
"""

import argparse
import textwrap

def file_to_hexdump(input_file, output_file=None, style="plain"):
    with open(input_file, 'rb') as f:
        data = f.read()

    if style == "plain":
        # Simple continuous hex string
        hex_str = data.hex()
    elif style == "xxd":
        # xxd-style formatted dump (offset + spaced bytes)
        hex_str = ""
        for offset in range(0, len(data), 16):
            chunk = data[offset:offset + 16]
            hex_part = " ".join(f"{b:02x}" for b in chunk)
            ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
            hex_str += f"{offset:08x}: {hex_part:<48}  {ascii_part}\n"
    else:
        raise ValueError("Invalid style. Use 'plain' or 'xxd'.")

    # Write or print
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(hex_str)
        print(f"Hexdump written to: {output_file}")
    else:
        print(hex_str)


def main():
    parser = argparse.ArgumentParser(
        description="Convert a PNG (or any binary file) to hexdump."
    )
    parser.add_argument("input", help="Input PNG or binary file")
    parser.add_argument("-o", "--output", help="Output text file (optional)")
    parser.add_argument("-s", "--style", choices=["plain", "xxd"], default="plain",
                        help="Output style: 'plain' (default) or 'xxd'")
    args = parser.parse_args()

    file_to_hexdump(args.input, args.output, args.style)


if __name__ == "__main__":
    main()
