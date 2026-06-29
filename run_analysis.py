"""
MD Analysis Pipeline - Main Script
Complete automated analysis of MD simulation trajectories

Usage:
    python run_analysis.py

This script:
1. Loads all XVG files from each complex
2. Performs block averaging
3. Calculates descriptive statistics
4. Performs bootstrap analysis
5. Calculates effective sample size
6. Performs trend analysis and convergence testing
7. Generates publication-quality figures
8. Exports all results to Excel and CSV
"""

import numpy as np
import pandas as pd
from pathlib import Path
import warnings
import time

# Import custom modules
import config
import md_statistics as stats
import plotting
import export

warnings.filterwarnings('ignore')

# ============================================================================
# MAIN ANALYSIS PIPELINE
# ============================================================================

def analyze_complex(complex_name):
    """
    Perform complete analysis for a single complex.
    
    Parameters
    ----------
    complex_name : str
        Name of complex to analyze
        
    Returns
    -------
    dict
        All analysis results for this complex
    """
    print(f"\n{'='*70}")
    print(f"Analyzing: {complex_name}")
    print(f"{'='*70}")
    
    # Load data
    print("\n1. Loading XVG files...")
    complex_data = stats.load_complex_data(complex_name)
    
    if not complex_data:
        print(f"  ✗ No data loaded for {complex_name}")
        return None
    
    results = {}
    
    # Analyze each descriptor
    for descriptor_name, (time, values) in complex_data.items():
        print(f"\n  Processing: {descriptor_name}")
        
        # Select equilibrated region
        time_eq, values_eq = stats.select_equilibrated_region(time, values)
        
        # Block averaging
        block_time, block_means, block_stds, block_sems = stats.block_average(
            time_eq, values_eq
        )
        
        print(f"    • Blocks: {len(block_means)}")
        print(f"    • Block size: {config.BLOCK_SIZE_NS} ns")
        print(f"    • Mean: {np.mean(block_means):.6f}")
        
        # Descriptive statistics
        desc_stats = stats.descriptive_statistics(block_means)
        
        # Bootstrap CI
        bootstrap_results = stats.bootstrap_ci(block_means)
        
        # Effective sample size
        ess_results = stats.effective_sample_size(block_means, time_array=block_time)
        
        # Trend analysis
        trend_results = stats.linear_trend_analysis(block_time, block_means)
        
        # Convergence test
        convergence_results = stats.convergence_test(time_eq, values_eq)
        
        # Store results
        results[descriptor_name] = {
            'time_raw': time,
            'values_raw': values,
            'time_eq': time_eq,
            'values_eq': values_eq,
            'block_time': block_time,
            'block_means': block_means,
            'block_stds': block_stds,
            'block_sems': block_sems,
            'descriptive': desc_stats,
            'bootstrap': bootstrap_results,
            'ess': ess_results,
            'trend': trend_results,
            'convergence': convergence_results,
        }
    
    return results


def generate_figures_for_complex(complex_name, results):
    """
    Generate all publication-quality figures for a complex.
    
    Parameters
    ----------
    complex_name : str
        Name of complex
    results : dict
        Analysis results from analyze_complex()
    """
    print(f"\n2. Generating figures for {complex_name}...")
    
    # Create complex-specific figure directory
    complex_fig_dir = plotting.config.FIGURES_DIR / complex_name
    complex_fig_dir.mkdir(parents=True, exist_ok=True)
    
    for descriptor_name, data in results.items():
        # Time series plot
        fig, ax = plotting.plot_time_series(
            data['time_eq'],
            data['values_eq'],
            data['block_time'],
            data['block_means'],
            descriptor_name=descriptor_name
        )
        plotting.save_figure(fig, complex_fig_dir / f"{descriptor_name}_timeseries")
        plotting.plt.close(fig)
        
        # Bootstrap distribution
        bootstrap = data['bootstrap']
        fig, ax = plotting.plot_bootstrap_distribution(
            bootstrap['bootstrap_samples'],
            bootstrap['mean'],
            bootstrap[f'ci_lower_{config.BOOTSTRAP_CI}'],
            bootstrap[f'ci_upper_{config.BOOTSTRAP_CI}'],
            descriptor_name=descriptor_name
        )
        plotting.save_figure(fig, complex_fig_dir / f"{descriptor_name}_bootstrap")
        plotting.plt.close(fig)
        
        # Autocorrelation plot
        ess = data['ess']
        fig, ax = plotting.plot_autocorrelation(
            ess['lags_ns'],
            ess['acf'],
            descriptor_name=descriptor_name
        )
        plotting.save_figure(fig, complex_fig_dir / f"{descriptor_name}_autocorr")
        plotting.plt.close(fig)
        
        # Trend analysis plot
        trend = data['trend']
        fig, ax = plotting.plot_trend_analysis(
            data['block_time'],
            data['block_means'],
            trend['slope'],
            trend['intercept'],
            trend['r_squared'],
            trend['p_value'],
            descriptor_name=descriptor_name
        )
        plotting.save_figure(fig, complex_fig_dir / f"{descriptor_name}_trend")
        plotting.plt.close(fig)
        
        # Convergence windows
        fig, ax = plotting.plot_convergence_windows(
            data['time_eq'],
            data['values_eq'],
            config.CONVERGENCE_WINDOWS
        )
        plotting.save_figure(fig, complex_fig_dir / f"{descriptor_name}_convergence")
        plotting.plt.close(fig)


