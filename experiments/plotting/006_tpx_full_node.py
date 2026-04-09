import matplotlib.pyplot as plt
import numpy as np

ops = ['Copy', 'Mul', 'Add', 'Triad', 'Dot']

# TPX full node: 12 devices, 3 per APU
data = {
    0:  [1341471.750, 1358507.388, 1359284.728, 1366840.203, 1175886.691],
    1:  [1290910.388, 1309791.059, 1350511.059, 1360561.872, 1171195.541],
    2:  [1417377.108, 1418411.115, 1427905.451, 1427965.585, 1376952.649],
    3:  [1413137.540, 1416629.108, 1425482.160, 1426144.825, 1370646.901],
    4:  [1416007.934, 1416988.517, 1428082.702, 1428190.657, 1353494.183],
    5:  [1335735.279, 1329878.810, 1340571.387, 1335419.501, 1133566.954],
    6:  [1414631.617, 1416250.734, 1426792.306, 1426871.307, 1279896.706],
    7:  [1416138.195, 1416923.072, 1427981.410, 1428102.013, 1351960.829],
    8:  [1315890.718, 1334705.432, 1328956.927, 1315158.983, 1080797.813],
    9:  [1314251.892, 1324293.932, 1318108.077, 1334655.938, 1141287.195],
    10: [1416381.507, 1417475.342, 1427807.349, 1427930.770, 1356799.765],
    11: [1414534.243, 1416128.857, 1425264.562, 1426514.291, 1269189.372],
}

# TPX mapping: 3 devices per APU
apu_map = {
    'APU 0': [0, 1, 2],
    'APU 1': [3, 4, 5],
    'APU 2': [6, 7, 8],
    'APU 3': [9, 10, 11],
}
apu_colors = {'APU 0': '#2196F3', 'APU 1': '#FF9800', 'APU 2': '#E91E63', 'APU 3': '#4CAF50'}

MB_TO_TB = 1e6
TB_TO_TIB = 1e12 / (2**40)
THEORETICAL_BW_TB = 5.3

# 1-XCD isolated baseline (from earlier experiment), scaled to 2-XCD TPX device
baseline_1xcd = np.array([710919.819, 711137.930, 714967.461, 714965.925, 704574.931])
baseline_tpx_device = baseline_1xcd * 2  # ideal per TPX device

fig, axes = plt.subplots(2, 3, figsize=(18, 10))

# ── Row 1, col 1: per-device bars (Triad only for clarity) ──
ax = axes[0, 0]
all_devs = list(range(12))
dev_apu_color = []
for d in all_devs:
    for apu, devs in apu_map.items():
        if d in devs:
            dev_apu_color.append(apu_colors[apu])

triad_idx = 3
vals = [data[d][triad_idx] / MB_TO_TB for d in all_devs]
bars = ax.bar(range(12), vals, color=dev_apu_color, edgecolor='white', linewidth=0.5, zorder=3)
ax.axhline(baseline_tpx_device[triad_idx] / MB_TO_TB, color='red', linestyle='--',
           alpha=0.5, linewidth=1.2, label='Ideal per TPX device')
ax.set_xticks(range(12))
ax.set_xticklabels([f'{d}' for d in all_devs], fontsize=9)
ax.set_xlabel('Device', fontsize=10)
ax.set_ylabel('TB/s', fontsize=11)
ax.set_ylim(1.2, 1.5)
ax.grid(axis='y', alpha=0.2)
ax.set_axisbelow(True)
ax.legend(fontsize=8)
ax.set_title('Triad per device', fontsize=13, fontweight='bold')

ax2 = ax.twinx()
ymin, ymax = ax.get_ylim()
ax2.set_ylim(ymin * TB_TO_TIB, ymax * TB_TO_TIB)
ax2.set_ylabel('TiB/s', fontsize=11)

# ── Row 1, col 2: efficiency vs isolated baseline ──
ax = axes[0, 1]
dev_markers = ['o', 's', '^']
for apu, devs in apu_map.items():
    for i, d in enumerate(devs):
        pcts = np.array(data[d]) / baseline_tpx_device * 100
        ax.plot(ops, pcts, f'-{dev_markers[i]}', color=apu_colors[apu], markersize=6,
                linewidth=1.5, label=f'Dev {d} ({apu})', alpha=0.8)

