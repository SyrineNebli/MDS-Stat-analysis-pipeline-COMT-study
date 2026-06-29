"""
Configuration file for MD Analysis Pipeline
Edit these settings to match your project structure
"""

import os
from pathlib import Path

# ============================================================================
# PROJECT SETUP
# ============================================================================

# Root directory containing all complex folders
PROJECT_ROOT = Path("./project")  # Change to your project directory

# Folder names (complexes to analyze)
COMPLEXES = ["OPI", "L2", "L4", "L10", "L11", "DNC"]

# XVG file names to analyze (must exist in each complex folder)
XVG_FILES = {
    "rmsd": "rmsd.xvg",
    "rg": "rg.xvg",
    "sasa": "sasa.xvg",
    "hbonds": "hbonds.xvg",
    "ligand_rmsd": "ligand_rmsd.xvg",
}

# ============================================================================
# SIMULATION PARAMETERS
# ============================================================================

# Total simulation length (ns)
TOTAL_TIME_NS = 150.0

# Equilibration period to exclude (ns)
EQUILIBRATION_NS = 50.0

# Block size for block averaging (ns)
# Options: 5, 10, 20
BLOCK_SIZE_NS = 5.0

# Time unit in XVG files (typically "ps" for picoseconds)
TIME_UNIT = "ps"

# ============================================================================
# STATISTICAL PARAMETERS
# ============================================================================

# Bootstrap parameters
N_BOOTSTRAP = 10000
BOOTSTRAP_CI = 95  # Confidence interval percentage

# Autocorrelation parameters
MAX_LAG_NS = 50.0  # Maximum lag to calculate autocorrelation (ns)

# Linear trend analysis
TREND_P_VALUE_THRESHOLD = 0.05

# ============================================================================
# OUTPUT SETTINGS
# ============================================================================

# Output directory
OUTPUT_DIR = Path("./analysis_results")

# Create output subdirectories
FIGURES_DIR = OUTPUT_DIR / "figures"
TABLES_DIR = OUTPUT_DIR / "tables"
DATA_DIR = OUTPUT_DIR / "processed_data"

# Figure format and quality
FIGURE_FORMAT = "png"  # Options: "png", "pdf", "both"
DPI = 300  # Resolution for raster formats

# Excel output settings
EXPORT_EXCEL = True
EXPORT_CSV = True
EXPORT_WORD_TABLES = True  # Creates formatted tables for Word

# ============================================================================
# PLOTTING SETTINGS
# ============================================================================

# Plot style
PLOT_STYLE = "seaborn-v0_8-darkgrid"  # or "default", "ggplot", etc.

# Color palette
COLOR_PALETTE = "husl"  # Options: "husl", "Set2", "Set1", "pastel", etc.

# Figure sizes (in inches)
FIGSIZE_SINGLE = (10, 6)
FIGSIZE_DOUBLE = (16, 6)
FIGSIZE_TRIPLE = (16, 10)

# Font sizes
FONTSIZE_TITLE = 14
FONTSIZE_LABEL = 12
FONTSIZE_TICK = 10
FONTSIZE_LEGEND = 10

# ============================================================================
# CONVERGENCE SETTINGS
# ============================================================================

# Time windows for convergence analysis (ns)
# If you have 150 ns total, set windows to compare
CONVERGENCE_WINDOWS = {
    "window1": (EQUILIBRATION_NS, 100.0),  # 50-100 ns
    "window2": (100.0, 150.0),               # 100-150 ns
}

# ============================================================================
# SPECIAL ANALYSIS OPTIONS
# ============================================================================

# RMSF analysis (per-residue)
PERFORM_RMSF_ANALYSIS = False
RMSF_FILE_PATTERN = "rmsf_*.xvg"  # Pattern to match RMSF files

# Binding site analysis (if you have specific residue ranges)
PERFORM_BINDING_SITE_ANALYSIS = False
BINDING_SITE_RESIDUES = {
    "binding_site_1": (10, 50),  # Residue range
    "binding_site_2": (100, 150),
}

# ============================================================================
# ADVANCED OPTIONS
# ============================================================================

# Autocorrelation method for effective sample size
# Options: "direct", "fft" (fast Fourier transform)
AUTOCORR_METHOD = "fft"

# Effective sample size calculation
# Options: "integrated" (recommended), "acf_decay"
ESS_METHOD = "integrated"

# Outlier detection for bootstrap
REMOVE_OUTLIERS = False
OUTLIER_THRESHOLD = 3.0  # Standard deviations

# Verbosity level (0=silent, 1=info, 2=debug)
VERBOSE = 1

# ============================================================================
# QUALITY CHECKS
# ============================================================================

# Warn if block size is <1% of trajectory
MIN_BLOCK_FRACTION = 0.01

# Warn if blocks < 10 total blocks
MIN_BLOCKS = 10

# Convergence test p-value threshold
CONVERGENCE_P_THRESHOLD = 0.05

# ============================================================================
# AUTO-GENERATED PATHS (Do not edit)
# ============================================================================

# Create output directories if they don't exist
def create_directories():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    create_directories()
    print("✓ Configuration loaded successfully")
    print(f"  Project root: {PROJECT_ROOT}")
    print(f"  Complexes: {', '.join(COMPLEXES)}")
    print(f"  Output directory: {OUTPUT_DIR}")
