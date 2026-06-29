"""
Debug script to diagnose XVG file reading issues
"""

import numpy as np
from pathlib import Path
import config
import md_statistics as stats

print("\n" + "="*70)
print("XVG FILE DEBUGGING")
print("="*70)

# Test with first complex
test_complex = config.COMPLEXES[0]
test_descriptor = "rmsd"

print(f"\nTesting: {test_complex}/{config.XVG_FILES[test_descriptor]}")

# Load raw data
filepath = config.PROJECT_ROOT / test_complex / config.XVG_FILES[test_descriptor]
print(f"File path: {filepath}")
print(f"File exists: {filepath.exists()}")

# Read XVG
time, values = stats.read_xvg(filepath)

print(f"\n--- RAW DATA ---")
print(f"Number of points: {len(values)}")
print(f"Time range: {time[0]:.6f} to {time[-1]:.6f} ns")
print(f"Value range: {np.min(values):.6f} to {np.max(values):.6f}")
print(f"NaN count (raw): {np.sum(np.isnan(values))}")
print(f"Inf count (raw): {np.sum(np.isinf(values))}")

print(f"\nFirst 10 values:")
for i in range(min(10, len(values))):
    print(f"  t={time[i]:.3f} ns → value={values[i]:.6f}")

# Select equilibrated region
time_eq, values_eq = stats.select_equilibrated_region(time, values)

print(f"\n--- AFTER EQUILIBRATION (>= {config.EQUILIBRATION_NS} ns) ---")
print(f"Number of points: {len(values_eq)}")
if len(values_eq) > 0:
    print(f"Time range: {time_eq[0]:.6f} to {time_eq[-1]:.6f} ns")
    print(f"Value range: {np.min(values_eq):.6f} to {np.max(values_eq):.6f}")
    print(f"NaN count: {np.sum(np.isnan(values_eq))}")
    print(f"Inf count: {np.sum(np.isinf(values_eq))}")
    
    print(f"\nFirst 10 equilibrated values:")
    for i in range(min(10, len(values_eq))):
        print(f"  t={time_eq[i]:.3f} ns → value={values_eq[i]:.6f}")
else:
    print("NO DATA AFTER EQUILIBRATION CUTOFF!")
    print(f"Check: Is data time range > {config.EQUILIBRATION_NS} ns?")

# Try block averaging
if len(values_eq) > 0:
    print(f"\n--- BLOCK AVERAGING ---")
    try:
        block_time, block_means, block_stds, block_sems = stats.block_average(
            time_eq, values_eq
        )
        print(f"Block size: {config.BLOCK_SIZE_NS} ns")
        print(f"Number of blocks: {len(block_means)}")
        print(f"Block means range: {np.min(block_means):.6f} to {np.max(block_means):.6f}")
        print(f"Block means (first 5):")
        for i in range(min(5, len(block_means))):
            print(f"  Block {i}: {block_means[i]:.6f}")
    except Exception as e:
        print(f"ERROR in block averaging: {e}")

print("\n" + "="*70)