ax.axhline(100, color='red', linestyle='--', alpha=0.5, linewidth=1.2)
ax.set_ylabel('% of ideal (2× isolated 1-XCD)', fontsize=10)
ax.set_ylim(72, 105)
ax.grid(alpha=0.2)
ax.set_axisbelow(True)
ax.legend(fontsize=6.5, ncol=3, loc='lower left')
ax.set_title('Efficiency vs. ideal', fontsize=13, fontweight='bold')

# ── Row 1, col 3: cumulative per APU (Triad) ──
ax = axes[0, 2]
ideal_cum = np.array([baseline_tpx_device[triad_idx] * (i+1) / MB_TO_TB for i in range(3)])

for apu in ['APU 0', 'APU 1', 'APU 2', 'APU 3']:
    devs = apu_map[apu]
    cum = np.zeros(5)
    cum_vals = []
    for d in devs:
        cum = cum + np.array(data[d])
        cum_vals.append(cum.copy())
    cum_arr = np.array(cum_vals) / MB_TO_TB
    ax.plot(range(1, 4), cum_arr[:, triad_idx], '-o', color=apu_colors[apu],
            markersize=6, linewidth=2.2, label=apu)
    ax.annotate(f'{cum_arr[-1, triad_idx]:.2f}', xy=(3, cum_arr[-1, triad_idx]),
                xytext=(6, 0), textcoords='offset points',
                fontsize=9, fontweight='bold', color=apu_colors[apu], va='center')

ax.plot(range(1, 4), ideal_cum, 'k--', alpha=0.3, linewidth=1.5, label='Ideal')
ax.axhline(THEORETICAL_BW_TB, color='red', linestyle=':', linewidth=1.5, alpha=0.6)
ax.text(1.1, THEORETICAL_BW_TB + 0.05, '5.3 TB/s peak', fontsize=8, color='red', alpha=0.7)

ax.set_xlabel('TPX devices (cumulative per APU)', fontsize=10)
ax.set_ylabel('TB/s', fontsize=11)
ax.set_xticks(range(1, 4))
ax.set_xlim(0.5, 4.2)
ax.set_ylim(0, THEORETICAL_BW_TB * 1.1)
ax.grid(alpha=0.2)
ax.set_axisbelow(True)
ax.legend(fontsize=9, loc='upper left')
ax.set_title('Cumulative Triad per APU', fontsize=13, fontweight='bold')

ax2 = ax.twinx()
ymin, ymax = ax.get_ylim()
ax2.set_ylim(ymin * TB_TO_TIB, ymax * TB_TO_TIB)
ax2.set_ylabel('TiB/s', fontsize=11)

# ── Row 2: all 5 ops cumulative ──
for j, op in enumerate(ops):
    ax = axes[1, j] if j < 3 else None
    if j >= 3:
        break
    ax_cur = axes[1, j]

    for apu in ['APU 0', 'APU 1', 'APU 2', 'APU 3']:
        devs_list = apu_map[apu]
        cum = np.zeros(5)
        cum_vals = []
        for d in devs_list:
            cum = cum + np.array(data[d])
            cum_vals.append(cum.copy())
        cum_arr = np.array(cum_vals) / MB_TO_TB
        ideal_op = np.array([baseline_tpx_device[j] * (i+1) / MB_TO_TB for i in range(3)])
        ax_cur.plot(range(1, 4), cum_arr[:, j], '-o', color=apu_colors[apu],
                    markersize=5, linewidth=2, label=apu)
        ax_cur.annotate(f'{cum_arr[-1, j]:.2f}', xy=(3, cum_arr[-1, j]),
                        xytext=(6, 0), textcoords='offset points',
                        fontsize=8.5, color=apu_colors[apu], fontweight='bold', va='center')

    ideal_op = np.array([baseline_tpx_device[j] * (i+1) / MB_TO_TB for i in range(3)])
    ax_cur.plot(range(1, 4), ideal_op, 'k--', alpha=0.3, linewidth=1.5, label='Ideal')
    ax_cur.axhline(THEORETICAL_BW_TB, color='red', linestyle=':', linewidth=1.5, alpha=0.6)

    ax_cur.set_title(op, fontsize=13, fontweight='bold')
    ax_cur.set_xlabel('TPX devices (cumulative)', fontsize=10)
    ax_cur.set_ylabel('TB/s', fontsize=11)
    ax_cur.set_xticks(range(1, 4))
    ax_cur.set_xlim(0.5, 4.5)
    ax_cur.set_ylim(0, THEORETICAL_BW_TB * 1.1)
    ax_cur.grid(alpha=0.2)
    ax_cur.set_axisbelow(True)
    if j == 0:
        ax_cur.legend(fontsize=8, loc='upper left')

    ax2 = ax_cur.twinx()
    ymin, ymax = ax_cur.get_ylim()
    ax2.set_ylim(ymin * TB_TO_TIB, ymax * TB_TO_TIB)
    ax2.set_ylabel('TiB/s', fontsize=11)

