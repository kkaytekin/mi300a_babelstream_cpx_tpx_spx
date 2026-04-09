# Experiment `000_test_cpx_full_node.sh` Key findings:

**OOM**: Consistently 4 devices get killed per run, but it's random which ones — the 24 × 12 GB (total size per instance) = 288 GB is bumping against the node's combined HBM. You'd want to drop `--arraysize` to ~400M to avoid this.

**Healthy devices are very consistent**: Triad averages 711.4 GB/s per device with only ±5 GB/s std. When a device survives the OOM lottery, it performs at essentially full bandwidth — meaning there's **no measurable contention** between XCDs in CPX mode with the larger array size and longer runtime.

**Per-APU**: The APUs with all 6 devices surviving (APU 1 and 3) show 4.26 TB/s aggregate each, which is almost exactly 6 × 711 GB/s = perfect linear scaling within an APU.

**vs previous short runs**: The earlier 100-iteration results showed ~580–670 GB/s average with high variance. The 600-iteration runs converge to ~711 GB/s — the short runs were dominated by warmup/startup noise. The "contention" we saw before was largely an artifact of short measurement windows.



```
s34623 x1001c2s0b0n0 202$ sh 000_test_cpx_full_node.sh 
000_test_cpx_full_node.sh: line 9: 1677395 Killed                  HIP_VISIBLE_DEVICES=$i /lustre/hpe/ws13/ws13.a/ws/hpckkuec-babelstream/BabelStream/build/hip-stream --arraysize 536870912 --numtimes 600 > $OUTDIR/device_${i}.txt 2>&1
000_test_cpx_full_node.sh: line 9: 1677407 Killed                  HIP_VISIBLE_DEVICES=$i /lustre/hpe/ws13/ws13.a/ws/hpckkuec-babelstream/BabelStream/build/hip-stream --arraysize 536870912 --numtimes 600 > $OUTDIR/device_${i}.txt 2>&1
000_test_cpx_full_node.sh: line 9: 1677408 Killed                  HIP_VISIBLE_DEVICES=$i /lustre/hpe/ws13/ws13.a/ws/hpckkuec-babelstream/BabelStream/build/hip-stream --arraysize 536870912 --numtimes 600 > $OUTDIR/device_${i}.txt 2>&1
000_test_cpx_full_node.sh: line 9: 1677409 Killed                  HIP_VISIBLE_DEVICES=$i /lustre/hpe/ws13/ws13.a/ws/hpckkuec-babelstream/BabelStream/build/hip-stream --arraysize 536870912 --numtimes 600 > $OUTDIR/device_${i}.txt 2>&1
=== Summary ===
--- Device 0 ---
Copy        661117.948     
Mul         640557.230     
Add         654860.947     
Triad       650132.270     
Dot         438943.653     
--- Device 1 ---
Copy        710542.806     
Mul         710920.340     
Add         715026.616     
Triad       715062.766     
Dot         644629.326     
--- Device 2 ---
Copy        675881.485     
Mul         674612.330     
Add         701742.622     
Triad       714396.708     
Dot         600493.414     
--- Device 3 ---
--- Device 4 ---
Copy        673778.913     
Mul         674544.521     
Add         671426.137     
Triad       692474.005     
Dot         543957.523     
--- Device 5 ---
Copy        710995.071     
Mul         711366.606     
Add         715148.492     
Triad       715137.775     
Dot         664225.119     
--- Device 6 ---
Copy        711040.977     
Mul         711312.353     
Add         714922.314     
Triad       714851.316     
Dot         627635.245     
--- Device 7 ---
Copy        711503.306     
Mul         711625.851     
Add         715331.125     
Triad       715305.312     
Dot         679620.963     
--- Device 8 ---
Copy        686060.791     
Mul         699817.288     
Add         707540.578     
Triad       693300.060     
Dot         579137.566     
--- Device 9 ---
Copy        686112.302     
Mul         700422.213     
Add         707845.664     
Triad       690595.999     
Dot         577822.337     
--- Device 10 ---
Copy        686212.057     
Mul         701475.174     
Add         708334.841     
Triad       697292.153     
Dot         583953.356     
--- Device 11 ---
Copy        711520.987     
Mul         711673.017     
Add         715329.100     
Triad       715317.623     
Dot         701750.246     
--- Device 12 ---
Copy        711088.066     
Mul         711254.693     
Add         714900.498     
Triad       715003.206     
Dot         658873.031     
--- Device 13 ---
Copy        711517.981     
Mul         711672.486     
Add         715333.508     
Triad       715327.948     
Dot         686089.833     
--- Device 14 ---
Copy        710806.803     
Mul         711142.815     
Add         714777.953     
Triad       714871.940     
Dot         655862.134     
--- Device 15 ---
--- Device 16 ---
--- Device 17 ---
--- Device 18 ---
Copy        711510.378     
Mul         711670.717     
Add         715350.585     
Triad       715346.971     
Dot         702337.788     
--- Device 19 ---
Copy        705915.766     
Mul         710263.148     
Add         714151.966     
Triad       714548.444     
Dot         569192.546     
--- Device 20 ---
Copy        676729.231     
Mul         673342.655     
Add         671297.057     
Triad       674470.159     
Dot         549025.899     
--- Device 21 ---
Copy        711156.297
Mul         711291.208     
Add         714843.384     
Triad       714990.906     
Dot         625144.431     
--- Device 22 ---
Copy        711525.702     
Mul         711636.521     
Add         715327.511     
Triad       715328.305     
Dot         682903.891     
--- Device 23 ---
Copy        707798.032     
Mul         708268.416     
Add         714282.651     
Triad       714480.650     
Dot         626901.900     
s34623 x1001c2s0b0n0 208$ ./000_test_cpx_full_node.sh 
./000_test_cpx_full_node.sh: line 9: 1750320 Killed                  HIP_VISIBLE_DEVICES=$i /lustre/hpe/ws13/ws13.a/ws/hpckkuec-babelstream/BabelStream/build/hip-stream --arraysize 536870912 --numtimes 600 > $OUTDIR/device_${i}.txt 2>&1
./000_test_cpx_full_node.sh: line 9: 1750324 Killed                  HIP_VISIBLE_DEVICES=$i /lustre/hpe/ws13/ws13.a/ws/hpckkuec-babelstream/BabelStream/build/hip-stream --arraysize 536870912 --numtimes 600 > $OUTDIR/device_${i}.txt 2>&1
./000_test_cpx_full_node.sh: line 9: 1750333 Killed                  HIP_VISIBLE_DEVICES=$i /lustre/hpe/ws13/ws13.a/ws/hpckkuec-babelstream/BabelStream/build/hip-stream --arraysize 536870912 --numtimes 600 > $OUTDIR/device_${i}.txt 2>&1
./000_test_cpx_full_node.sh: line 9: 1750337 Killed                  HIP_VISIBLE_DEVICES=$i /lustre/hpe/ws13/ws13.a/ws/hpckkuec-babelstream/BabelStream/build/hip-stream --arraysize 536870912 --numtimes 600 > $OUTDIR/device_${i}.txt 2>&1
=== Summary ===
--- Device 0 ---
Copy        710791.393     
Mul         710726.642     
Add         714499.945     
Triad       714579.988     
Dot         642513.408     
--- Device 1 ---
--- Device 2 ---
Copy        710697.300     
Mul         712294.900     
Add         714604.559     
Triad       714804.005     
Dot         633539.964     
--- Device 3 ---
Copy        710843.095     
Mul         711208.053     
Add         715038.441     
Triad       715075.742     
Dot         650280.281     
--- Device 4 ---
--- Device 5 ---
Copy        711040.859     
Mul         711368.786     
Add         715146.785     
Triad       715142.816     
Dot         663239.819     
--- Device 6 ---
Copy        675910.097     
Mul         676139.401     
Add         679240.230     
Triad       678881.242     
Dot         606127.622     
--- Device 7 ---
Copy        710506.250     
Mul         712408.382     
Add         705193.757     
Triad       713378.458     
Dot         564509.175     
--- Device 8 ---
Copy        711514.327     
Mul         711714.823     
Add         715349.274     
Triad       715358.766     
Dot         677564.997     
--- Device 9 ---
Copy        711341.158     
Mul         711588.063     
Add         715267.431     
Triad       715254.328     
Dot         702272.215     
--- Device 10 ---
Copy        711124.976     
Mul         711425.935     
Add         715005.864     
Triad       714896.016     
Dot         632151.514     
--- Device 11 ---
Copy        711579.162     
Mul         711692.416     
Add         715357.575     
Triad       715363.572     
Dot         703595.811     
--- Device 12 ---
--- Device 13 ---
Copy        710987.303     
Mul         711322.838     
Add         715127.296     
Triad       715139.601     
Dot         662195.765     
--- Device 14 ---
Copy        710948.407     
Mul         711294.035     
Add         715066.218     
Triad       715090.783     
Dot         649433.680     
--- Device 15 ---
Copy        710947.289     
Mul         711232.785     
Add         714910.692     
Triad       714882.530     
Dot         658491.542     
--- Device 16 ---
--- Device 17 ---
Copy        711219.771     
Mul         711328.787     
Add         714978.925     
Triad       715036.020     
Dot         656642.706     
--- Device 18 ---
Copy        711561.538     
Mul         711703.561     
Add         715362.738     
Triad       715370.324     
Dot         703814.935     
--- Device 19 ---
Copy        711561.479     
Mul         711678.795     
Add         715313.890     
Triad       715358.806     
Dot         687825.200     
--- Device 20 ---
Copy        710721.409     
Mul         711359.949     
Add         714923.782     
Triad       714646.572     
Dot         622145.161     
--- Device 21 ---
Copy        710967.296     
Mul         711195.040     
Add         715112.611     
Triad       715110.627     
Dot         678706.913     
--- Device 22 ---
Copy        675895.737     
Mul         707197.131     
Add         714399.718     
Triad       714995.945     
Dot         605889.915     
--- Device 23 ---
Copy        711306.345     
Mul         711573.857     
Add         715243.251     
Triad       715288.079     
Dot         702157.405     
s34623 x1001c2s0b0n0 209$ ./000_test_cpx_full_node.sh 
./000_test_cpx_full_node.sh: line 9: 1789755 Killed                  HIP_VISIBLE_DEVICES=$i /lustre/hpe/ws13/ws13.a/ws/hpckkuec-babelstream/BabelStream/build/hip-stream --arraysize 536870912 --numtimes 600 > $OUTDIR/device_${i}.txt 2>&1
./000_test_cpx_full_node.sh: line 9: 1789759 Killed                  HIP_VISIBLE_DEVICES=$i /lustre/hpe/ws13/ws13.a/ws/hpckkuec-babelstream/BabelStream/build/hip-stream --arraysize 536870912 --numtimes 600 > $OUTDIR/device_${i}.txt 2>&1
./000_test_cpx_full_node.sh: line 9: 1789774 Killed                  HIP_VISIBLE_DEVICES=$i /lustre/hpe/ws13/ws13.a/ws/hpckkuec-babelstream/BabelStream/build/hip-stream --arraysize 536870912 --numtimes 600 > $OUTDIR/device_${i}.txt 2>&1
./000_test_cpx_full_node.sh: line 9: 1789780 Killed                  HIP_VISIBLE_DEVICES=$i /lustre/hpe/ws13/ws13.a/ws/hpckkuec-babelstream/BabelStream/build/hip-stream --arraysize 536870912 --numtimes 600 > $OUTDIR/device_${i}.txt 2>&1
=== Summary ===
--- Device 0 ---
Copy        710954.938     
Mul         711345.222     
Add         715118.207     
Triad       715119.755     
Dot         644523.738     
--- Device 1 ---
Copy        711085.594     
Mul         711444.790     
Add         715190.052     
Triad       715206.686     
Dot         692289.352     
--- Device 2 ---
--- Device 3 ---
Copy        623072.077     
Mul         610237.735     
Add         663080.766     
Triad       663280.447     
Dot         400046.525     
--- Device 4 ---
Copy        711127.979     
Mul         711419.453     
Add         715212.284     
Triad       715334.540     
Dot         692143.761     
--- Device 5 ---
--- Device 6 ---
Copy        711478.378     
Mul         711623.375     
Add         715346.097     
Triad       715331.006     
Dot         704589.099     
--- Device 7 ---
Copy        711294.035     
Mul         711502.599     
Add         715219.033     
Triad       715268.265     
Dot         690496.334     
--- Device 8 ---
Copy        710637.270     
Mul         710819.625     
Add         714497.171     
Triad       714707.261     
Dot         604508.839     
--- Device 9 ---
Copy        711321.719     
Mul         711399.421     
Add         715229.712     
Triad       715211.847     
Dot         690687.880     
--- Device 10 ---
Copy        711497.236     
Mul         711615.180     
Add         715312.738     
Triad       715305.193     
Dot         687305.176     
--- Device 11 ---
Copy        711107.904     
Mul         711262.172     
Add         714897.602     
Triad       714869.402     
Dot         637408.096     
--- Device 12 ---
Copy        674543.886     
Mul         673799.895     
Add         672506.789     
Triad       672919.120     
Dot         589338.301     
--- Device 13 ---
Copy        711527.882     
Mul         711662.286     
Add         715342.483     
Triad       715351.657     
Dot         687129.792     
--- Device 14 ---
Copy        710614.401     
Mul         711041.448     
Add         714719.155     
Triad       714775.019     
Dot         604499.055     
--- Device 15 ---
--- Device 16 ---
Copy        711526.763     
Mul         711695.895     
Add         715392.963     
Triad       715375.090     
Dot         703761.309     
--- Device 17 ---
Copy        674484.035     
Mul         675236.916     
Add         677643.393     
Triad       681794.987     
Dot         590515.276     
--- Device 18 ---
Copy        711534.366     
Mul         711686.520     
Add         715352.849     
Triad       715375.447     
Dot         702926.775     
--- Device 19 ---
Copy        711498.415     
Mul         711627.560     
Add         715328.583     
Triad       715341.728     
Dot         676491.375     
--- Device 20 ---
Copy        711260.994     
Mul         711460.759     
Add         715195.173     
Triad       715160.281     
Dot         675204.539     
--- Device 21 ---
--- Device 22 ---
Copy        673635.086     
Mul         674289.672     
Add         673147.982     
Triad       675443.810     
Dot         555881.575     
--- Device 23 ---
Copy        674352.718     
Mul         682499.010     
Add         712006.229     
Triad       711425.974     
Dot         565496.225    
```