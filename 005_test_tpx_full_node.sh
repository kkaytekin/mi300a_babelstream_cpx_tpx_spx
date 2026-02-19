#!/bin/bash
OUTDIR=/zhome/academic/HLRS/hlrs/hpckkuec/cpx_tpx_test/logs/005
mkdir -p $OUTDIR

for i in $(seq 0 11); do
  # Run for roughle 1 minutes
  # Same array size as in CPX case. Not sure if I should double it.
  HIP_VISIBLE_DEVICES=$i /lustre/hpe/ws13/ws13.a/ws/hpckkuec-babelstream/BabelStream/build/hip-stream \
    --arraysize 268435456 \
    --numtimes 1500 \
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
