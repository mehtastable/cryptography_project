#include <iostream>
#include <fstream>
#include <random>
#include <cstdint>

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cerr << "Usage: ./rd_cpp <output_file> <num_bits>\n";
        return 1;
    }

    const char* filename = argv[1];
    size_t n_bits = std::stoull(argv[2]);

    std::random_device rd;
    std::cout << "random_device entropy: " << rd.entropy() << std::endl;

    std::ofstream out(filename, std::ios::binary);

    uint8_t buffer = 0;
    int bit_count = 0;

    while (n_bits > 0) {
        uint32_t value = rd();

        for (int i = 0; i < 32 && n_bits > 0; i++, n_bits--) {
            int bit = (value >> (31 - i)) & 1;
            buffer = (buffer << 1) | bit;
            bit_count++;

            if (bit_count == 8) {
                out.put(static_cast<char>(buffer));
                buffer = 0;
                bit_count = 0;
            }
        }
    }

    if (bit_count > 0) {
        buffer <<= (8 - bit_count);
        out.put(static_cast<char>(buffer));
    }

    return 0;
}
