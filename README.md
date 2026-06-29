🔬 MD Analysis Pipeline (Statistical Framework for Molecular Dynamics)

This repository provides a fully automated statistical analysis pipeline for molecular dynamics (MD) trajectories generated with GROMACS.
It implements rigorous statistical treatment of time-correlated data to ensure reproducibility and publication-quality results.

🚀 Features
Block averaging of MD trajectories (handles autocorrelation)
Bootstrap-based confidence intervals (BCa, 10,000 resamples)
Effective Sample Size (Neff) estimation
Trend detection via linear regression
Convergence testing across simulation windows
Publication-ready figures and tables
📊 Supported Descriptors
RMSD (protein & ligand)
Radius of gyration (Rg)
Solvent-accessible surface area (SASA)
Hydrogen bonds
Ligand RMSD
⚙️ Workflow

Raw MD data (XVG files)
→ Equilibration filtering
→ Block averaging
→ Statistical descriptors
→ Bootstrap CI estimation
→ Autocorrelation & Neff analysis
→ Trend & convergence testing
→ Publication outputs

📁 Project Structure
project/
 ├── OPI/
 ├── L2/
 ├── L4/
 ├── L10/
 ├── L11/
 ├── DNC/

analysis_results/
 ├── figures/
 ├── tables/
 ├── processed_data/
 ├── analysis_summary.txt
🧪 Statistical Methods

This pipeline applies:

Block averaging to reduce autocorrelation effects
Bootstrap (BCa, 10,000 resamples) for confidence intervals
Integrated autocorrelation time for Neff estimation
Linear regression for trend detection
Window-based convergence testing
📦 Installation
pip install -r requirements.txt
▶️ Usage
python setup_verify.py
python run_analysis.py
📈 Output
Publication-ready figures (PNG/PDF)
Excel/CSV statistical summaries
Convergence reports
Bootstrap analysis tables
📚 Scientific Basis
Efron & Tibshirani (1993) — Bootstrap
Sokal (1997) — Autocorrelation in MC/MD
Chodera & Shirts (2011) — Effective sample size
DiCiccio & Efron (1996) — BCa confidence intervals
Berg & Neuhaus (1992) — Block averaging
