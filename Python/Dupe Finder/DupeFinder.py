import sys, os, hashlib, time

class Data:
    def __init__(self):
        self.sum = 0
        self.hashes = {}

BLOCK_SIZE = 2 ** 16

def md5calc(fname):
    hash = hashlib.md5()
    with open(fname, "rb") as f:
        for data in iter(lambda: f.read(BLOCK_SIZE), b""):
            hash.update(data)
    return hash.hexdigest()

def readFolder(path, data):
    hash = None
    curFile = None
    for r, d, f in os.walk(path):
        for file in f:
            curFile = os.path.join(r, file)
            #print(f"Hashing {curFile}", end = "\r")
            hash = md5calc(curFile)
            if hash not in data.hashes:
                data.hashes[hash] = curFile
            elif data.hashes[hash] != curFile:
                try:
                    os.remove(curFile)
                    data.sum += 1
                    print(f"- {curFile}\n  {data.hashes[hash]}\n"
                        f"Deleted {data.sum} files so far\n")
                except PermissionError:
                    print(f"\nMissing Permissions. Could not remove {curFile}\n")

t = time.time()
path = [os.getcwd()] if len(sys.argv) == 1 else sys.argv[1:]
d = Data()
for p in path:
    if os.path.isdir(p):
        temp = d.sum
        readFolder(p, d)
        print(f"Deleted {d.sum - temp} duplicate files in {p}")
print(f"Total deleted files: {d.sum}")
print(f"Calculation time: {time.time() - t} s")