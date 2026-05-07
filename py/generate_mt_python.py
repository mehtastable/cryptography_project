### import packages
import random
import sys

### generate bits function
def generate(filename, n_bits, seed):
    ### use per trial seed
    random.seed(seed)

    ### open/create binary file
    with open(filename, "wb") as f:

        ### initialize buffer and count
        buffer = 0
        count = 0

        ### generate bits
        while n_bits > 0:

            ### generate 32 bits at a time
            value = random.getrandbits(32)

            ### package as bytes
            for i in range(32):
                if n_bits == 0:
                    break
                bit = (value >> (31 - i)) & 1
                buffer = (buffer << 1) | bit
                count += 1
                n_bits -= 1

                ### write bytes to file
                if count == 8:
                    f.write(bytes([buffer]))

                    ### reset buffer and count
                    buffer = 0
                    count = 0

        ### write leftover bits to binary file
        if count > 0:
            buffer <<= (8 - count)
            f.write(bytes([buffer]))

### program entry point
if __name__ == "__main__":

    ### filename, n_bits, seed
    generate(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
