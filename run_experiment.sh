#!/bin/bash

### set failures
set -euo pipefail

### locate base directory
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$BASE_DIR"

### activate python virtual environment
source venv/bin/activate

TRIALS=1000
BITS=1000000

CPP_DIR="$BASE_DIR/cpp"
PY_DIR="$BASE_DIR/py"
DAT_DIR="$BASE_DIR/data_$TRIALS"
BIN_DIR="$DAT_DIR/bins_$TRIALS"
CSV_DIR="$DAT_DIR/trials_$TRIALS"
RES_DIR="$BASE_DIR/results_$TRIALS"

mkdir -p "$DAT_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$CSV_DIR"
mkdir -p "$RES_DIR"

echo "======================================"
echo "Randomness Experiment Starting"
echo "Trials: $TRIALS"
echo "Bits per sample: $BITS"
echo "======================================"

### trials loop
for i in $(seq 1 $TRIALS); do
	### generate random seed for mt19937 generators
	SEED=$RANDOM$RANDOM

    echo "[Trial $i] seed=$SEED starting..."

    ### cpp std::mt19937
    $CPP_DIR/generate_mt_cpp "$BIN_DIR/cpp_mt_${i}.bin" "$BITS" "$SEED"
    python3 $PY_DIR/run_tests.py "$BIN_DIR/cpp_mt_${i}.bin" "$CSV_DIR/cpp_mt_${i}.csv"

    ### cpp std::random_device
    $CPP_DIR/generate_rd_cpp "$BIN_DIR/cpp_rd_${i}.bin" "$BITS"
    python3 $PY_DIR/run_tests.py "$BIN_DIR/cpp_rd_${i}.bin" "$CSV_DIR/cpp_rd_${i}.csv"

    ### python random.getrandbits
    python3 $PY_DIR/generate_mt_python.py "$BIN_DIR/py_mt_${i}.bin" "$BITS" "$SEED"
    python3 $PY_DIR/run_tests.py "$BIN_DIR/py_mt_${i}.bin" "$CSV_DIR/py_mt_${i}.csv"

    ### python os.urandom
    python3 $PY_DIR/generate_os_python.py "$BIN_DIR/py_os_${i}.bin" "$BITS"
    python3 $PY_DIR/run_tests.py "$BIN_DIR/py_os_${i}.bin" "$CSV_DIR/py_os_${i}.csv"

    echo "[Trial $i] complete"
    echo "--------------------------------------"
done

echo "All trials completed."

### generate summary and plots
echo "Generating summary + plots..."
python3 $PY_DIR/summary_and_plots.py "$BASE_DIR" "$TRIALS"

### tests complete
echo "======================================"
echo "DONE"
echo "Outputs:"
echo " - $BIN_DIR"
echo " - $CSV_DIR"
echo " - $RES_DIR/summary_stats.csv"
echo " - $RES_DIR/summary_report.txt"
echo " - $RES_DIR/combined_boxplots.png"
echo "======================================"
