```markdown
# 🧬 Molecular Dynamics Statistical Analysis Pipeline

A reproducible and statistically rigorous pipeline for analyzing molecular dynamics (MD) simulations generated from **GROMACS trajectories**.  

This framework implements advanced statistical treatment of time-correlated data, ensuring **robust uncertainty quantification, convergence assessment, and publication-quality outputs** for drug discovery and structural biology studies.

---

## 📌 Overview

Molecular dynamics simulations produce highly correlated time-series data that require specialized statistical treatment.  
This pipeline provides a **complete end-to-end workflow** for:

- Structural stability analysis
- Ligand binding dynamics evaluation
- Statistical uncertainty quantification
- Convergence diagnostics
- Publication-ready visualization

---

## 🚀 Key Features

### 📊 Statistical Robustness
- Block averaging to reduce autocorrelation bias
- Bootstrap resampling (BCa, 10,000+ iterations)
- Effective sample size (Neff) estimation
- Autocorrelation function (ACF) analysis

### 📉 Convergence Analysis
- Linear regression trend detection
- Sliding window statistical comparison
- Equilibration validation
- Drift detection in trajectories

### 🧪 Structural Descriptors
- RMSD (protein backbone & ligand)
- Radius of gyration (Rg)
- Solvent-accessible surface area (SASA)
- Hydrogen bond analysis
- Ligand RMSD

### 📦 Automation
- Fully automated pipeline execution
- Configurable analysis parameters
- Batch processing of multiple complexes
- Export of figures and statistical tables

---

## 🧬 Scientific Objective

This pipeline is designed to:

- Ensure statistically valid interpretation of MD simulations
- Compare ligand binding stability across multiple compounds
- Identify stable vs dynamic binding regimes
- Support structure-based drug design decisions

---

## 📁 Project Structure

```

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
│   │   ├── OPI/
│   │   ├── L2/
│   │   ├── ...
│   │   ├── comparison_plots/
│   │
│   ├── tables/
│   │   ├── summary_statistics.xlsx
│   │   ├── bootstrap_results.xlsx
│   │   ├── effective_sample_size.xlsx
│   │   ├── trend_analysis.xlsx
│   │   ├── convergence_analysis.xlsx
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

## ⚙️ Workflow

The analysis pipeline follows a rigorous statistical workflow:

```

Raw MD Trajectories (XVG files)
↓
Equilibration Filtering (50–150 ns)
↓
Block Averaging (5–10 ns blocks)
↓
Descriptive Statistics (mean, SD, CV, etc.)
↓
Bootstrap Resampling (BCa, 10,000 samples)
↓
Autocorrelation Analysis (Neff estimation)
↓
Trend Detection (linear regression)
↓
Convergence Testing (window comparison)
↓
Publication Outputs (tables + figures)

````

---

## 🧪 Statistical Methods

### 📊 Descriptive Statistics
- Mean, median, standard deviation (SD)
- Standard error of the mean (SEM)
- Coefficient of variation (CV)
- Interquartile range (IQR)

### 📉 Bootstrap Analysis
- 10,000 resampling iterations
- Bias-corrected and accelerated (BCa) confidence intervals
- Robust uncertainty quantification

### 🔁 Autocorrelation & Neff
- Integrated autocorrelation time
- Effective sample size (Neff)
- Sampling efficiency (%)

### 📈 Trend Analysis
- Linear regression on block-averaged data
- Slope and R² estimation
- Statistical significance (p < 0.05)

### ✔️ Convergence Criteria
A system is considered converged when:
- No significant trend is detected
- Stable statistical descriptors across time windows
- Consistent Neff and CV behavior

---

## 📦 Installation

### 1. Clone repository
```bash
git clone https://github.com/USERNAME/md-analysis-pipeline.git
cd md-analysis-pipeline
````

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Verify installation

```bash
python setup_verify.py
```

---

## ▶️ Usage

### Run full analysis

```bash
python run_analysis.py
```

### Output location

```
analysis_results/
```

Includes:

* Figures (PNG / PDF)
* Statistical tables (Excel / CSV)
* Convergence reports
* Processed block-averaged data

---

## 📊 Output Examples

### Figures

* RMSD time series plots
* Bootstrap distributions
* Autocorrelation functions
* Trend and convergence plots
* Ligand comparison plots

### Tables

* Summary statistics
* Effective sample size (Neff)
* Bootstrap confidence intervals
* Trend analysis results
* Publication-ready combined table

---

## 🧠 Interpretation Guidelines

### ✔️ Good Simulation Behavior

* Stable RMSD / ligand RMSD
* Low CV (< 5–10%)
* High Neff (good independence)
* No significant trend (p > 0.05)

### ⚠️ Potential Issues

* Significant drift in RMSD
* Low Neff (strong autocorrelation)
* High variability (CV > 10%)
* Non-converged trajectories

---

## 📚 Scientific Foundations

This pipeline is based on established statistical and computational chemistry methodologies:

* Efron & Tibshirani (1993) — Bootstrap methods
* DiCiccio & Efron (1996) — BCa confidence intervals
* Sokal (1997) — Autocorrelation in statistical mechanics
* Chodera & Shirts (2011) — Effective sample size in simulations
* Berg & Neuhaus (1992) — Block averaging techniques

---

## 👩‍🔬 Applications

* Drug discovery (ligand screening)
* Protein-ligand stability evaluation
* Structural bioinformatics
* Molecular mechanism investigation
* Comparative binding analysis

---

## 👤 Author

Developed for advanced molecular dynamics analysis in computational chemistry and bioinformatics.

---

## 📜 License

This project is intended for academic and research use. Modify freely with citation.

---

## ⭐ Future Improvements

* Free energy analysis (MM/PBSA integration)
* Principal component analysis (PCA)
* Markov state models (MSM)
* Machine learning-based clustering of trajectories

```
