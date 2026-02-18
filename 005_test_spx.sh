#!/bin/bash
OUTDIR=/zhome/academic/HLRS/hlrs/hpckkuec/cpx_tpx_test/logs/005
mkdir -p $OUTDIR

for i in $(seq 0 3); do
  # Run for roughle 1 minutes
  # We were putting 536870912 per XPU in 000_CPX experiment. Now we should put 6 * 536870912 = 3221225472 per XPU, since we have 6 XPU in total.
  HIP_VISIBLE_DEVICES=$i /lustre/hpe/ws13/ws13.a/ws/hpckkuec-babelstream/BabelStream/build/hip-stream --arraysize 3221225472 --numtimes 600 > $OUTDIR/device_${i}.txt 2>&1 &
done
wait

echo "=== Summary ==="
for i in $(seq 0 3); do
  echo "--- Device $i ---"
  grep -E "^(Copy|Mul|Add|Triad|Dot)" $OUTDIR/device_${i}.txt
done
