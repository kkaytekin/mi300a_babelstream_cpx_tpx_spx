import matplotlib.pyplot as plt
import numpy as np

ops = ['Copy', 'Mul', 'Add', 'Triad', 'Dot']

# 2^28 (previous run)
data_28 = {
    0: [709765.890, 710496.318, 716850.031, 714322.488, 639342.393],
    1: [716799.863, 710613.754, 714506.284, 715018.640, 697597.792],
    2: [673513.605, 673454.464, 694839.259, 670292.598, 574235.328],
    3: [709858.681, 710592.592, 714289.304, 714589.499, 645398.842],
    4: [673180.021, 673353.105, 694448.289, 670210.315, 569768.188],
    5: [710952.526, 711112.613, 714961.508, 714955.954, 703043.620],
}

# 2^29 (new run)
data_29 = {
    0: [711481.973, 711693.006, 715338.948, 715311.547, 704627.881],
    1: [694792.462, 711184.500, 714944.410, 715032.488, 616991.234],
    2: [631440.352, 670036.891, 670734.478, 672723.568, 569147.592],
    3: [711541.556, 711625.202, 715350.069, 715359.997, 687049.058],
    4: [692079.966, 679557.304, 687436.232, 672092.754, 566944.894],
    5: [692020.866, 679941.909, 688540.120, 672246.690, 567257.514],
}

baseline_1xcd = np.array([710919.819, 711137.930, 714967.461, 714965.925, 704574.931])

MB_TO_TB = 1e6
TB_TO_TIB = 1e12 / (2**40)
THEORETICAL_BW_TB = 5.3

devs = list(range(6))

fig, axes = plt.subplots(2, 3, figsize=(18, 10))

# ── Row 1: per-device efficiency (% of isolated baseline) ──
for col, (label, dat) in enumerate([('2²⁸ (268M doubles)', data_28), ('2²⁹ (536M doubles)', data_29)]):
    ax = axes[0, col]
    colors = plt.cm.viridis(np.linspace(0.15, 0.85, 6))
    for i, d in enumerate(devs):
        pcts = np.array(dat[d]) / baseline_1xcd * 100
        ax.plot(ops, pcts, '-o', color=colors[i], markersize=6, linewidth=1.8, label=f'Dev {d}')
    ax.axhline(100, color='red', linestyle='--', alpha=0.5, linewidth=1.2)
    ax.set_ylabel('% of 1-XCD isolated baseline', fontsize=10)
    ax.set_ylim(75, 105)
    ax.grid(alpha=0.2)
    ax.set_axisbelow(True)
    ax.legend(fontsize=8, ncol=3, loc='lower left')
    ax.set_title(f'Efficiency — arraysize={label}', fontsize=12, fontweight='bold')

# ── Row 1, col 3: delta (2^29 − 2^28) per device ──
ax = axes[0, 2]
for i, d in enumerate(devs):
    pct_28 = np.array(data_28[d]) / baseline_1xcd * 100
    pct_29 = np.array(data_29[d]) / baseline_1xcd * 100
    delta = pct_29 - pct_28
    colors_d = plt.cm.viridis(np.linspace(0.15, 0.85, 6))
    ax.bar(np.arange(len(ops)) + (i - 2.5) * 0.13, delta, 0.13,
           color=colors_d[i], edgecolor='white', linewidth=0.5, label=f'Dev {d}')
ax.axhline(0, color='black', linewidth=0.8, alpha=0.5)
ax.set_xticks(range(len(ops)))
ax.set_xticklabels(ops, fontsize=11, fontweight='bold')
ax.set_ylabel('Δ efficiency (pp)', fontsize=10)
ax.set_title('Change: 2²⁹ − 2²⁸', fontsize=12, fontweight='bold')
ax.grid(axis='y', alpha=0.2)
ax.set_axisbelow(True)
ax.legend(fontsize=7, ncol=3, loc='lower left')

