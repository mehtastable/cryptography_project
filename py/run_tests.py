import numpy as np
from scipy.special import erfc, gammaincc
import math
import csv
import sys

### read bits from binary files
def read_bits(file):
    data = np.fromfile(file, dtype=np.uint8)
    return np.unpackbits(data)

### monobit test
def monobit_test(bits):
    bits = np.asarray(bits, dtype=np.int8)
    n = len(bits)
    S_n = np.sum(2 * bits - 1)
    s_obs = abs(S_n) / np.sqrt(n)
    p_value = erfc(s_obs / math.sqrt(2))
    return ("Monobit", float(p_value), p_value > 0.01)

### frequency block test
def block_frequency_test(bits, M=128):
    n = len(bits)
    N = n // M
    if N == 0:
        return ("Block Frequency", 0.0, False)
    blocks = bits[:N * M].reshape((N, M))
    pi = np.mean(blocks, axis=1)
    chi_sq = 4 * M * np.sum((pi - 0.5) ** 2)
    p_value = gammaincc(N / 2, chi_sq / 2)
    return ("Block Frequency", float(p_value), p_value > 0.01)

### runs test
def runs_test(bits):
    n = len(bits)
    pi = np.mean(bits)
    if abs(pi - 0.5) >= (2 / np.sqrt(n)):
        return ("Runs", 0.0, False)
    V_n_obs = 1 + np.sum(bits[1:] != bits[:-1])
    p_value = erfc(abs(V_n_obs - (2 * n * pi * (1 - pi))) / (2 * np.sqrt(2 * n) * pi * (1 - pi)))
    return ("Runs", float(p_value), p_value > 0.01)

### run all tests
def run_tests(bits):
    return [
        monobit_test(bits),
        block_frequency_test(bits),
        runs_test(bits)
    ]

### write results
def run(input_file, output):
    infile = sys.argv[1]
    outfile = sys.argv[2]
    bits = read_bits(infile)
    results = run_tests(bits)

    with open(outfile, "w") as f:
        f.write("Test,p-value,Pass\n")
        for name, p, passed in results:
            f.write(f"{name},{p},{passed}\n")

### main program entry point
if __name__ == "__main__":
    ### (bin_dir, csv_dir)
    run(sys.argv[1], sys.argv[2])
