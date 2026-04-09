import matplotlib.pyplot as plt
import numpy as np

ops = ['Copy', 'Mul', 'Add', 'Triad', 'Dot']

# None = SIGKILL
run1 = {
    0:  [661117.948, 640557.230, 654860.947, 650132.270, 438943.653],
    1:  [710542.806, 710920.340, 715026.616, 715062.766, 644629.326],
    2:  [675881.485, 674612.330, 701742.622, 714396.708, 600493.414],
    3:  None,
    4:  [673778.913, 674544.521, 671426.137, 692474.005, 543957.523],
    5:  [710995.071, 711366.606, 715148.492, 715137.775, 664225.119],
    6:  [711040.977, 711312.353, 714922.314, 714851.316, 627635.245],
    7:  [711503.306, 711625.851, 715331.125, 715305.312, 679620.963],
    8:  [686060.791, 699817.288, 707540.578, 693300.060, 579137.566],
    9:  [686112.302, 700422.213, 707845.664, 690595.999, 577822.337],
    10: [686212.057, 701475.174, 708334.841, 697292.153, 583953.356],
    11: [711520.987, 711673.017, 715329.100, 715317.623, 701750.246],
    12: [711088.066, 711254.693, 714900.498, 715003.206, 658873.031],
    13: [711517.981, 711672.486, 715333.508, 715327.948, 686089.833],
    14: [710806.803, 711142.815, 714777.953, 714871.940, 655862.134],
    15: None, 16: None, 17: None,
    18: [711510.378, 711670.717, 715350.585, 715346.971, 702337.788],
    19: [705915.766, 710263.148, 714151.966, 714548.444, 569192.546],
    20: [676729.231, 673342.655, 671297.057, 674470.159, 549025.899],
    21: [711156.297, 711291.208, 714843.384, 714990.906, 625144.431],
    22: [711525.702, 711636.521, 715327.511, 715328.305, 682903.891],
    23: [707798.032, 708268.416, 714282.651, 714480.650, 626901.900],
}
run2 = {
    0:  [710791.393, 710726.642, 714499.945, 714579.988, 642513.408],
    1:  None,
    2:  [710697.300, 712294.900, 714604.559, 714804.005, 633539.964],
    3:  [710843.095, 711208.053, 715038.441, 715075.742, 650280.281],
    4:  None,
    5:  [711040.859, 711368.786, 715146.785, 715142.816, 663239.819],
    6:  [675910.097, 676139.401, 679240.230, 678881.242, 606127.622],
    7:  [710506.250, 712408.382, 705193.757, 713378.458, 564509.175],
    8:  [711514.327, 711714.823, 715349.274, 715358.766, 677564.997],
    9:  [711341.158, 711588.063, 715267.431, 715254.328, 702272.215],
    10: [711124.976, 711425.935, 715005.864, 714896.016, 632151.514],
    11: [711579.162, 711692.416, 715357.575, 715363.572, 703595.811],
    12: None,
    13: [710987.303, 711322.838, 715127.296, 715139.601, 662195.765],
    14: [710948.407, 711294.035, 715066.218, 715090.783, 649433.680],
    15: [710947.289, 711232.785, 714910.692, 714882.530, 658491.542],
    16: None,
    17: [711219.771, 711328.787, 714978.925, 715036.020, 656642.706],
    18: [711561.538, 711703.561, 715362.738, 715370.324, 703814.935],
    19: [711561.479, 711678.795, 715313.890, 715358.806, 687825.200],
    20: [710721.409, 711359.949, 714923.782, 714646.572, 622145.161],
    21: [710967.296, 711195.040, 715112.611, 715110.627, 678706.913],
    22: [675895.737, 707197.131, 714399.718, 714995.945, 605889.915],
    23: [711306.345, 711573.857, 715243.251, 715288.079, 702157.405],
}
run3 = {
    0:  [710954.938, 711345.222, 715118.207, 715119.755, 644523.738],
    1:  [711085.594, 711444.790, 715190.052, 715206.686, 692289.352],
    2:  None,
    3:  [623072.077, 610237.735, 663080.766, 663280.447, 400046.525],
    4:  [711127.979, 711419.453, 715212.284, 715334.540, 692143.761],
    5:  None,
    6:  [711478.378, 711623.375, 715346.097, 715331.006, 704589.099],
    7:  [711294.035, 711502.599, 715219.033, 715268.265, 690496.334],
    8:  [710637.270, 710819.625, 714497.171, 714707.261, 604508.839],
    9:  [711321.719, 711399.421, 715229.712, 715211.847, 690687.880],
    10: [711497.236, 711615.180, 715312.738, 715305.193, 687305.176],
    11: [711107.904, 711262.172, 714897.602, 714869.402, 637408.096],
    12: [674543.886, 673799.895, 672506.789, 672919.120, 589338.301],
    13: [711527.882, 711662.286, 715342.483, 715351.657, 687129.792],
    14: [710614.401, 711041.448, 714719.155, 714775.019, 604499.055],
    15: None,
    16: [711526.763, 711695.895, 715392.963, 715375.090, 703761.309],
    17: [674484.035, 675236.916, 677643.393, 681794.987, 590515.276],
    18: [711534.366, 711686.520, 715352.849, 715375.447, 702926.775],
    19: [711498.415, 711627.560, 715328.583, 715341.728, 676491.375],
    20: [711260.994, 711460.759, 715195.173, 715160.281, 675204.539],
    21: None,
    22: [673635.086, 674289.672, 673147.982, 675443.810, 555881.575],
    23: [674352.718, 682499.010, 712006.229, 711425.974, 565496.225],
}
all_runs = [run1, run2, run3]

