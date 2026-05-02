import os
import sys

def generate(filename, n_bits):
    n_bytes = (n_bits + 7) // 8
    data = os.urandom(n_bytes)

    with open(filename, "wb") as f:
        f.write(data)

if __name__ == "__main__":
    generate(sys.argv[1], int(sys.argv[2]))
