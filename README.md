# MI300A BabelStream: CPX vs TPX vs SPX

BabelStream memory bandwidth benchmarks on AMD MI300A under different partition modes (CPX, TPX, SPX) on the Hunter cluster.

![CPX vs TPX vs SPX Comparison](figures/008_cpx_tpx_spx_comparison.png)

## Repository Structure

- `0XX_test_*.sh` -- experiment scripts for each configuration
- `plotting/` -- matplotlib scripts that produce the figures (data is embedded directly in each script)
- `figures/` -- output PNGs from the plotting scripts
- `reporting/` -- summary report (docx) and presentation (pptx)

## Notes on Data and Reporting

- Run outputs were manually pasted into Claude and the plotting scripts were generated from those results. A subset of values were spot-checked against manual calculations and appeared correct; a full audit was not performed but no parsing errors are suspected.
- The report and presentation in `reporting/` were summarized by Claude. There may be subtle interpretation errors, but the raw data tables speak for themselves.

## BabelStream Build (Hunter)

```bash
git clone https://github.com/UoB-HPC/BabelStream
cd BabelStream
git checkout 2f00dfb7f8b7cfe8c53d20d5c770bccbf8673440
cmake -B build -DMODEL=hip -DCMAKE_CXX_COMPILER=hipcc
cmake --build build
```