# Healthy = survived all 3 runs (no SIGKILL in any run)
device_survived = {}
device_avg = {}
for d in range(24):
    valid = [r[d] for r in all_runs if r[d] is not None]
    device_survived[d] = len(valid)
    if len(valid) == 0:
        device_avg[d] = None
    else:
        device_avg[d] = [np.mean([v[j] for v in valid]) for j in range(5)]

fully_healthy = {d: (device_survived[d] == 3) for d in range(24)}

# APU mapping (user corrected)
apu_map = {0: list(range(0,6)), 1: list(range(6,12)), 2: list(range(12,18)), 3: list(range(18,24))}
apu_labels = ['APU 0', 'APU 1', 'APU 2', 'APU 3']
apu_colors = ['#2196F3', '#FF9800', '#E91E63', '#4CAF50']

THEORETICAL_BW_TB = 5.3
single_baseline = np.array([702162.857, 702227.147, 708953.866, 708922.661, 691820.779])

# Build cumulative per APU from fully healthy devices only
apu_cumulative = {}
apu_healthy_count = {}
for a in range(4):
    healthy_devs = [d for d in apu_map[a] if fully_healthy[d]]
    apu_healthy_count[a] = len(healthy_devs)
    cum = np.zeros((len(healthy_devs), 5))
    for i, dev_id in enumerate(healthy_devs):
        vals = np.array(device_avg[dev_id])
        cum[i] = (cum[i-1] if i > 0 else np.zeros(5)) + vals
    apu_cumulative[a] = cum / 1e6

ideal_per_apu = np.array([single_baseline * (i+1) / 1e6 for i in range(6)])

# ── Plot ──
fig, axes = plt.subplots(2, 3, figsize=(18, 11))
axes_flat = axes.flatten()

for j, op in enumerate(ops):
    ax = axes_flat[j]

    ax.axhline(THEORETICAL_BW_TB, color='red', linestyle=':', linewidth=1.5, alpha=0.6, zorder=1)
    ax.text(0.7, THEORETICAL_BW_TB + 0.05, 'Theoretical peak: 5.3 TB/s',
            fontsize=8, color='red', alpha=0.7, va='bottom')

    ax.fill_between(range(1, 7), 0, ideal_per_apu[:, j], alpha=0.05, color='black')
    ax.plot(range(1, 7), ideal_per_apu[:, j], 'k--', alpha=0.35, linewidth=1.5, label='Ideal (linear)')

    for a in range(4):
        cum = apu_cumulative[a]
        n_h = apu_healthy_count[a]
        if n_h == 0:
            continue
        xcds = np.arange(1, n_h + 1)
        ax.plot(xcds, cum[:, j], '-o', color=apu_colors[a], markersize=5,
                linewidth=2.2, label=f'{apu_labels[a]} ({n_h}/6)')
        ax.annotate(f'{cum[-1, j]:.2f}', xy=(n_h, cum[-1, j]),
                    xytext=(6, 0), textcoords='offset points',
                    fontsize=8.5, color=apu_colors[a], fontweight='bold', va='center')

    ax.set_title(op, fontsize=14, fontweight='bold')
    ax.set_xlabel('XCDs (cumulative, 3/3 survived)', fontsize=10)
    ax.set_ylabel('Bandwidth (TB/s)', fontsize=10)
    ax.set_xticks(range(1, 7))
    ax.set_xlim(0.5, 7.5)
    ax.set_ylim(0, THEORETICAL_BW_TB * 1.15)
    ax.grid(alpha=0.2)
    ax.set_axisbelow(True)
    if j == 0:
        ax.legend(fontsize=8.5, loc='upper left')