# ── Row 2: cumulative comparison ──
for label_short, dat, col, color in [('2²⁸', data_28, 0, '#2196F3'), ('2²⁹', data_29, 1, '#E91E63')]:
    ax = axes[1, col]
    cum = np.zeros(5)
    cum_vals = []
    for d in devs:
        cum = cum + np.array(dat[d])
        cum_vals.append(cum.copy())
    cum_arr = np.array(cum_vals) / MB_TO_TB
    ideal = np.array([baseline_1xcd * (i+1) / MB_TO_TB for i in range(6)])

    for op_idx, op_name, ls in [(3, 'Triad', '-'), (0, 'Copy', '--'), (4, 'Dot', ':')]:
        ax.plot(range(1, 7), cum_arr[:, op_idx], f'{ls}o', color=color, markersize=5,
                linewidth=2.2, label=f'{op_name}', alpha=1.0 if op_idx == 3 else 0.6)
        ax.plot(range(1, 7), ideal[:, op_idx], f'{ls}', color='black', alpha=0.2, linewidth=1.5)

    ax.axhline(THEORETICAL_BW_TB, color='red', linestyle=':', linewidth=1.5, alpha=0.6)
    ax.text(1.1, THEORETICAL_BW_TB + 0.05, '5.3 TB/s peak', fontsize=8, color='red', alpha=0.7)
    ax.set_xlabel('XCDs (cumulative)', fontsize=10)
    ax.set_ylabel('TB/s', fontsize=11)
    ax.set_xticks(range(1, 7))
    ax.set_xlim(0.5, 7)
    ax.set_ylim(0, THEORETICAL_BW_TB * 1.1)
    ax.grid(alpha=0.2)
    ax.set_axisbelow(True)
    ax.legend(fontsize=9, loc='upper left')
    ax.set_title(f'Cumulative — arraysize={label_short}', fontsize=12, fontweight='bold')

    # Annotate Triad final
    ax.annotate(f'{cum_arr[-1, 3]:.2f}', xy=(6, cum_arr[-1, 3]),
                xytext=(6, 6), textcoords='offset points',
                fontsize=9, fontweight='bold', color=color, va='bottom')

    ax2 = ax.twinx()
    ymin, ymax = ax.get_ylim()
    ax2.set_ylim(ymin * TB_TO_TIB, ymax * TB_TO_TIB)
    ax2.set_ylabel('TiB/s', fontsize=11)

# ── Row 2, col 3: side-by-side Triad cumulative overlay ──
ax = axes[1, 2]
for label_short, dat, color, ms in [('2²⁸', data_28, '#2196F3', 's'), ('2²⁹', data_29, '#E91E63', 'o')]:
    cum = np.zeros(5)
    cum_vals = []
    for d in devs:
        cum = cum + np.array(dat[d])
        cum_vals.append(cum.copy())
    cum_arr = np.array(cum_vals) / MB_TO_TB
    ax.plot(range(1, 7), cum_arr[:, 3], f'-{ms}', color=color, markersize=6,
            linewidth=2.2, label=f'Triad {label_short}')
    ax.annotate(f'{cum_arr[-1, 3]:.2f}', xy=(6, cum_arr[-1, 3]),
                xytext=(6, 4 if label_short == '2²⁸' else -12), textcoords='offset points',
                fontsize=9, fontweight='bold', color=color, va='center')

ideal = np.array([baseline_1xcd[3] * (i+1) / MB_TO_TB for i in range(6)])
ax.plot(range(1, 7), ideal, 'k--', alpha=0.3, linewidth=1.5, label='Ideal')
ax.axhline(THEORETICAL_BW_TB, color='red', linestyle=':', linewidth=1.5, alpha=0.6)

ax.set_xlabel('XCDs (cumulative)', fontsize=10)
ax.set_ylabel('TB/s', fontsize=11)
ax.set_xticks(range(1, 7))
ax.set_xlim(0.5, 7)
ax.set_ylim(0, THEORETICAL_BW_TB * 1.1)
ax.grid(alpha=0.2)
ax.set_axisbelow(True)
ax.legend(fontsize=9, loc='upper left')
ax.set_title('Triad: overlay comparison', fontsize=12, fontweight='bold')

ax2 = ax.twinx()
ymin, ymax = ax.get_ylim()
ax2.set_ylim(ymin * TB_TO_TIB, ymax * TB_TO_TIB)
ax2.set_ylabel('TiB/s', fontsize=11)

fig.suptitle('MI300A CPX — 6 XCDs on APU 0: arraysize 2²⁸ vs 2²⁹',
             fontsize=15, fontweight='bold')
fig.text(0.5, 0.005,
         'BabelStream · double-precision · numtimes=1500 · devices 0–5 on APU 0 · '
         'grey lines = ideal (linear from 1-XCD isolated baseline)',
         ha='center', fontsize=9, style='italic', color='#555555',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0f0f0', edgecolor='#cccccc', alpha=0.9))

plt.tight_layout(rect=[0, 0.035, 1, 0.94])
plt.savefig('/home/claude/cpx_1apu_28vs29.png', dpi=150, bbox_inches='tight')
print("Saved.")