import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ── Data ──────────────────────────────────────────────────────────────────────
BASE = '/zhome/academic/HLRS/hlrs/hpckkuec/cpx_tpx_test/logs'
cpx = pd.read_csv(f'{BASE}/010_cpx/summary.csv')
tpx = pd.read_csv(f'{BASE}/010_tpx/summary.csv')
spx = pd.read_csv(f'{BASE}/010_spx/summary.csv')

EXP_MIN, EXP_MAX = 10, 28
exps = list(range(EXP_MIN, EXP_MAX + 1))

MB_TO_TB  = 1e6
THEO_XCD  = 5.3 / 6   # TB/s per XCD ≈ 0.883
THEO_APU  = 5.3        # TB/s per APU
THEO_NODE = 5.3 * 4    # TB/s per node = 21.2

mode_colors = {'CPX': '#2196F3', 'TPX': '#FF9800', 'SPX': '#E91E63'}
op_colors   = {'Copy':  '#4CAF50', 'Mul': '#9C27B0',
               'Add':   '#FF5722', 'Triad': '#1565C0', 'Dot': '#E65100'}
op_cols = ['Copy_MBs', 'Mul_MBs', 'Add_MBs', 'Triad_MBs', 'Dot_MBs']
ops     = ['Copy', 'Mul', 'Add', 'Triad', 'Dot']

CPX_APU_MAP = {a: list(range(a * 6, (a + 1) * 6)) for a in range(4)}
TPX_APU_MAP = {a: list(range(a * 3, (a + 1) * 3)) for a in range(4)}
SPX_APU_MAP = {a: [a] for a in range(4)}

# ── Helpers ───────────────────────────────────────────────────────────────────

def buf_arr_mb(df):
    """Single-array buffer size in MB for each exp (doubles = 8 bytes)."""
    return np.array([df[df.exp == e]['arraysize_elements'].iloc[0] * 8 / 1e6
                     for e in exps])

def dev_stats(df, op_col='Triad_MBs'):
    """Mean / min / max of `op_col` across all devices, per exp. Returns TB/s."""
    mean_v, min_v, max_v = [], [], []
    for e in exps:
        vals = df[df.exp == e][op_col].values / MB_TO_TB
        mean_v.append(vals.mean()); min_v.append(vals.min()); max_v.append(vals.max())
    return np.array(mean_v), np.array(min_v), np.array(max_v)

def apu_stats(df, apu_map, op_col='Triad_MBs'):
    """Per-APU bandwidth (sum of devices in APU), then mean/min/max across 4 APUs."""
    mean_v, min_v, max_v = [], [], []
    for e in exps:
        rows_e = df[df.exp == e]
        apu_bws = [rows_e[rows_e.device.isin(apu_map[a])][op_col].sum() / MB_TO_TB
                   for a in range(4)]
        mean_v.append(np.mean(apu_bws)); min_v.append(np.min(apu_bws)); max_v.append(np.max(apu_bws))
    return np.array(mean_v), np.array(min_v), np.array(max_v)

def node_total(df, op_col='Triad_MBs'):
    """Whole-node bandwidth (sum of all devices) per exp. Returns TB/s."""
    return np.array([df[df.exp == e][op_col].sum() / MB_TO_TB for e in exps])

def saturation_buf(bw, buf, frac=0.90):
    """Buffer size (MB) at which bandwidth first reaches `frac` × max."""
    thresh = np.nanmax(bw) * frac
    idx = int(np.argmax(bw >= thresh))
    return buf[idx]

# ── X-axis vectors ─────────────────────────────────────────────────────────────
cpx_buf = buf_arr_mb(cpx)   # per-device = per-XCD for CPX
tpx_buf = buf_arr_mb(tpx)   # per-device (2 XCDs)
spx_buf = buf_arr_mb(spx)   # per-device (6 XCDs)
xcd_buf = cpx_buf            # per-XCD buffer (same scale for all after normalising)
apu_buf = xcd_buf * 6        # per-APU buffer (6 XCDs per APU, same for all modes)

