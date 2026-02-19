import matplotlib.pyplot as plt
import numpy as np

ops = ['Copy', 'Mul', 'Add', 'Triad', 'Dot']

data = {
    0:  [710817.214, 711125.565, 714968.570, 714961.429, 703602.208],
    1:  [710843.095, 711110.259, 714983.646, 715000.310, 683653.334],
    2:  [710463.293, 710605.524, 714436.557, 714688.590, 612286.378],
    3:  [710919.575, 710979.712, 714523.718, 714463.496, 699919.300],
    4:  [673548.566, 673228.666, 672681.423, 671262.119, 532222.415],
    5:  [674350.177, 674151.182, 672083.464, 671867.586, 534642.589],
    6:  [710939.581, 711140.989, 715053.480, 715058.242, 703101.166],
    7:  [710747.813, 711009.019, 714902.719, 714918.586, 703098.864],
    8:  [710016.985, 710402.186, 714568.020, 714375.557, 635575.182],
    9:  [710399.953, 710469.169, 714430.219, 714059.633, 624244.095],
    10: [628094.768, 634043.836, 641712.192, 622142.727, 385494.256],
    11: [710899.689, 711013.727, 714890.820, 714911.446, 686938.017],
    12: [709758.970, 710361.062, 714380.310, 714432.596, 655398.302],
    13: [674251.723, 674645.604, 685856.050, 671899.118, 571742.943],
    14: [709838.619, 710980.771, 713201.163, 706637.047, 530319.936],
    15: [709890.242, 705287.942, 711129.921, 712596.889, 536786.167],
    16: [709648.617, 710285.877, 714232.209, 714147.494, 639430.058],
    17: [710745.460, 710932.520, 714634.681, 714362.883, 700498.066],
    18: [645140.097, 638156.949, 644440.295, 638095.702, 395035.638],
    19: [709891.416, 710339.915, 714481.720, 714402.491, 655839.651],
    20: [709500.908, 710413.936, 714129.286, 714195.787, 616602.290],
    21: [628617.843, 603552.951, 672060.327, 689864.599, 541727.294],
    22: [710682.071, 710946.642, 714716.340, 714829.742, 679078.852],
    23: [710857.214, 711049.041, 714989.200, 715001.897, 697371.368],
}

apu_map = {0: list(range(0,6)), 1: list(range(6,12)), 2: list(range(12,18)), 3: list(range(18,24))}
apu_labels = ['APU 0', 'APU 1', 'APU 2', 'APU 3']
apu_colors = ['#2196F3', '#FF9800', '#E91E63', '#4CAF50']

THEORETICAL_BW_TB = 5.3
MB_TO_TB = 1e6
TB_TO_TIB = 1e12 / (2**40)  # 1 TB = 1e12 / 2^40 TiB ≈ 0.9095

top_devs = [0, 1, 3, 6, 7, 11, 17, 22, 23]
single_baseline = np.mean([data[d] for d in top_devs], axis=0)

apu_cumulative = {}
for a in range(4):
    devs = apu_map[a]
    cum = np.zeros((6, 5))
    for i, dev_id in enumerate(devs):
        vals = np.array(data[dev_id])
        cum[i] = (cum[i-1] if i > 0 else np.zeros(5)) + vals
    apu_cumulative[a] = cum / MB_TO_TB

ideal_per_apu = np.array([single_baseline * (i+1) / MB_TO_TB for i in range(6)])

def add_tib_axis(ax):
    ax2 = ax.twinx()
    ymin, ymax = ax.get_ylim()
    ax2.set_ylim(ymin * TB_TO_TIB, ymax * TB_TO_TIB)
    ax2.set_ylabel('TiB/s', fontsize=10)
    return ax2

# ── Plot ──
fig, axes = plt.subplots(2, 3, figsize=(18, 11))
axes_flat = axes.flatten()