# Overwrite row2 to show all 5 ops properly
# Actually let's redo row 2 as: Copy, Mul, Dot (Add/Triad already similar to Triad above)
for col, j in enumerate([0, 1, 4]):  # Copy, Mul, Dot
    ax_cur = axes[1, col]
    ax_cur.clear()
    op = ops[j]

    for apu in ['APU 0', 'APU 1', 'APU 2', 'APU 3']:
        devs_list = apu_map[apu]
        cum = np.zeros(5)
        cum_vals = []
        for d in devs_list:
            cum = cum + np.array(data[d])
            cum_vals.append(cum.copy())
        cum_arr = np.array(cum_vals) / MB_TO_TB
        ax_cur.plot(range(1, 4), cum_arr[:, j], '-o', color=apu_colors[apu],
                    markersize=5, linewidth=2.2, label=apu)
        ax_cur.annotate(f'{cum_arr[-1, j]:.2f}', xy=(3, cum_arr[-1, j]),
                        xytext=(6, 0), textcoords='offset points',
                        fontsize=8.5, color=apu_colors[apu], fontweight='bold', va='center')

    ideal_op = np.array([baseline_tpx_device[j] * (i+1) / MB_TO_TB for i in range(3)])
    ax_cur.plot(range(1, 4), ideal_op, 'k--', alpha=0.3, linewidth=1.5, label='Ideal')
    ax_cur.axhline(THEORETICAL_BW_TB, color='red', linestyle=':', linewidth=1.5, alpha=0.6)
    ax_cur.text(1.1, THEORETICAL_BW_TB + 0.05, '5.3 TB/s peak', fontsize=8, color='red', alpha=0.7)

    ax_cur.set_title(op, fontsize=13, fontweight='bold')
    ax_cur.set_xlabel('TPX devices (cumulative per APU)', fontsize=10)
    ax_cur.set_ylabel('TB/s', fontsize=11)
    ax_cur.set_xticks(range(1, 4))
    ax_cur.set_xlim(0.5, 4.5)
    ax_cur.set_ylim(0, THEORETICAL_BW_TB * 1.1)
    ax_cur.grid(alpha=0.2)
    ax_cur.set_axisbelow(True)
    if col == 0:
        ax_cur.legend(fontsize=8, loc='upper left')

    ax2 = ax_cur.twinx()
    ymin, ymax = ax_cur.get_ylim()
    ax2.set_ylim(ymin * TB_TO_TIB, ymax * TB_TO_TIB)
    ax2.set_ylabel('TiB/s', fontsize=11)

fig.suptitle('MI300A TPX Mode — Full Node BabelStream (12 devices, 3 per APU, 2 XCDs each)',
             fontsize=14, fontweight='bold')
fig.text(0.5, 0.005,
         'BabelStream · double-precision · arraysize=2²⁸ · numtimes=1500 · '
         'TPX mode (2 XCDs/device) · "ideal" = 2× isolated 1-XCD baseline',
         ha='center', fontsize=9, style='italic', color='#555555',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0f0f0', edgecolor='#cccccc', alpha=0.9))

plt.tight_layout(rect=[0, 0.035, 1, 0.94])
plt.savefig('/home/claude/tpx_full_node.png', dpi=150, bbox_inches='tight')
print("Saved.")