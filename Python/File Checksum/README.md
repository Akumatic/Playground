# File Checksum

## Description
`checksum.py` generates checksums of a given file and compares them to verify the integrity of a download.

## Usage
`checksum.py [-h] [--crc32] [--md5] [--sha1] [--sha256] [-b SIZE] [-c COMP] file`

- `[--crc32]`, `[--md5]`, `[--sha1]`, `[--sha256]`: The hashing algorithm(s) to be used to generate checksum. If no algorithm is specified, all four of them will be used.
- `[-b SIZE]` The amount of bits being read at a time to update the current hash. Default is 512.
- `[-c COMP]` If passed, it will compare the generated checksums with the given one. The input is case insensitive and will be converted to uppercase leters.