# ── Summary: Triad bars ──
ax = axes_flat[5]
triad_idx = ops.index('Triad')
apu_totals = [apu_cumulative[a][-1, triad_idx] if apu_healthy_count[a] > 0 else 0 for a in range(4)]
ideal_6xcd = ideal_per_apu[-1, triad_idx]
apu_ideal = [ideal_per_apu[max(apu_healthy_count[a]-1, 0), triad_idx] for a in range(4)]

bars = ax.bar(apu_labels, apu_totals, color=apu_colors, edgecolor='white',
              linewidth=0.8, width=0.55, zorder=3)
ax.axhline(ideal_6xcd, color='black', linestyle='--', alpha=0.4, linewidth=1.2,
           label=f'Ideal 6×XCD: {ideal_6xcd:.2f} TB/s')
ax.axhline(THEORETICAL_BW_TB, color='red', linestyle=':', linewidth=1.5, alpha=0.6,
           label=f'Theoretical peak: {THEORETICAL_BW_TB} TB/s')

for bar, val, n_h, ideal_n in zip(bars, apu_totals,
                                    [apu_healthy_count[a] for a in range(4)],
                                    apu_ideal):
    if n_h == 0:
        continue
    eff_ideal = val / ideal_n * 100
    eff_theo = val / THEORETICAL_BW_TB * 100
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.06,
            f'{val:.2f} TB/s\n{n_h}/6 XCDs\n({eff_ideal:.0f}% ideal · {eff_theo:.0f}% peak)',
            ha='center', va='bottom', fontsize=8.5, fontweight='bold')

ax.set_title('Triad: Aggregate per APU (fully healthy)', fontsize=14, fontweight='bold')
ax.set_ylabel('Bandwidth (TB/s)', fontsize=10)
ax.set_ylim(0, THEORETICAL_BW_TB * 1.45)
ax.legend(fontsize=8.5, loc='upper right')
ax.grid(axis='y', alpha=0.2)
ax.set_axisbelow(True)

# MCLK table — bottom right of summary panel
mclk_notes = ['1300 MHz (both runs)', '900 MHz (both runs)', '900–1100 MHz (varies)', '900–1300 MHz (varies)']
table_text = (
    "Idle MCLK (rocm-smi, pre-load DVFS):\n"
    "───────────────────────────────────\n"
    f" APU 0:  {mclk_notes[0]:<26s}\n"
    f" APU 1:  {mclk_notes[1]:<26s}\n"
    f" APU 2:  {mclk_notes[2]:<26s}\n"
    f" APU 3:  {mclk_notes[3]:<26s}\n"
    "───────────────────────────────────\n"
    "MCLK varies at idle; BW consistent\n"
    "→ DVFS ramps clocks under load"
)
ax.text(0.98, 0.03, table_text, transform=ax.transAxes, fontsize=7.5,
        va='bottom', ha='right', family='monospace',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#f5f5f5', edgecolor='#cccccc', alpha=0.95))

# OOM note at bottom of figure
fig.text(0.5, 0.005,
         '⚠ ~4 of 24 procs SIGKILL\'d per run (OOM: arraysize=536M → 12 GB/proc × 24 = 288 GB exceeds node HBM). '
         'Only devices surviving all 3 runs shown. APU 1: 6/6, APU 3: 5/6, APU 2: 2/6, APU 0: 1/6.',
         ha='center', fontsize=8.5, style='italic', color='#666666',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff3e0', edgecolor='#ffcc80', alpha=0.9))

fig.suptitle('MI300A CPX: Per-APU Cumulative BabelStream Bandwidth (fully healthy devices)\n'
             'numtimes=600 · arraysize=536M · 3 runs · "healthy" = survived all 3 runs without SIGKILL',
             fontsize=14, fontweight='bold')
plt.tight_layout(rect=[0, 0.035, 1, 0.93])
plt.savefig('/home/claude/cpx_per_apu_v5.png', dpi=150, bbox_inches='tight')
print("Saved.")