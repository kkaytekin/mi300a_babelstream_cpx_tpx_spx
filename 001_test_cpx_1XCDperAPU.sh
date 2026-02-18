#!/bin/bash
OUTDIR=/zhome/academic/HLRS/hlrs/hpckkuec/cpx_tpx_test/logs/001
mkdir -p $OUTDIR

for i in 0 6 12 18; do
  # Run for roughle 1 minutes
  HIP_VISIBLE_DEVICES=$i /lustre/hpe/ws13/ws13.a/ws/hpckkuec-babelstream/BabelStream/build/hip-stream --arraysize 536870912 --numtimes 600 > $OUTDIR/device_${i}.txt 2>&1 &
done
wait

echo "=== Summary ==="
for i in 0 6 12 18; do
  echo "--- Device $i ---"
  grep -E "^(Copy|Mul|Add|Triad|Dot)" $OUTDIR/device_${i}.txt
done