def generate_comparison_figures(all_results):
    """
    Generate comparison figures across complexes.
    
    Parameters
    ----------
    all_results : dict
        Results for all complexes
    """
    print(f"\n3. Generating comparison figures...")
    
    # Get all descriptors
    descriptors = list(all_results[config.COMPLEXES[0]].keys())
    
    for descriptor_name in descriptors:
        # Collect data across complexes
        data_dict = {}
        summary_dict = {}
        
        for complex_name in config.COMPLEXES:
            if complex_name in all_results:
                data = all_results[complex_name][descriptor_name]
                data_dict[complex_name] = data['block_means']
                
                summary_dict[complex_name] = {
                    'mean': data['descriptive']['mean'],
                    'ci_lower': data['bootstrap'][f'ci_lower_{config.BOOTSTRAP_CI}'],
                    'ci_upper': data['bootstrap'][f'ci_upper_{config.BOOTSTRAP_CI}'],
                    'cv': data['descriptive']['cv'],
                    'n_eff': data['ess']['n_effective'],
                    'converged': not data['trend']['significant'],
                }
        
        # Distribution plots
        fig = plotting.plot_distributions(
            data_dict,
            descriptor_name=descriptor_name
        )
        plotting.save_figure(fig, f"01_distributions_{descriptor_name}")
        plotting.plt.close(fig)
        
        # Comparison plot
        fig = plotting.plot_complex_comparison(
            summary_dict,
            descriptor_name=descriptor_name
        )
        plotting.save_figure(fig, f"02_comparison_{descriptor_name}")
        plotting.plt.close(fig)


def export_all_results(all_results):
    """
    Export all results to Excel, CSV, and other formats.
    
    Parameters
    ----------
    all_results : dict
        Results for all complexes
    """
    print(f"\n4. Exporting results...")
    
    # Summary statistics
    export.export_summary_statistics(all_results)
    
    # Bootstrap results
    export.export_bootstrap_results(all_results)
    
    # Effective sample size
    export.export_effective_sample_size(all_results)
    
    # Trend analysis
    export.export_trend_analysis(all_results)
    
    # Convergence analysis
    export.export_convergence_analysis(all_results)
    
    # Publication table
    export.export_publication_table(all_results, output_format='both')
    
    # Markdown tables
    export.export_markdown_table(all_results)
    
    # Block-averaged data
    export.export_block_averaged_data(all_results)


