### import packages
import os
import sys

### generate bits function
def generate(filename, n_bits):

    ### convert bits to bytes
    n_bytes = (n_bits + 7) // 8

    ### generate bytes
    data = os.urandom(n_bytes)

    ### write bytes to file
    with open(filename, "wb") as f:
        f.write(data)

### program entry point
if __name__ == "__main__":

    ### filename, n_bits
    generate(sys.argv[1], int(sys.argv[2]))