for j, op in enumerate(ops):
    ax = axes_flat[j]

    ax.axhline(THEORETICAL_BW_TB, color='red', linestyle=':', linewidth=1.5, alpha=0.6, zorder=1)
    ax.text(0.7, THEORETICAL_BW_TB + 0.05, '5.3 TB/s peak',
            fontsize=8, color='red', alpha=0.7, va='bottom')

    ax.fill_between(range(1, 7), 0, ideal_per_apu[:, j], alpha=0.05, color='black')
    ax.plot(range(1, 7), ideal_per_apu[:, j], 'k--', alpha=0.35, linewidth=1.5, label='Ideal (linear)')

    for a in range(4):
        cum = apu_cumulative[a]
        xcds = np.arange(1, 7)
        ax.plot(xcds, cum[:, j], '-o', color=apu_colors[a], markersize=5,
                linewidth=2.2, label=f'{apu_labels[a]}')
        ax.annotate(f'{cum[-1, j]:.2f}', xy=(6, cum[-1, j]),
                    xytext=(6, 0), textcoords='offset points',
                    fontsize=8.5, color=apu_colors[a], fontweight='bold', va='center')

    ax.set_title(op, fontsize=14, fontweight='bold')
    ax.set_xlabel('XCDs (cumulative)', fontsize=10)
    ax.set_ylabel('TB/s', fontsize=10)
    ax.set_xticks(range(1, 7))
    ax.set_xlim(0.5, 7.5)
    ax.set_ylim(0, THEORETICAL_BW_TB * 1.15)
    ax.grid(alpha=0.2)
    ax.set_axisbelow(True)
    if j == 0:
        ax.legend(fontsize=8.5, loc='upper left')

    add_tib_axis(ax)

# ── Summary: Triad bars ──
ax = axes_flat[5]
triad_idx = ops.index('Triad')
apu_totals = [apu_cumulative[a][-1, triad_idx] for a in range(4)]
ideal_6xcd = ideal_per_apu[-1, triad_idx]

bars = ax.bar(apu_labels, apu_totals, color=apu_colors, edgecolor='white',
              linewidth=0.8, width=0.55, zorder=3)
ax.axhline(ideal_6xcd, color='black', linestyle='--', alpha=0.4, linewidth=1.2,
           label=f'Ideal 6×XCD: {ideal_6xcd:.2f} TB/s')
ax.axhline(THEORETICAL_BW_TB, color='red', linestyle=':', linewidth=1.5, alpha=0.6,
           label=f'Peak: {THEORETICAL_BW_TB} TB/s')

for bar, val in zip(bars, apu_totals):
    eff_ideal = val / ideal_6xcd * 100
    eff_theo = val / THEORETICAL_BW_TB * 100
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.06,
            f'{val:.2f} TB/s\n({eff_ideal:.0f}% ideal · {eff_theo:.0f}% peak)',
            ha='center', va='bottom', fontsize=8.5, fontweight='bold')

ax.set_title('Triad: Aggregate per APU', fontsize=14, fontweight='bold')
ax.set_ylabel('TB/s', fontsize=10)
ax.set_ylim(0, THEORETICAL_BW_TB * 1.35)
ax.legend(fontsize=8.5, loc='upper right')
ax.grid(axis='y', alpha=0.2)
ax.set_axisbelow(True)

ax2 = ax.twinx()
ymin, ymax = ax.get_ylim()
ax2.set_ylim(ymin * TB_TO_TIB, ymax * TB_TO_TIB)
ax2.set_ylabel('TiB/s', fontsize=10)

# ── Footer with all details (single source of truth) ──
fig.text(0.5, 0.005,
         'BabelStream on MI300A CPX · double-precision · arraysize=2²⁸ (268M elements) · '
         'numtimes=1500 · all 24 XCDs completed · "ideal" baseline = mean of top XCDs',
         ha='center', fontsize=9, style='italic', color='#555555',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0f0f0', edgecolor='#cccccc', alpha=0.9))

fig.suptitle('MI300A CPX — Per-APU Cumulative BabelStream HBM Bandwidth',
             fontsize=15, fontweight='bold')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('/home/claude/cpx_per_apu_v8.png', dpi=150, bbox_inches='tight')
print("Saved.")