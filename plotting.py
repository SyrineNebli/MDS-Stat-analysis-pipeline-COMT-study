"""
Plotting Module
Publication-quality figures for molecular dynamics analysis
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import seaborn as sns
from pathlib import Path

import config

# Set style
if config.PLOT_STYLE:
    try:
        plt.style.use(config.PLOT_STYLE)
    except:
        pass

sns.set_palette(config.COLOR_PALETTE)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def setup_figure(figsize=None, dpi=None):
    """Create figure with consistent styling."""
    if figsize is None:
        figsize = config.FIGSIZE_SINGLE
    if dpi is None:
        dpi = config.DPI
    
    fig = plt.figure(figsize=figsize, dpi=dpi)
    return fig


def save_figure(fig, filename, formats=None):
    """Save figure in specified formats."""
    if formats is None:
        if config.FIGURE_FORMAT == 'both':
            formats = ['png', 'pdf']
        else:
            formats = [config.FIGURE_FORMAT]
    
    for fmt in formats:
        filepath = config.FIGURES_DIR / f"{filename}.{fmt}"
        fig.savefig(filepath, dpi=config.DPI, bbox_inches='tight')
        if config.VERBOSE >= 1:
            print(f"  ✓ Saved {filepath.name}")


# ============================================================================
# TIME SERIES PLOTS
# ============================================================================

def plot_time_series(time, values, block_time=None, block_means=None, 
                     descriptor_name="Descriptor", unit=""):
    """
    Plot raw time series with optional block averages and trend.
    
    Parameters
    ----------
    time : ndarray
        Time array (ns)
    values : ndarray
        Raw values
    block_time : ndarray, optional
        Block time points
    block_means : ndarray, optional
        Block means
    descriptor_name : str
        Name for plotting
    unit : str
        Units for y-axis
    """
    fig, ax = plt.subplots(figsize=config.FIGSIZE_SINGLE)
    
    # Plot raw data
    ax.plot(time, values, 'o-', alpha=0.5, markersize=3, 
            label='Raw data', color='steelblue')
    
    # Plot block averages
    if block_time is not None and block_means is not None:
        ax.plot(block_time, block_means, 's-', alpha=0.8, markersize=6,
                label=f'Block averaged ({config.BLOCK_SIZE_NS} ns)',
                color='darkred', linewidth=2)
    
    # Add equilibration line
    ax.axvline(config.EQUILIBRATION_NS, color='gray', linestyle='--', 
               linewidth=2, alpha=0.7, label='Equilibration cutoff')
    
    ax.set_xlabel('Time (ns)', fontsize=config.FONTSIZE_LABEL)
    ax.set_ylabel(f'{descriptor_name} {unit}', fontsize=config.FONTSIZE_LABEL)
    ax.set_title(f'{descriptor_name} vs Time', fontsize=config.FONTSIZE_TITLE)
    ax.legend(fontsize=config.FONTSIZE_LEGEND)
    ax.grid(True, alpha=0.3)
    
    return fig, ax


# ============================================================================
# DISTRIBUTION PLOTS
# ============================================================================

def plot_distributions(data_dict, descriptor_name="Descriptor", unit=""):
    """
    Create comprehensive distribution plots (boxplot, violin, histogram).
    
    Parameters
    ----------
    data_dict : dict
        Dictionary of {complex_name: values}
    descriptor_name : str
        Name of descriptor
    unit : str
        Units
    """
    complexes = list(data_dict.keys())
    values_list = list(data_dict.values())
    
    fig = plt.figure(figsize=config.FIGSIZE_DOUBLE)
    gs = GridSpec(1, 3, figure=fig)
    
    # Boxplot
    ax1 = fig.add_subplot(gs[0])
    bp = ax1.boxplot(values_list, labels=complexes, patch_artist=True)
    for patch in bp['boxes']:
        patch.set_facecolor('lightblue')
        patch.set_alpha(0.7)
    ax1.set_ylabel(f'{descriptor_name} {unit}', fontsize=config.FONTSIZE_LABEL)
    ax1.set_title('Boxplot', fontsize=config.FONTSIZE_LABEL)
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Violin plot
    ax2 = fig.add_subplot(gs[1])
    parts = ax2.violinplot(values_list, positions=range(len(values_list)),
                            showmeans=True, showmedians=True)
    ax2.set_xticks(range(len(complexes)))
    ax2.set_xticklabels(complexes, rotation=45)
    ax2.set_ylabel(f'{descriptor_name} {unit}', fontsize=config.FONTSIZE_LABEL)
    ax2.set_title('Violin Plot', fontsize=config.FONTSIZE_LABEL)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Histograms
    ax3 = fig.add_subplot(gs[2])
    colors = sns.color_palette(config.COLOR_PALETTE, len(complexes))
    for i, (complex_name, vals) in enumerate(data_dict.items()):
        ax3.hist(vals, alpha=0.5, bins=10, label=complex_name, color=colors[i])
    ax3.set_xlabel(f'{descriptor_name} {unit}', fontsize=config.FONTSIZE_LABEL)
    ax3.set_ylabel('Frequency', fontsize=config.FONTSIZE_LABEL)
    ax3.set_title('Histogram', fontsize=config.FONTSIZE_LABEL)
    ax3.legend(fontsize=config.FONTSIZE_LEGEND-2)
    ax3.grid(True, alpha=0.3)
    
    plt.suptitle(f'{descriptor_name} Distributions', 
                 fontsize=config.FONTSIZE_TITLE, y=1.02)
    plt.tight_layout()
    
    return fig


# ============================================================================
# AUTOCORRELATION PLOTS
# ============================================================================

def plot_autocorrelation(lags_ns, acf, descriptor_name="Descriptor"):
    """
    Plot autocorrelation function with confidence bounds.
    
    Parameters
    ----------
    lags_ns : ndarray
        Lags in nanoseconds
    acf : ndarray
        ACF values
    descriptor_name : str
        Name of descriptor
    """
    fig, ax = plt.subplots(figsize=config.FIGSIZE_SINGLE)
    
    ax.plot(lags_ns, acf, 'o-', color='steelblue', markersize=4, linewidth=2)
    
    # Add 95% confidence bounds (assuming white noise)
    n = len(acf)
    ci_bound = 1.96 / np.sqrt(n)
    ax.axhline(ci_bound, color='red', linestyle='--', alpha=0.5, 
               label='95% CI')
    ax.axhline(-ci_bound, color='red', linestyle='--', alpha=0.5)
    ax.axhline(0, color='black', linestyle='-', alpha=0.3, linewidth=0.5)
    
    ax.set_xlabel('Lag (ns)', fontsize=config.FONTSIZE_LABEL)
    ax.set_ylabel('Autocorrelation', fontsize=config.FONTSIZE_LABEL)
    ax.set_title(f'{descriptor_name} Autocorrelation Function',
                fontsize=config.FONTSIZE_TITLE)
    ax.legend(fontsize=config.FONTSIZE_LEGEND)
    ax.grid(True, alpha=0.3)
    ax.set_ylim([-0.2, 1.05])
    
    return fig, ax


# ============================================================================
# BOOTSTRAP PLOTS
# ============================================================================

def plot_bootstrap_distribution(bootstrap_samples, mean_value, ci_lower, ci_upper,
                                descriptor_name="Descriptor", unit=""):
    """
    Plot bootstrap distribution with CI.
    
    Parameters
    ----------
    bootstrap_samples : ndarray
        Bootstrap sample means
    mean_value : float
        Original mean
    ci_lower : float
        Lower CI bound
    ci_upper : float
        Upper CI bound
    descriptor_name : str
        Name of descriptor
    unit : str
        Units
    """
    fig, ax = plt.subplots(figsize=config.FIGSIZE_SINGLE)
    
    ax.hist(bootstrap_samples, bins=50, alpha=0.7, color='steelblue',
            edgecolor='black', density=True)
    
    # Mark mean and CI
    ax.axvline(mean_value, color='red', linestyle='-', linewidth=2,
              label=f'Mean: {mean_value:.3f}')
    ax.axvline(ci_lower, color='green', linestyle='--', linewidth=2,
              label=f'95% CI: [{ci_lower:.3f}, {ci_upper:.3f}]')
    ax.axvline(ci_upper, color='green', linestyle='--', linewidth=2)
    
    # Shade CI region
    ax.axvspan(ci_lower, ci_upper, alpha=0.2, color='green')
    
    ax.set_xlabel(f'{descriptor_name} {unit}', fontsize=config.FONTSIZE_LABEL)
    ax.set_ylabel('Density', fontsize=config.FONTSIZE_LABEL)
    ax.set_title(f'{descriptor_name} Bootstrap Distribution (n={len(bootstrap_samples)})',
                fontsize=config.FONTSIZE_TITLE)
    ax.legend(fontsize=config.FONTSIZE_LEGEND)
    ax.grid(True, alpha=0.3, axis='y')
    
    return fig, ax


# ============================================================================
# CONFIDENCE INTERVAL PLOTS
# ============================================================================

def plot_confidence_intervals(summary_df, descriptor_col='Descriptor'):
    """
    Plot confidence intervals for multiple complexes/descriptors.
    
    Parameters
    ----------
    summary_df : pd.DataFrame
        Summary statistics from create_statistics_summary
    descriptor_col : str
        Column name for descriptor labels
    """
    fig, ax = plt.subplots(figsize=config.FIGSIZE_SINGLE)
    
    n = len(summary_df)
    means = summary_df['Mean'].values
    ci_lower = summary_df['95% CI Lower'].values
    ci_upper = summary_df['95% CI Upper'].values
    errors = [means - ci_lower, ci_upper - means]
    
    labels = summary_df[descriptor_col].values
    x_pos = np.arange(n)
    
    ax.bar(x_pos, means, alpha=0.7, color='steelblue', edgecolor='black')
    ax.errorbar(x_pos, means, yerr=errors, fmt='none', ecolor='black',
               capsize=5, capthick=2, linewidth=2)
    
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.set_ylabel('Value', fontsize=config.FONTSIZE_LABEL)
    ax.set_title('Means with 95% Bootstrap CI', fontsize=config.FONTSIZE_TITLE)
    ax.grid(True, alpha=0.3, axis='y')
    
    return fig, ax


# ============================================================================
# CONVERGENCE PLOTS
# ============================================================================

def plot_convergence_windows(time, values, windows_dict):
    """
    Plot data with convergence windows highlighted.
    
    Parameters
    ----------
    time : ndarray
        Time array (ns)
    values : ndarray
        Data values
    windows_dict : dict
        Dictionary of {name: (t_start, t_end)}
    """
    fig, ax = plt.subplots(figsize=config.FIGSIZE_SINGLE)
    
    ax.plot(time, values, 'o-', alpha=0.6, markersize=3, color='steelblue')
    
    colors = sns.color_palette(config.COLOR_PALETTE, len(windows_dict))
    for (window_name, (t_start, t_end)), color in zip(windows_dict.items(), colors):
        ax.axvspan(t_start, t_end, alpha=0.2, color=color, label=window_name)
    
    ax.set_xlabel('Time (ns)', fontsize=config.FONTSIZE_LABEL)
    ax.set_ylabel('Value', fontsize=config.FONTSIZE_LABEL)
    ax.set_title('Convergence Test Windows', fontsize=config.FONTSIZE_TITLE)
    ax.legend(fontsize=config.FONTSIZE_LEGEND)
    ax.grid(True, alpha=0.3)
    
    return fig, ax


# ============================================================================
# TREND ANALYSIS PLOTS
# ============================================================================

def plot_trend_analysis(time, values, slope, intercept, r_squared, p_value,
                       descriptor_name="Descriptor", unit=""):
    """
    Plot data with linear trend line.
    
    Parameters
    ----------
    time : ndarray
        Time array (ns)
    values : ndarray
        Data values
    slope : float
        Regression slope
    intercept : float
        Regression intercept
    r_squared : float
        R² value
    p_value : float
        Statistical p-value
    descriptor_name : str
        Name of descriptor
    unit : str
        Units
    """
    fig, ax = plt.subplots(figsize=config.FIGSIZE_SINGLE)
    
    ax.scatter(time, values, alpha=0.6, s=30, color='steelblue',
              edgecolor='black', linewidth=0.5)
    
    # Trend line
    y_trend = slope * time + intercept
    ax.plot(time, y_trend, 'r-', linewidth=2,
           label=f'Trend: y = {slope:.6f}x + {intercept:.3f}')
    
    # Statistics text
    textstr = f'R² = {r_squared:.4f}\np-value = {p_value:.4e}'
    if p_value < config.TREND_P_VALUE_THRESHOLD:
        textstr += '\nSignificant trend'
        color_box = 'red'
    else:
        textstr += '\nNo significant trend'
        color_box = 'green'
    
    props = dict(boxstyle='round', facecolor=color_box, alpha=0.3)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=10,
           verticalalignment='top', bbox=props)
    
    ax.set_xlabel('Time (ns)', fontsize=config.FONTSIZE_LABEL)
    ax.set_ylabel(f'{descriptor_name} {unit}', fontsize=config.FONTSIZE_LABEL)
    ax.set_title(f'{descriptor_name} Trend Analysis', fontsize=config.FONTSIZE_TITLE)
    ax.legend(fontsize=config.FONTSIZE_LEGEND)
    ax.grid(True, alpha=0.3)
    
    return fig, ax


# ============================================================================
# CORRELATION HEATMAP
# ============================================================================

def plot_correlation_heatmap(data_df, descriptor_names):
    """
    Plot correlation matrix heatmap for multiple descriptors.
    
    Parameters
    ----------
    data_df : pd.DataFrame
        DataFrame with descriptor columns
    descriptor_names : list
        Names of descriptor columns to correlate
    """
    # Extract relevant columns
    corr_data = data_df[descriptor_names]
    corr_matrix = corr_data.corr()
    
    fig, ax = plt.subplots(figsize=(8, 7))
    
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm',
               center=0, vmin=-1, vmax=1, square=True, ax=ax,
               cbar_kws={'label': 'Correlation coefficient'},
               linewidths=1, linecolor='white')
    
    ax.set_title('Descriptor Correlation Matrix', fontsize=config.FONTSIZE_TITLE)
    plt.tight_layout()
    
    return fig, ax


# ============================================================================
# COMPARISON PLOTS
# ============================================================================

def plot_complex_comparison(summary_dict, descriptor_name=""):
    """
    Compare a descriptor across all complexes.
    
    Parameters
    ----------
    summary_dict : dict
        Dictionary of {complex: summary_stats}
    descriptor_name : str
        Name of descriptor being compared
    """
    fig, axes = plt.subplots(2, 2, figsize=config.FIGSIZE_DOUBLE)
    
    complexes = list(summary_dict.keys())
    
    # Means with CI
    ax = axes[0, 0]
    means = [summary_dict[c]['mean'] for c in complexes]
    ci_lower = [summary_dict[c]['ci_lower'] for c in complexes]
    ci_upper = [summary_dict[c]['ci_upper'] for c in complexes]
    errors = [np.array(means) - np.array(ci_lower), 
              np.array(ci_upper) - np.array(means)]
    
    x_pos = np.arange(len(complexes))
    ax.bar(x_pos, means, alpha=0.7, color='steelblue', edgecolor='black')
    ax.errorbar(x_pos, means, yerr=errors, fmt='none', ecolor='black',
               capsize=5, capthick=2)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(complexes, rotation=45)
    ax.set_ylabel('Mean Value', fontsize=config.FONTSIZE_LABEL)
    ax.set_title('Means with 95% CI', fontsize=config.FONTSIZE_LABEL)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Coefficient of variation
    ax = axes[0, 1]
    cvs = [summary_dict[c]['cv'] for c in complexes]
    ax.bar(x_pos, cvs, alpha=0.7, color='coral', edgecolor='black')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(complexes, rotation=45)
    ax.set_ylabel('CV (%)', fontsize=config.FONTSIZE_LABEL)
    ax.set_title('Coefficient of Variation', fontsize=config.FONTSIZE_LABEL)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Effective sample size
    ax = axes[1, 0]
    n_effs = [summary_dict[c]['n_eff'] for c in complexes]
    ax.bar(x_pos, n_effs, alpha=0.7, color='lightgreen', edgecolor='black')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(complexes, rotation=45)
    ax.set_ylabel('Neff', fontsize=config.FONTSIZE_LABEL)
    ax.set_title('Effective Sample Size', fontsize=config.FONTSIZE_LABEL)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Convergence indicator
    ax = axes[1, 1]
    converged = [1 if summary_dict[c]['converged'] else 0 for c in complexes]
    colors_conv = ['green' if c else 'red' for c in converged]
    ax.bar(x_pos, [1]*len(complexes), alpha=0.7, color=colors_conv, 
          edgecolor='black')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(complexes, rotation=45)
    ax.set_ylim([0, 1.2])
    ax.set_yticks([])
    ax.set_title('Convergence Status', fontsize=config.FONTSIZE_LABEL)
    
    plt.suptitle(f'{descriptor_name} Comparison Across Complexes',
                fontsize=config.FONTSIZE_TITLE, y=1.00)
    plt.tight_layout()
    
    return fig
