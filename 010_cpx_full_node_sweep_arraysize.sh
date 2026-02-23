#!/bin/bash
OUTDIR=/zhome/academic/HLRS/hlrs/hpckkuec/cpx_tpx_test/logs/010_cpx
BABELSTREAM=/lustre/hpe/ws13/ws13.a/ws/hpckkuec-babelstream/BabelStream/build/hip-stream
NUMTIMES=1500

# Sweep bounds (powers of two)
# Small sizes probe cache hierarchy; large sizes (2^28) are in the HBM-saturated regime
EXP_MIN=10
EXP_MAX=28

mkdir -p $OUTDIR

for exp in $(seq $EXP_MIN $EXP_MAX); do
  arraysize=$((2 ** exp))
  size_kib=$(( arraysize * 8 / 1024 ))
  expdir=$OUTDIR/exp${exp}_s${arraysize}
  mkdir -p $expdir

  echo "=== Array size: 2^${exp} = ${arraysize} elements (${size_kib} KiB per array) ==="

  for i in $(seq 0 23); do
    HIP_VISIBLE_DEVICES=$i $BABELSTREAM \
      --arraysize $arraysize \
      --numtimes $NUMTIMES \
      > $expdir/device_${i}.txt \
      2>&1 \
      &
  done
  wait
  echo "    done."
done

# Generate summary CSV
SUMMARY_CSV=$OUTDIR/summary.csv
echo "exp,arraysize_elements,arraysize_KiB,device,Copy_MBs,Mul_MBs,Add_MBs,Triad_MBs,Dot_MBs" > $SUMMARY_CSV

for exp in $(seq $EXP_MIN $EXP_MAX); do
  arraysize=$((2 ** exp))
  size_kib=$(( arraysize * 8 / 1024 ))
  for i in $(seq 0 23); do
    f=$OUTDIR/exp${exp}_s${arraysize}/device_${i}.txt
    copy=$(grep  "^Copy"  $f | awk '{print $2}')
    mul=$(grep   "^Mul"   $f | awk '{print $2}')
    add=$(grep   "^Add"   $f | awk '{print $2}')
    triad=$(grep "^Triad" $f | awk '{print $2}')
    dot=$(grep   "^Dot"   $f | awk '{print $2}')
    echo "$exp,$arraysize,$size_kib,$i,$copy,$mul,$add,$triad,$dot" >> $SUMMARY_CSV
  done
done

echo ""
echo "=== Summary (Triad bandwidth per device per array size) ==="
echo "CSV written to: $SUMMARY_CSV"
echo ""
printf "%-6s %-12s" "exp" "size(KiB)"
for i in $(seq 0 23); do printf " dev%-2s" $i; done
echo ""

for exp in $(seq $EXP_MIN $EXP_MAX); do
  arraysize=$((2 ** exp))
  size_kib=$(( arraysize * 8 / 1024 ))
  printf "%-6s %-12s" "2^$exp" "$size_kib"
  for i in $(seq 0 23); do
    triad=$(grep "^Triad" $OUTDIR/exp${exp}_s${arraysize}/device_${i}.txt | awk '{printf "%5.0f", $2}')
    printf " %5s" "$triad"
  done
  echo ""
done
