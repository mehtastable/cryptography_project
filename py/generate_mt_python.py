import random
import sys

def generate(filename, n_bits, seed):
    random.seed(seed)

    with open(filename, "wb") as f:
        buffer = 0
        count = 0

        while n_bits > 0:
            value = random.getrandbits(32)

            for i in range(32):
                if n_bits == 0:
                    break
                bit = (value >> (31 - i)) & 1
                buffer = (buffer << 1) | bit
                count += 1
                n_bits -= 1

                if count == 8:
                    f.write(bytes([buffer]))
                    buffer = 0
                    count = 0

        if count > 0:
            buffer <<= (8 - count)
            f.write(bytes([buffer]))

if __name__ == "__main__":
    generate(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
