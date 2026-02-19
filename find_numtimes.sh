#!/bin/bash
# find_numtimes.sh — discover the --numtimes that makes BabelStream run ~60s
#
# Uses a simple scaling approach:
#   1. Start with a small numtimes, measure duration
#   2. Extrapolate linearly to estimate numtimes for 60s
#   3. Run with that estimate, measure again
#   4. Repeat until within tolerance

STREAM_BIN="/lustre/hpe/ws13/ws13.a/ws/hpckkuec-babelstream/BabelStream/build/hip-stream"
ARRAYSIZE=268435456
TARGET_SECS=65
TOLERANCE=5          # accept if within ±5s of target
MAX_ITERS=8          # safety limit on search iterations
LOGFILE="logs/numtimes_search.log"
mkdir -p logs

echo "=== BabelStream numtimes search ===" | tee "$LOGFILE"
echo "Target duration: ${TARGET_SECS}s (±${TOLERANCE}s)" | tee -a "$LOGFILE"
echo "Array size: $ARRAYSIZE" | tee -a "$LOGFILE"
echo "---" | tee -a "$LOGFILE"

run_bench() {
    local nt=$1
    local start end duration
    start=$(date +%s.%N)
    HIP_VISIBLE_DEVICES=0 "$STREAM_BIN" --arraysize "$ARRAYSIZE" --numtimes "$nt" > /dev/null 2>&1
    end=$(date +%s.%N)
    duration=$(echo "$end - $start" | bc)
    echo "$duration"
}

# Initial probe with numtimes=10
NT=600
echo "[iter 0] numtimes=$NT ..." | tee -a "$LOGFILE"
DUR=$(run_bench $NT)
echo "[iter 0] numtimes=$NT  duration=${DUR}s" | tee -a "$LOGFILE"

for i in $(seq 1 $MAX_ITERS); do
    # Extrapolate: rate = NT / DUR, so target NT ≈ rate * TARGET_SECS
    NT_NEW=$(echo "$NT * $TARGET_SECS / $DUR" | bc)
    # Clamp to minimum of 2
    if [ "$NT_NEW" -lt 2 ]; then NT_NEW=2; fi

    echo "[iter $i] numtimes=$NT_NEW (extrapolated from ${NT}/${DUR}s) ..." | tee -a "$LOGFILE"
    DUR=$(run_bench "$NT_NEW")
    NT=$NT_NEW
    echo "[iter $i] numtimes=$NT  duration=${DUR}s" | tee -a "$LOGFILE"

    # Check if within tolerance
    DIFF=$(echo "$DUR - $TARGET_SECS" | bc)
    ABS_DIFF=$(echo "${DIFF#-}")
    IN_RANGE=$(echo "$ABS_DIFF <= $TOLERANCE" | bc)
    if [ "$IN_RANGE" -eq 1 ]; then
        echo "---" | tee -a "$LOGFILE"
        echo "FOUND: numtimes=$NT gives ${DUR}s (target: ${TARGET_SECS}s ±${TOLERANCE}s)" | tee -a "$LOGFILE"
        exit 0
    fi
done

echo "---" | tee -a "$LOGFILE"
echo "BEST after $MAX_ITERS iterations: numtimes=$NT gives ${DUR}s" | tee -a "$LOGFILE"
