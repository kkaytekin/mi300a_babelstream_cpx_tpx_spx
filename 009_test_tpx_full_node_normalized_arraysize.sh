#!/bin/bash
OUTDIR=/zhome/academic/HLRS/hlrs/hpckkuec/cpx_tpx_test/logs/009_tpx
mkdir -p $OUTDIR

for i in $(seq 0 11); do
  # Run for roughle 1 minutes
  # Array size: 2 * 2^28 elements
  HIP_VISIBLE_DEVICES=$i /lustre/hpe/ws13/ws13.a/ws/hpckkuec-babelstream/BabelStream/build/hip-stream \
    --arraysize 536870912 \
    --numtimes 600 \
    > $OUTDIR/device_${i}.txt \
    2>&1 \
    &
done
wait

echo "=== Summary ==="
for i in $(seq 0 11); do
  echo "--- Device $i ---"
  grep -E "^(Copy|Mul|Add|Triad|Dot)" $OUTDIR/device_${i}.txt
done
