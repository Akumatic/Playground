#!/usr/bin/env python3

# SPDX-License-Identifier: MIT
# Copyright (c) 2020 Akumatic 

import hashlib, zlib, argparse

def _hash (
        function,
        file: str,
        blocksize: int
    ) -> str:
    """ Hashing the given file with the given function
    
    Args:
        function:
            the function to be used to generate or calculate the hash
        file (str):
            the path to the file
        blocksize (int):
            the amount of bytes to be read at a time to update the hash

    Returns:
        a string containing the calculated hash with uppercase letters.
    """
    try:
        # MD5, SHA1 and SHA256
        if function.__module__ == "_hashlib":
            hash = function()
            with open(file, "rb") as f:
                for chunk in iter(lambda: f.read(blocksize), b""):
                    hash.update(chunk)
            return hash.hexdigest().upper()

        # CRC32
        elif function.__module__ == "zlib":
            hash = 0
            with open(file, "rb") as f:
                for chunk in iter(lambda: f.read(blocksize), b""):
                    hash = function(chunk, hash)
            return ("%08X" % (hash & 0xFFFFFFFF)).upper()
    except FileNotFoundError:
        print(f"checksum.py: error: argument file: '{file}' not found")
        exit(1)

def in_bytes (
        x
    ) -> int:
    """ Verifies the passed input for the amount of bytes to be read at a time.
        Input has to be an integer and bigger or equals to 1.
    
    Args:
        x:
            The value to be verified
    
    Raises:
        ArgumentTypeError
            if the given value is no integer or smaller than 1
    """
    try:
        x = int(x)
        if x < 1:
            raise argparse.ArgumentTypeError("invalid integer value. "
                "minimum amount of bytes is 1")
        return x
    except ValueError:
        raise argparse.ArgumentTypeError("invalid integer value.")


def parse_args (
        algorithms: list
    ) -> dict:
    """ Parses cli arguments.

    Args:
        algorithms (list):
            a list with algorithms usable in this program.
    
    Returns:
        a dict containing the parsed arguments.
    """
    p = argparse.ArgumentParser(
        description="A tool to calculate and compare checksums.")
    for algo in algorithms:
        p.add_argument(f"--{algo.lower()}", action="store_true", dest=algo,
        help=f"calculates checksum with {algo}")
    p.add_argument("-b", "--blocksize", dest="size", default=64, type=in_bytes,
        help="specify the amount of bytes to be read at a time")
    p.add_argument("-c", "--compare", dest="comp",
        help="compare the given checksum with the calculated ones.")
    p.add_argument("file",
        help="the file you want to calculate the checksums for.")
    return vars(p.parse_args())

def compare (
        hashes: dict,
        hash: str
    ) -> tuple:
    """ Compares a hash with a dict of given hashes.

    Args:
        hashes (dict):
            a dict containing the hashing method as key and the hash as value
        hash:
            a string with the hash to be compared

    Returns:
        a tuple containing a boolean and a string.
        the boolean stores if a match was found.
        the string stores the matched hashing algorithm or None.
    """
    for h in hashes:
        if hashes[h] == hash:
            return (True, h)
    return (False, None)

if __name__ == __name__:
    # dict containing hashing algorithms to be used
    algorithms = {
        "CRC32": zlib.crc32,
        "MD5": hashlib.md5,
        "SHA1": hashlib.sha1,
        "SHA256": hashlib.sha256
    }
    args = parse_args(algorithms.keys())
    # boolean to check if any hashing algorithm was specified
    passed_algos = any([1 for x in algorithms if args[x]])

    print("Checksums:\n==========")
    hashes = dict()
    for a in algorithms:
        if args[a] or not passed_algos:
            hashes[a] = _hash(algorithms[a], args["file"], args["size"])
            print(a, "\t", hashes[a])

    if args["comp"]:
        found, algorithm = compare(hashes, args["comp"].upper())
        if found:
            print("\nMatch found:", algorithm)
        else:
            print("\nNo match found.")