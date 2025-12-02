# PNGHexPNGConverter

A Python toolkit for converting PNG images to hexdump format and vice versa. Perfect for embedding image data in text files, code, or for educational purposes.

## Features

- 🔄 **PNG to Hexdump**: Convert PNG images to hexadecimal text format
- 🔄 **Hexdump to PNG**: Convert hexdump text back to PNG images
- 📝 **Multiple Formats**: Supports both plain hex strings and xxd-style formatted hexdumps
- 🔍 **Smart Detection**: Automatically finds PNG data even if hexdump contains padding
- ✅ **Validation**: Verifies PNG signatures and structure
- 🛠️ **Flexible Input**: Accept input from files or direct text input

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Installation

No installation required! Just download the scripts and run them directly.

```bash
git clone https://github.com/yourusername/PNGHexPNGConverter.git
cd PNGHexPNGConverter
```

## Usage

### PNG2HexDump.py - Convert PNG to Hexdump

Converts a PNG image (or any binary file) into a hexdump text file.

#### Basic Usage

```bash
python PNG2HexDump.py <input.png> [-o output.txt] [-s style]
```

#### Options

- `input` (required): Input PNG or binary file
- `-o, --output`: Output text file (optional, prints to console if omitted)
- `-s, --style`: Output style - `plain` (default) or `xxd`

#### Examples

```bash
# Convert PNG to plain hex string (default)
python PNG2HexDump.py image.png -o image_hex.txt

# Convert PNG to xxd-style format
python PNG2HexDump.py image.png -o image_hex_xxd.txt -s xxd

# Print hexdump to console
python PNG2HexDump.py image.png

# Convert with xxd format
python PNG2HexDump.py image.png -s xxd -o output.txt
```

#### Output Formats

**Plain format** (default):
```
89504e470d0a1a0a0000000d49484452000001000000010008060000005c72a866...
```

**xxd format**:
```
00000000: 8950 4e47 0d0a 1a0a 0000 000d 4948 4452  ...PNG........IHDR
00000010: 0000 0100 0000 0100 0806 0000 005c 72a8  .............\r.
...
```

### HexDumpToPNG.py - Convert Hexdump to PNG

Converts a hexdump text file back into a PNG image file.

#### Basic Usage

```bash
python HexDumpToPNG.py -f <input.txt> -o <output.png>
# OR
python HexDumpToPNG.py -t "<hex_text>" -o <output.png>
```

#### Options

- `-f, --file`: Path to hexdump text file
- `-t, --text`: Hexdump text input (can be raw or xxd format)
- `-o, --output` (required): Output PNG file name

#### Examples

```bash
# Convert hexdump file to PNG
python HexDumpToPNG.py -f image_hex.txt -o image_recovered.png

# Convert from text input
python HexDumpToPNG.py -t "89504e470d0a1a0a..." -o output.png

# Using short flags
python HexDumpToPNG.py -f superman_hex.txt -o superman.png
```

#### Features

- **Automatic PNG Detection**: Finds PNG signature even if hexdump has padding or extra data
- **Format Support**: Handles both plain hex strings and xxd-style hexdumps
- **Validation**: Verifies PNG signature and structure
- **Error Handling**: Clear error messages if PNG data is invalid or missing

## Complete Workflow Example

```bash
# Step 1: Convert PNG to hexdump
python PNG2HexDump.py image.png -o image_hex.txt

# Step 2: Convert hexdump back to PNG
python HexDumpToPNG.py -f image_hex.txt -o image_recovered.png

# Verify the round-trip conversion
# image.png and image_recovered.png should be identical
```

## File Descriptions

- **PNG2HexDump.py**: Converts PNG images to hexdump text format
- **HexDumpToPNG.py**: Converts hexdump text back to PNG images

## Supported Formats

### Input Formats (for HexDumpToPNG.py)

1. **Plain hex string**:
   ```
   89504e470d0a1a0a0000000d49484452...
   ```

2. **xxd-style format**:
   ```
   00000000: 8950 4e47 0d0a 1a0a 0000 000d 4948 4452  ...PNG........IHDR
   00000010: 0000 0100 0000 0100 0806 0000 005c 72a8  .............\r.
   ```

3. **Hex with padding**: The script automatically finds PNG data even if the hexdump contains padding bytes before the PNG signature.

## Error Handling

The scripts provide clear error messages for common issues:

- **Missing PNG signature**: If the hexdump doesn't contain valid PNG data
- **Invalid hex characters**: If the input contains non-hexadecimal characters
- **Incomplete PNG**: Warnings if PNG structure appears truncated
- **File not found**: Clear messages for missing input files

## Use Cases

- 📝 Embed image data in source code or text files
- 🔒 Store images in text-only formats
- 📚 Educational purposes for understanding binary file formats
- 🔄 Convert between binary and text representations
- 📦 Include images in documentation or configuration files

## Limitations

- Only works with PNG format images
- Large images will generate very large hexdump files
- Hexdump files are not compressed (much larger than original PNG)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

Created for converting PNG images to hexdump format and back.

## Notes

- The hexdump format preserves all PNG data exactly
- Round-trip conversion (PNG → hexdump → PNG) should produce identical files
- xxd format is more human-readable but takes more space
- Plain format is more compact and easier to embed in code

---

**Enjoy converting your PNG images!** 🎨

