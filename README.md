# C++ and Python Random Generator Test Using NIST Test Suite

## Description
This project was created for a cryptography class.

It tests 2 C++ and 2 Python random number generators (RNGs) against the NIST test suite for random numbers.
- C++ std::mt19937
- C++ std::random_device
- Python random.getrandbits
- Python os.urandom
    
The first three NIST tests were recreated and used to test the generated sequences.
1. Frequency (Monobit) Test
2. Frequency Within a Block Test
3. Runs Test

## Installation
If running in Codespaces:
- Python virtual environment should download the required packages using the requirements.txt.

If running locally:
1. Navigate to the project directory
2. Activate virtual environment: `source venv/bin/activate`
3. Install the requirements: `pip install -r requirements.txt`
4. Deactivate the virtual environment: `deactivate`

## Running the program
Using the terminal/command line:
1. Navigate to project folder
2. Run the bash script run_experiment.sh: `./run_experiment.sh`
3. Enter the number of trials to run: `100` (NIST recommends 100 or more trials)
4. Enter the number of bits to generate: `1000000` (NIST recommends 1,000,000 or more bits)

The program will run the requested number of trials, generating the requested number of bits each time and the bit sequence as a binary file in the data folder.

The bit sequences will be tested using the three NIST tests above and save as .csv files in the results folder.

The results will be plotted and saved as .txt, .csv, and .png files in the results folder.

## Future Work
1. Recreate all 15 tests and include them in the pipeline.
2. Implement the NIST sts tool in the pipeline to ensure that my implementation of the tests are accurate.
3. Add different C++ and Python generators.
