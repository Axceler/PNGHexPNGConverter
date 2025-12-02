#!/usr/bin/env python3
"""
Convert a hexdump (xxd-style or raw hex string) back into a PNG image file.
Can read from a text file or from direct text input.
"""

import argparse
import sys
import os

def find_png_data(binary_data: bytes) -> bytes:
    """
    Find and extract valid PNG data from binary bytes, even if padded.
    PNG files start with signature: 89 50 4E 47 0D 0A 1A 0A
    """
    PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'
    IEND_CHUNK = b'IEND'
    
    # Try to find PNG signature
    png_start = binary_data.find(PNG_SIGNATURE)
    
    if png_start == -1:
        # Check if entire file is PNG (starts with signature)
        if binary_data[:8] == PNG_SIGNATURE:
            png_start = 0
        else:
            raise ValueError("PNG signature not found in hexdump data. Expected signature: 89504e470d0a1a0a")
    
    # Extract from PNG signature onwards
    png_data = binary_data[png_start:]
    
    # Validate PNG structure by checking for IEND chunk
    iend_pos = png_data.rfind(IEND_CHUNK)
    if iend_pos == -1:
        raise ValueError("PNG IEND chunk not found. The hexdump may be incomplete or corrupted.")
    
    # PNG IEND chunk is: 4 bytes length (0x00000000), 4 bytes type (IEND), 4 bytes CRC
    # So we need 12 bytes after IEND
    iend_end = iend_pos + 12
    if len(png_data) < iend_end:
        # If we don't have enough data, try to use what we have but warn
        print("Warning: PNG may be incomplete. IEND chunk appears truncated.")
        return png_data
    
    # Return complete PNG (from signature to end of IEND chunk)
    return png_data[:iend_end]


def parse_hexdump(hexdump_data: str) -> bytes:
    """
    Parse a hexdump string (xxd-style or raw hex) into binary bytes.
    """
    hex_str = ''
    for line in hexdump_data.splitlines():
        line = line.strip()
        if not line:
            continue
        if ':' in line:  # xxd-style (offset + hex)
            try:
                _, hex_part = line.split(':', 1)
                # More robust parsing: remove ASCII part if present
                # xxd format: "offset: hexdata  ascii"
                # Try splitting by multiple spaces to separate hex from ASCII
                hex_part = hex_part.strip()
                # Remove ASCII part (anything after 2+ consecutive spaces or at position 48+)
                if '  ' in hex_part:
                    hex_part = hex_part.split('  ')[0]
                elif len(hex_part) > 48:
                    # xxd typically has 48 chars of hex, rest is ASCII
                    hex_part = hex_part[:48]
                hex_str += hex_part.replace(' ', '')
            except ValueError:
                continue
        else:
            # plain hex string line - remove any non-hex characters
            # Keep only 0-9, a-f, A-F
            cleaned = ''.join(c for c in line if c in '0123456789abcdefABCDEF')
            hex_str += cleaned
    
    if not hex_str:
        raise ValueError("No hex characters found in input")
    
    # Validate hex string length (must be even)
    if len(hex_str) % 2 != 0:
        raise ValueError(f"Hex string length is odd ({len(hex_str)} characters). Each byte requires 2 hex digits.")
    
    try:
        binary_data = bytes.fromhex(hex_str)
        # Try to find and extract valid PNG data
        return find_png_data(binary_data)
    except ValueError as e:
        # Re-raise PNG-specific errors
        if "PNG" in str(e) or "IEND" in str(e):
            raise
        # Provide more helpful error message for hex parsing errors
        raise ValueError(f"Invalid hex characters found. Hex strings can only contain 0-9, a-f, A-F. Original error: {e}")


def hexdump_to_png(hexdump_input: str, output_file: str, from_file: bool):
    """
    Convert the provided hexdump (from file or text) into a PNG file.
    """
    try:
        if from_file:
            if not os.path.exists(hexdump_input):
                print(f"Error: Input file not found: {hexdump_input}")
                sys.exit(1)
            with open(hexdump_input, 'r', encoding='utf-8') as f:
                data = f.read()
        else:
            data = hexdump_input

        if not data or not data.strip():
            print("Error: No hexdump data found.")
            sys.exit(1)

        img_bytes = parse_hexdump(data)
        
        if not img_bytes:
            print("Error: Failed to parse hexdump data. No valid hex bytes found.")
            sys.exit(1)

        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        with open(output_file, 'wb') as f:
            f.write(img_bytes)

        abs_output_path = os.path.abspath(output_file)
        file_size = len(img_bytes)
        
        # Validate PNG signature
        if img_bytes[:8] != b'\x89PNG\r\n\x1a\n':
            print("Warning: Output file does not have a valid PNG signature.")
        
        print(f"PNG successfully written to: {abs_output_path}")
        print(f"File size: {file_size:,} bytes")
        print(f"PNG signature verified: {img_bytes[:8].hex()}")
    except ValueError as e:
        error_msg = str(e)
        print(f"Error: {error_msg}")
        if "PNG signature" in error_msg or "IEND" in error_msg:
            print("\nThe hexdump file does not contain valid PNG data.")
            print("A valid PNG file must:")
            print("  1. Start with signature: 89 50 4E 47 0D 0A 1A 0A (89504e470d0a1a0a in hex)")
            print("  2. Contain an IEND chunk at the end")
            print("\nPlease check that:")
            print("  - The hexdump file was generated from a valid PNG image")
            print("  - The hexdump file is not corrupted or truncated")
            print("  - If the hexdump has padding, the script will try to find the PNG data automatically")
        else:
            print("Please ensure your hexdump file contains only hexadecimal characters (0-9, a-f, A-F)")
            print("Formats supported:")
            print("  - xxd format: '00000000: 8950 4e47 0d0a 1a0a  ...PNG....'")
            print("  - Raw hex: '89504e47 0d0a1a0a' or '89504e470d0a1a0a'")
        sys.exit(1)
    except IOError as e:
        print(f"Error: File I/O error - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Unexpected error - {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Convert a hexdump back into a PNG image file."
    )
    parser.add_argument(
        "-f", "--file",
        help="Path to hexdump text file (optional if using --text)"
    )
    parser.add_argument(
        "-t", "--text",
        help="Hexdump text input (can be raw or xxd format, quoted or piped)"
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Output PNG file name"
    )
    args = parser.parse_args()

    if not args.file and not args.text:
        print("Error: You must provide either --file or --text input.")
        sys.exit(1)

    # Determine output file path
    try:
        if args.file:
            # If output is just a filename (no directory), place it in same directory as input file
            if os.path.dirname(args.output):
                output_path = args.output
            else:
                # Get absolute path of input file and use its directory
                input_abs = os.path.abspath(args.file)
                input_dir = os.path.dirname(input_abs)
                if not input_dir:
                    input_dir = os.getcwd()
                output_path = os.path.join(input_dir, args.output)
            hexdump_to_png(args.file, output_path, from_file=True)
        else:
            # For text input, use current working directory if output is just a filename
            if os.path.dirname(args.output):
                output_path = args.output
            else:
                output_path = os.path.join(os.getcwd(), args.output)
            hexdump_to_png(args.text, output_path, from_file=False)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)


if __name__ == "__main__":
    main()