def print_summary(all_results):
    """
    Print comprehensive summary to console and file.
    
    Parameters
    ----------
    all_results : dict
        Results for all complexes
    """
    print(f"\n\n{'='*70}")
    print("ANALYSIS SUMMARY")
    print(f"{'='*70}")
    
    summary_file = config.OUTPUT_DIR / "analysis_summary.txt"
    
    with open(summary_file, 'w') as f:
        f.write("="*70 + "\n")
        f.write("MD SIMULATION ANALYSIS RESULTS\n")
        f.write("="*70 + "\n\n")
        
        for complex_name in config.COMPLEXES:
            if complex_name not in all_results:
                continue
            
            f.write(f"\n{complex_name.upper()}\n")
            f.write("-" * 70 + "\n")
            print(f"\n{complex_name.upper()}")
            
            descriptors = all_results[complex_name]
            
            for desc_name, data in descriptors.items():
                desc_stat = data['descriptive']
                bootstrap = data['bootstrap']
                ess = data['ess']
                trend = data['trend']
                
                output = (
                    f"\n  {desc_name}:\n"
                    f"    Mean ± SD:        {desc_stat['mean']:.6f} ± {desc_stat['std']:.6f}\n"
                    f"    95% CI:           [{bootstrap['ci_lower_95']:.6f}, {bootstrap['ci_upper_95']:.6f}]\n"
                    f"    CV:               {desc_stat['cv']:.2f}%\n"
                    f"    Neff:             {ess['n_effective']:.0f} (efficiency: {ess['efficiency']:.1f}%)\n"
                    f"    Trend slope:      {trend['slope']:.2e} (R² = {trend['r_squared']:.4f})\n"
                    f"    Converged:        {'Yes' if not trend['significant'] else 'No'}\n"
                )
                
                print(output)
                f.write(output)
    
    print(f"\n✓ Summary saved to {summary_file.name}")


def main():
    """Main execution function."""
    
    start_time = time.time()
    
    print("\n" + "="*70)
    print("MD SIMULATION ANALYSIS PIPELINE")
    print("="*70)
    print(f"\nConfiguration:")
    print(f"  Project root: {config.PROJECT_ROOT}")
    print(f"  Complexes: {', '.join(config.COMPLEXES)}")
    print(f"  Block size: {config.BLOCK_SIZE_NS} ns")
    print(f"  Equilibration: {config.EQUILIBRATION_NS} ns")
    print(f"  Output directory: {config.OUTPUT_DIR}")
    
    # Create output directories
    config.create_directories()
    
    # Analyze all complexes
    all_results = {}
    for complex_name in config.COMPLEXES:
        try:
            results = analyze_complex(complex_name)
            if results:
                all_results[complex_name] = results
                
                # Generate figures for this complex
                generate_figures_for_complex(complex_name, results)
        
        except Exception as e:
            print(f"\n✗ Error analyzing {complex_name}: {e}")
            if config.VERBOSE >= 2:
                import traceback
                traceback.print_exc()
            # Continue with next complex instead of stopping
            continue
    
    if not all_results:
        print("\n✗ No results generated. Check configuration and file paths.")
        return
    
    # Generate comparison figures
    try:
        generate_comparison_figures(all_results)
    except Exception as e:
        print(f"\n✗ Error generating comparison figures: {e}")
        if config.VERBOSE >= 2:
            import traceback
            traceback.print_exc()
    
    # Export results
    try:
        export_all_results(all_results)
    except Exception as e:
        print(f"\n✗ Error exporting results: {e}")
        if config.VERBOSE >= 2:
            import traceback
            traceback.print_exc()
    
    # Print summary
    try:
        print_summary(all_results)
    except Exception as e:
        print(f"\n✗ Error printing summary: {e}")
    
    # Final report
    elapsed_time = time.time() - start_time
    
    print(f"\n{'='*70}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*70}")
    print(f"Time elapsed: {elapsed_time:.1f} seconds ({elapsed_time/60:.1f} minutes)")
    print(f"\nOutput files saved to:")
    print(f"  Figures: {config.FIGURES_DIR}")
    print(f"  Tables: {config.TABLES_DIR}")
    print(f"  Data: {config.DATA_DIR}")
    print(f"\nKey output files:")
    print(f"  • summary_statistics.xlsx")
    print(f"  • bootstrap_results.xlsx")
    print(f"  • effective_sample_size.xlsx")
    print(f"  • trend_analysis.xlsx")
    print(f"  • convergence_analysis.xlsx")
    print(f"  • publication_table.xlsx / .csv")
    print(f"  • tables_markdown.md (for Word/presentations)")
    print(f"  • analysis_summary.txt")
    print()


if __name__ == "__main__":
    main()