# ── Figure ────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(21, 14))
gs  = fig.add_gridspec(2, 3, hspace=0.44, wspace=0.33)

# ════════════════════════════════════════════════════════════════════════════════
# Row 0 — individual mode plots (all 5 ops + Triad spread)
# ════════════════════════════════════════════════════════════════════════════════
def plot_mode(ax, df, buf, n_xcds, mode_color, title, theo_dev):
    for op, col in zip(ops, op_cols):
        mean_v, _, _ = dev_stats(df, col)
        ax.plot(buf, mean_v, '-o', color=op_colors[op],
                markersize=3.5, linewidth=1.8, label=op, zorder=3)

    t_mean, t_min, t_max = dev_stats(df, 'Triad_MBs')
    ax.fill_between(buf, t_min, t_max, alpha=0.12, color=mode_color, label='Triad spread')

    # Peak reference
    ax.axhline(theo_dev, color='red', linestyle='--', linewidth=1.2, alpha=0.7,
               label=f'Peak {theo_dev:.3f} TB/s')

    # Saturation marker
    sat = saturation_buf(t_mean, buf)
    ax.axvline(sat, color='steelblue', linestyle=':', linewidth=1.3, alpha=0.85,
               label=f'Sat. ~{sat:.0f} MB')

    ax.set_xscale('log')
    ax.set_xlabel('Buffer size per array (MB)', fontsize=10)
    ax.set_ylabel('TB/s', fontsize=10)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.legend(fontsize=7.5, ncol=2, loc='upper left')
    ax.grid(which='both', alpha=0.15); ax.set_axisbelow(True)


ax0 = fig.add_subplot(gs[0, 0])
plot_mode(ax0, cpx, cpx_buf, 1, mode_colors['CPX'],
          'CPX — per device (1 XCD)\n24 devices', THEO_XCD)

ax1 = fig.add_subplot(gs[0, 1])
plot_mode(ax1, tpx, tpx_buf, 2, mode_colors['TPX'],
          'TPX — per device (2 XCDs)\n12 devices', THEO_XCD * 2)

ax2 = fig.add_subplot(gs[0, 2])
plot_mode(ax2, spx, spx_buf, 6, mode_colors['SPX'],
          'SPX — per device (6 XCDs)\n4 devices', THEO_APU)

# ════════════════════════════════════════════════════════════════════════════════
# Row 1, Col 0 — per-APU overlay  (user's "plot 4")
# X: per-APU buffer = 6 × per-XCD buffer  →  same for all three modes
# ════════════════════════════════════════════════════════════════════════════════
ax3 = fig.add_subplot(gs[1, 0])
for mode, df, amap in [('CPX', cpx, CPX_APU_MAP),
                        ('TPX', tpx, TPX_APU_MAP),
                        ('SPX', spx, SPX_APU_MAP)]:
    mean_v, min_v, max_v = apu_stats(df, amap)
    ax3.plot(apu_buf, mean_v, '-o', color=mode_colors[mode],
             markersize=4, linewidth=2.2, label=mode, zorder=3)
    ax3.fill_between(apu_buf, min_v, max_v, alpha=0.13, color=mode_colors[mode])

ax3.axhline(THEO_APU, color='red', linestyle='--', linewidth=1.2, alpha=0.7,
            label=f'APU peak {THEO_APU} TB/s')
sat_cpx = saturation_buf(apu_stats(cpx, CPX_APU_MAP)[0], apu_buf)
ax3.axvline(sat_cpx, color='steelblue', linestyle=':', linewidth=1.3, alpha=0.85,
            label=f'Sat. ~{sat_cpx:.0f} MB')
ax3.set_xscale('log')
ax3.set_xlabel('Per-APU buffer size per array (MB)', fontsize=10)
ax3.set_ylabel('TB/s  (per APU)', fontsize=10)
ax3.set_title('Triad bandwidth per APU\n(CPX / TPX / SPX on same APU scale)', fontsize=12, fontweight='bold')
ax3.legend(fontsize=9); ax3.grid(which='both', alpha=0.15); ax3.set_axisbelow(True)

