import matplotlib.pyplot as plt
import numpy as np

ops = ['Copy', 'Mul', 'Add', 'Triad', 'Dot']

# 1 APU, 6 XCDs (devices 0-5, all on APU 0)
data = {
    0: [709765.890, 710496.318, 716850.031, 714322.488, 639342.393],
    1: [716799.863, 710613.754, 714506.284, 715018.640, 697597.792],
    2: [673513.605, 673454.464, 694839.259, 670292.598, 574235.328],
    3: [709858.681, 710592.592, 714289.304, 714589.499, 645398.842],
    4: [673180.021, 673353.105, 694448.289, 670210.315, 569768.188],
    5: [710952.526, 711112.613, 714961.508, 714955.954, 703043.620],
}

# Reference: 1-XCD isolated baseline (mean from previous 1-XCD-per-APU experiment)
baseline_1xcd = np.array([710919.819, 711137.930, 714967.461, 714965.925, 704574.931])

THEORETICAL_BW_TB = 5.3
TB_TO_TIB = 1e12 / (2**40)
MB_TO_TB = 1e6

devs = list(range(6))
dev_colors = plt.cm.viridis(np.linspace(0.15, 0.85, 6))

fig, axes = plt.subplots(1, 3, figsize=(18, 5.5), gridspec_kw={'width_ratios': [3, 2, 2]})

# ── Left: per-device bars ──
ax = axes[0]
x = np.arange(len(ops))
w = 0.13
for i, d in enumerate(devs):
    v = np.array(data[d]) / MB_TO_TB
    ax.bar(x + (i - 2.5) * w, v, w, color=dev_colors[i], edgecolor='white',
           linewidth=0.5, label=f'Dev {d}', zorder=3)

# baseline reference
for j in range(len(ops)):
    ax.hlines(baseline_1xcd[j] / MB_TO_TB, x[j] - 3*w, x[j] + 3*w,
              colors='red', linewidths=1.2, linestyles='--', alpha=0.6, zorder=4)

ax.hlines([], [], [], colors='red', linewidths=1.2, linestyles='--', alpha=0.6, label='1-XCD isolated baseline')

ax.set_xticks(x)
ax.set_xticklabels(ops, fontsize=12, fontweight='bold')
ax.set_ylabel('TB/s', fontsize=11)
ax.set_ylim(0.55, 0.73)
ax.grid(axis='y', alpha=0.2)
ax.set_axisbelow(True)
ax.legend(fontsize=8, ncol=4, loc='lower left')
ax.set_title('Per-XCD bandwidth', fontsize=13, fontweight='bold')

ax2 = ax.twinx()
ymin, ymax = ax.get_ylim()
ax2.set_ylim(ymin * TB_TO_TIB, ymax * TB_TO_TIB)
ax2.set_ylabel('TiB/s', fontsize=11)

# ── Middle: % of isolated baseline ──
ax = axes[1]
for i, d in enumerate(devs):
    pcts = np.array(data[d]) / baseline_1xcd * 100
    ax.plot(ops, pcts, '-o', color=dev_colors[i], markersize=6, linewidth=1.8, label=f'Dev {d}')

ax.axhline(100, color='red', linestyle='--', alpha=0.5, linewidth=1.2)
ax.set_ylabel('% of 1-XCD isolated baseline', fontsize=10)
ax.set_ylim(75, 105)
ax.grid(alpha=0.2)
ax.set_axisbelow(True)
ax.legend(fontsize=8, ncol=2, loc='lower left')
ax.set_title('Efficiency vs. isolated', fontsize=13, fontweight='bold')

# ── Right: cumulative bandwidth ──
ax = axes[2]
cum = np.zeros(5)
cum_vals = []
for d in devs:
    cum = cum + np.array(data[d])
    cum_vals.append(cum.copy())
cum_arr = np.array(cum_vals) / MB_TO_TB

ideal = np.array([baseline_1xcd * (i+1) / MB_TO_TB for i in range(6)])

# Just show Triad + Copy
for j, (op, ls) in enumerate([(3, '-'), (0, '--')]):  # Triad, Copy
    ax.plot(range(1, 7), cum_arr[:, op], f'{ls}o', color='#2196F3', markersize=5,
            linewidth=2.2, label=f'{ops[op]} (measured)', alpha=1.0 if j == 0 else 0.6)
    ax.plot(range(1, 7), ideal[:, op], f'{ls}', color='black', alpha=0.3, linewidth=1.5,
            label=f'{ops[op]} (ideal)' if j == 0 else f'{ops[op]} (ideal)')

ax.axhline(THEORETICAL_BW_TB, color='red', linestyle=':', linewidth=1.5, alpha=0.6)
ax.text(1.1, THEORETICAL_BW_TB + 0.05, '5.3 TB/s peak', fontsize=8, color='red', alpha=0.7)

ax.set_xlabel('XCDs (cumulative)', fontsize=10)
ax.set_ylabel('TB/s', fontsize=11)
ax.set_xticks(range(1, 7))
ax.set_xlim(0.5, 6.8)
ax.set_ylim(0, THEORETICAL_BW_TB * 1.1)
ax.grid(alpha=0.2)
ax.set_axisbelow(True)
ax.legend(fontsize=8, loc='upper left')
ax.set_title('Cumulative (APU 0)', fontsize=13, fontweight='bold')

# Annotate final values
for op, yoff in [(3, -8), (0, 8)]:
    ax.annotate(f'{cum_arr[-1, op]:.2f}', xy=(6, cum_arr[-1, op]),
                xytext=(6, yoff), textcoords='offset points',
                fontsize=9, fontweight='bold', color='#2196F3', va='center')

ax2 = ax.twinx()
ymin, ymax = ax.get_ylim()
ax2.set_ylim(ymin * TB_TO_TIB, ymax * TB_TO_TIB)
ax2.set_ylabel('TiB/s', fontsize=11)

fig.suptitle('MI300A CPX — BabelStream HBM Bandwidth: 6 XCDs on 1 APU (APU 0)',
             fontsize=14, fontweight='bold')
fig.text(0.5, 0.005,
         'BabelStream · double-precision · arraysize=2²⁸ · numtimes=1500 · '
         'devices 0–5 on APU 0 · red dashes = 1-XCD isolated baseline',
         ha='center', fontsize=9, style='italic', color='#555555',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0f0f0', edgecolor='#cccccc', alpha=0.9))

plt.tight_layout(rect=[0, 0.04, 1, 0.93])
plt.savefig('/home/claude/cpx_1apu_6xcd.png', dpi=150, bbox_inches='tight')
print("Saved.")