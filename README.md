# 🧬 Molecular Dynamics Statistical Analysis Pipeline

A reproducible and statistically rigorous pipeline for analyzing **GROMACS molecular dynamics (MD) trajectories**.

This framework provides robust statistical analysis of time-correlated MD data, including uncertainty quantification, convergence assessment, and publication-quality visualizations for computational chemistry, structural biology, and drug discovery.

---

# 📌 Overview

Molecular dynamics trajectories consist of highly autocorrelated time-series data that require specialized statistical treatment.

This pipeline performs a complete analysis workflow including:

- Structural stability analysis
- Ligand binding dynamics
- Statistical uncertainty estimation
- Convergence diagnostics
- Publication-ready figures and tables

---

# 🚀 Features

## 📊 Statistical Analysis

- Block averaging to reduce autocorrelation
- Bootstrap confidence intervals (BCa, 10,000+ resamples)
- Effective sample size (Neff)
- Autocorrelation analysis
- Descriptive statistics

## 📉 Convergence Assessment

- Linear regression trend analysis
- Drift detection
- Sliding-window comparison
- Equilibration validation

## 🧬 Structural Descriptors

- Protein RMSD
- Ligand RMSD
- Radius of gyration (Rg)
- Solvent-accessible surface area (SASA)
- Hydrogen bonds

## ⚙️ Automation

- Batch processing
- Configurable parameters
- Automatic figure generation
- Excel and CSV exports

---

# 🎯 Scientific Objective

The pipeline enables statistically rigorous comparison of MD simulations by:

- Quantifying structural stability
- Evaluating ligand binding behavior
- Detecting simulation drift
- Assessing convergence
- Producing publication-quality statistical summaries

---

# 📁 Project Structure

```text
project/
│
├── OPI/
├── DNC/
├── L2/
├── L4/
├── L10/
├── L11/
│   ├── rmsd.xvg
│   ├── rg.xvg
│   ├── sasa.xvg
│   ├── hbonds.xvg
│   └── ligand_rmsd.xvg
│
├── analysis_results/
│   ├── figures/
│   │   ├── comparison_plots/
│   │   ├── OPI/
│   │   ├── DNC/
│   │   ├── L2/
│   │   └── ...
│   │
│   ├── tables/
│   │   ├── summary_statistics.xlsx
│   │   ├── bootstrap_results.xlsx
│   │   ├── effective_sample_size.xlsx
│   │   ├── trend_analysis.xlsx
│   │   └── convergence_analysis.xlsx
│   │
│   ├── processed_data/
│   └── analysis_summary.txt
│
├── src/
│   ├── md_statistics.py
│   ├── plotting.py
│   ├── export.py
│   └── run_analysis.py
│
├── config.py
├── setup_verify.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Workflow

```text
Raw GROMACS XVG files
          │
          ▼
 Equilibration filtering
     (e.g. 50–150 ns)
          │
          ▼
   Block averaging
     (5–10 ns)
          │
          ▼
 Descriptive statistics
          │
          ▼
 Bootstrap resampling
 (10,000 BCa iterations)
          │
          ▼
 Autocorrelation analysis
      (Neff estimation)
          │
          ▼
 Linear trend detection
          │
          ▼
 Convergence assessment
          │
          ▼
 Publication-ready tables
      and figures
```

---

# 📊 Statistical Methods

## Descriptive Statistics

- Mean
- Median
- Standard deviation (SD)
- Standard error (SEM)
- Coefficient of variation (CV)
- Interquartile range (IQR)

---

## Bootstrap Analysis

- BCa bootstrap confidence intervals
- 10,000 resampling iterations
- Robust uncertainty estimation

---

## Autocorrelation Analysis

- Autocorrelation function (ACF)
- Integrated autocorrelation time
- Effective sample size (Neff)
- Sampling efficiency

---

## Trend Analysis

Linear regression is performed on block-averaged trajectories to estimate:

- Slope
- R²
- p-value

---

## Convergence Criteria

A trajectory is considered converged when:

- No significant linear trend
- Stable statistical descriptors
- Consistent Neff
- Stable block averages

---

# 📦 Installation

## Clone repository

```bash
git clone https://github.com/SyrineNebli/MDS-Stat-analysis-pipeline-COMT-study.git
cd MDS-Stat-analysis-pipeline-COMT-study
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Verify installation

```bash
python setup_verify.py
```

---

# ▶️ Usage

Run the complete analysis:

```bash
python run_analysis.py
```

Results are automatically saved in

```text
analysis_results/
```

including

- Figures
- Statistical tables
- Convergence reports
- Processed trajectories

---

# 📈 Generated Outputs

## Figures

- RMSD time series
- Ligand RMSD
- Radius of gyration
- SASA
- Hydrogen bonds
- Bootstrap distributions
- Autocorrelation functions
- Trend analysis
- Comparison plots

## Tables

- Summary statistics
- Bootstrap confidence intervals
- Effective sample size
- Trend analysis
- Convergence diagnostics


# 📚 Statistical Foundations

The implemented methodology follows established references:

- Berg & Neuhaus (1992) – Block averaging
- Efron & Tibshirani (1993) – Bootstrap methods
- DiCiccio & Efron (1996) – BCa confidence intervals
- Sokal (1997) – Autocorrelation analysis
- Chodera & Shirts (2011) – Effective sample size estimation

---

# 🔬 Applications

- Structure-based drug discovery
- Protein–ligand stability analysis
- Comparative MD studies
- Computational structural biology
- Molecular mechanism investigation

---
