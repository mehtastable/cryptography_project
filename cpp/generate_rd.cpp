#include <iostream>
#include <fstream>
#include <random>
#include <cstdint>

// main
int main(int argc, char* argv[]) {
    
    // check args
    if (argc < 3) {
        std::cerr << "Usage: ./rd_cpp <output_file> <num_bits>\n";
        return 1;
    }

    // parse args
    const char* filename = argv[1];
    size_t n_bits = std::stoull(argv[2]);

    // initialize random_device
    std::random_device rd;

    // print entropy per trial
    std::cout << "random_device entropy: " << rd.entropy() << std::endl;

    // create binary file
    std::ofstream out(filename, std::ios::binary);

    // initialize buffer and bit_count
    uint8_t buffer = 0;
    int bit_count = 0;

    // generate bits and convert to bytes
    while (n_bits > 0) {
        
        // generate random bits
        uint32_t value = rd();

        // process bits
        for (int i = 0; i < 32 && n_bits > 0; i++, n_bits--) {
            int bit = (value >> (31 - i)) & 1;
            buffer = (buffer << 1) | bit;
            bit_count++;

            // write byte to binary file
            if (bit_count == 8) {
                out.put(static_cast<char>(buffer));
                buffer = 0;
                bit_count = 0;
            }
        }
    }

    // write leftover bits to binary file
    if (bit_count > 0) {
        buffer <<= (8 - bit_count);
        out.put(static_cast<char>(buffer));
    }

    return 0;
}