# ════════════════════════════════════════════════════════════════════════════════
# Row 1, Col 1 — per-XCD normalised  (key insight: do modes agree?)
# X: per-XCD buffer size  (= CPX per-device = TPX per-device / 2 = SPX / 6)
# Y: per-device bandwidth / n_xcds
# ════════════════════════════════════════════════════════════════════════════════
ax4 = fig.add_subplot(gs[1, 1])
for mode, df, n_xcds in [('CPX', cpx, 1), ('TPX', tpx, 2), ('SPX', spx, 6)]:
    mean_v, min_v, max_v = dev_stats(df, 'Triad_MBs')
    ax4.plot(xcd_buf, mean_v / n_xcds, '-o', color=mode_colors[mode],
             markersize=4, linewidth=2.2, label=mode, zorder=3)
    ax4.fill_between(xcd_buf, min_v / n_xcds, max_v / n_xcds,
                     alpha=0.13, color=mode_colors[mode])

ax4.axhline(THEO_XCD, color='red', linestyle='--', linewidth=1.2, alpha=0.7,
            label=f'XCD peak {THEO_XCD:.3f} TB/s')
ax4.set_xscale('log')
ax4.set_xlabel('Per-XCD buffer size per array (MB)', fontsize=10)
ax4.set_ylabel('TB/s  (per XCD)', fontsize=10)
ax4.set_title('Triad bandwidth per XCD — normalised\n(overlap = partition mode is transparent)', fontsize=12, fontweight='bold')
ax4.legend(fontsize=9); ax4.grid(which='both', alpha=0.15); ax4.set_axisbelow(True)

# ════════════════════════════════════════════════════════════════════════════════
# Row 1, Col 2 — whole-node total bandwidth
# ════════════════════════════════════════════════════════════════════════════════
ax5 = fig.add_subplot(gs[1, 2])
for mode, df in [('CPX', cpx), ('TPX', tpx), ('SPX', spx)]:
    bw = node_total(df)
    ax5.plot(xcd_buf, bw, '-o', color=mode_colors[mode],
             markersize=4, linewidth=2.2, label=mode, zorder=3)

ax5.axhline(THEO_NODE, color='red', linestyle='--', linewidth=1.2, alpha=0.7,
            label=f'Node peak {THEO_NODE:.1f} TB/s')
ax5.set_xscale('log')
ax5.set_xlabel('Per-XCD buffer size per array (MB)', fontsize=10)
ax5.set_ylabel('TB/s  (whole node)', fontsize=10)
ax5.set_title('Triad bandwidth: whole node\n(CPX / TPX / SPX)', fontsize=12, fontweight='bold')
ax5.legend(fontsize=9); ax5.grid(which='both', alpha=0.15); ax5.set_axisbelow(True)

# ── Titles & caption ──────────────────────────────────────────────────────────
fig.suptitle('MI300A BabelStream — Buffer Size Sweep: CPX / TPX / SPX',
             fontsize=16, fontweight='bold')
fig.text(0.5, 0.005,
         'BabelStream · double-precision · '
         'CPX: 24 devices × 1 XCD, array = 1×2ⁿ elems, numtimes=1500 · '
         'TPX: 12 devices × 2 XCDs, array = 2×2ⁿ elems, numtimes=600 · '
         'SPX: 4 devices × 6 XCDs, array = 6×2ⁿ elems, numtimes=250 · '
         'theoretical peak: 5.3 TB/s / APU (0.883 TB/s / XCD), 21.2 TB/s / node',
         ha='center', fontsize=8.5, style='italic', color='#555555',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0f0f0', edgecolor='#cccccc', alpha=0.9))

plt.tight_layout(rect=[0, 0.04, 1, 0.96])
out = '/zhome/academic/HLRS/hlrs/hpckkuec/cpx_tpx_test/plotting/010_sweep_bandwidth.png'
plt.savefig(out, dpi=150, bbox_inches='tight')
print(f'Saved → {out}')
