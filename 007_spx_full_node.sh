#!/bin/bash
OUTDIR=/zhome/academic/HLRS/hlrs/hpckkuec/cpx_tpx_test/logs/007
mkdir -p $OUTDIR

for i in $(seq 0 3); do
  # Run for roughle 1 minutes
  # Array size is set to 268435456 (1GB) Sam array size as in CPX case. Cannot multiply by 6 because log_2 of array size must be an integer.
  HIP_VISIBLE_DEVICES=$i /lustre/hpe/ws13/ws13.a/ws/hpckkuec-babelstream/BabelStream/build/hip-stream \
    --arraysize 268435456 \
    --numtimes 1500 \
    > $OUTDIR/device_${i}.txt \
    2>&1 \
    &
done
wait

echo "=== Summary ==="
for i in $(seq 0 3); do
  echo "--- Device $i ---"
  grep -E "^(Copy|Mul|Add|Triad|Dot)" $OUTDIR/device_${i}.txt
done
