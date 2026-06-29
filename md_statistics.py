"""
MD Statistics Module
Core statistical functions for molecular dynamics analysis
"""

import numpy as np
import pandas as pd
from pathlib import Path
from scipy import stats, signal
import warnings

import config

# ============================================================================
# XVG FILE READING
# ============================================================================

def read_xvg(filepath):
    """
    Read GROMACS .xvg file, skipping comments and headers.
    
    Parameters
    ----------
    filepath : str or Path
        Path to .xvg file
        
    Returns
    -------
    tuple
        (time_array, value_array) in ns and native units
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    times = []
    values = []

    # Détection automatique de l'unité
    time_unit = "ps"   # valeur par défaut

    try:
        with open(filepath, 'r') as f:
            for line in f:

                # Détecter l'unité dans l'en-tête
                if line.startswith("@") and "Time" in line:
                    if "(ns)" in line:
                        time_unit = "ns"
                    elif "(ps)" in line:
                        time_unit = "ps"

                # Ignorer les commentaires
                if line.startswith('#') or line.startswith('@'):
                    continue

                # Lire les données
                parts = line.strip().split()
                if len(parts) >= 2:
                    try:
                        times.append(float(parts[0]))
                        values.append(float(parts[1]))
                    except ValueError:
                        continue
    except Exception as e:
        raise ValueError(f"Error reading {filepath}: {e}")
    
    if len(times) == 0:
        raise ValueError(f"No data found in {filepath}")
    
    # Convert time to nanoseconds (assuming input in picoseconds)
    times = np.array(times)

    if time_unit == "ps":
        times = times / 1000.0
    
    values = np.array(values)
    
    return times, values


def load_complex_data(complex_name, xvg_files=None):
    """
    Load all XVG files for a complex.
    
    Parameters
    ----------
    complex_name : str
        Name of the complex folder
    xvg_files : dict, optional
        Dictionary of descriptor names and filenames
        
    Returns
    -------
    dict
        Dictionary of {descriptor: (time, values)}
    """
    if xvg_files is None:
        xvg_files = config.XVG_FILES
    
    complex_dir = config.PROJECT_ROOT / complex_name
    data = {}
    
    for descriptor, filename in xvg_files.items():
        filepath = complex_dir / filename
        try:
            time, values = read_xvg(filepath)
            data[descriptor] = (time, values)
            if config.VERBOSE >= 1:
                print(f"  ✓ Loaded {complex_name}/{filename} ({len(values)} points)")
        except Exception as e:
            print(f"  ✗ Error loading {complex_name}/{filename}: {e}")
    
    return data


# ============================================================================
# DATA FILTERING & EQUILIBRATION
# ============================================================================

def select_equilibrated_region(time, values):
    """
    Select data after equilibration period.
    
    Parameters
    ----------
    time : ndarray
        Time array (ns)
    values : ndarray
        Data values
        
    Returns
    -------
    tuple
        (filtered_time, filtered_values)
    """
    mask = time >= config.EQUILIBRATION_NS
    time_eq = time[mask]
    values_eq = values[mask]
    
    # Count and report NaN values
    nan_count = np.sum(np.isnan(values_eq))
    if nan_count > 0 and config.VERBOSE >= 1:
        print(f"      Found {nan_count} NaN values in equilibrated region")
    
    return time_eq, values_eq


# ============================================================================
# BLOCK AVERAGING
# ============================================================================

def block_average(time, values, block_size_ns=None):
    """
    Perform block averaging on time series data.
    
    Parameters
    ----------
    time : ndarray
        Time array (ns)
    values : ndarray
        Data values
    block_size_ns : float, optional
        Block size in nanoseconds
        
    Returns
    -------
    tuple
        (block_time, block_means, block_stds, block_sems)
    """
    if block_size_ns is None:
        block_size_ns = config.BLOCK_SIZE_NS
    
    # Remove NaN values
    valid_mask = ~np.isnan(values)
    if np.sum(valid_mask) == 0:
        raise ValueError("All values are NaN")
    
    if config.VERBOSE >= 1:
        nan_count = len(values) - np.sum(valid_mask)
        if nan_count > 0:
            print(f"      Removed {nan_count} NaN values")
    
    time = time[valid_mask]
    values = values[valid_mask]
    
    # Calculate points per block
    time_diffs = np.diff(time)
    time_diffs = time_diffs[~np.isnan(time_diffs)]
    
    if len(time_diffs) == 0:
        raise ValueError("Cannot calculate time step from data")
    
    dt = np.mean(time_diffs)
    
    if np.isnan(dt) or dt <= 0:
        raise ValueError(f"Invalid time step: {dt}")
    
    points_per_block = int(np.round(block_size_ns / dt))
    
    if points_per_block < 1:
        points_per_block = 1
    
    # Check for sufficient blocks
    n_blocks = len(values) // points_per_block
    if n_blocks < config.MIN_BLOCKS:
        warnings.warn(
            f"Only {n_blocks} blocks created (minimum {config.MIN_BLOCKS} recommended). "
            f"Consider smaller block size or longer trajectory."
        )
    
    # Perform block averaging
    block_times = []
    block_means = []
    block_stds = []
    block_sems = []
    
    for i in range(n_blocks):
        start_idx = i * points_per_block
        end_idx = (i + 1) * points_per_block
        
        block_values = values[start_idx:end_idx]
        block_time = np.mean(time[start_idx:end_idx])
        
        block_times.append(block_time)
        block_means.append(np.mean(block_values))
        block_stds.append(np.std(block_values, ddof=1))
        block_sems.append(stats.sem(block_values))
    
    return (
        np.array(block_times),
        np.array(block_means),
        np.array(block_stds),
        np.array(block_sems)
    )


# ============================================================================
# DESCRIPTIVE STATISTICS
# ============================================================================

def descriptive_statistics(values):
    """
    Calculate comprehensive descriptive statistics.
    
    Parameters
    ----------
    values : ndarray
        Data array (typically block means)
        
    Returns
    -------
    dict
        Dictionary of statistics
    """
    # Remove any NaN values
    values_clean = values[~np.isnan(values)]
    
    if len(values_clean) == 0:
        raise ValueError("All values are NaN - cannot calculate statistics")
    
    return {
        'mean': np.mean(values_clean),
        'median': np.median(values_clean),
        'std': np.std(values_clean, ddof=1),
        'sem': stats.sem(values_clean),
        'min': np.min(values_clean),
        'max': np.max(values_clean),
        'q25': np.percentile(values_clean, 25),
        'q75': np.percentile(values_clean, 75),
        'iqr': np.percentile(values_clean, 75) - np.percentile(values_clean, 25),
        'cv': (np.std(values_clean, ddof=1) / np.mean(values_clean)) * 100 if np.mean(values_clean) != 0 else 0,
    }


# ============================================================================
# BOOTSTRAP CONFIDENCE INTERVALS
# ============================================================================

def bootstrap_ci(data, n_bootstrap=None, ci=None, method='bca'):
    """
    Calculate bootstrap confidence intervals.
    
    Parameters
    ----------
    data : ndarray
        Input data array (typically block means)
    n_bootstrap : int, optional
        Number of bootstrap samples
    ci : float, optional
        Confidence interval percentage (e.g., 95)
    method : str
        'bca' (bias-corrected and accelerated) or 'percentile'
        
    Returns
    -------
    dict
        Bootstrap statistics including CI bounds
    """
    if n_bootstrap is None:
        n_bootstrap = config.N_BOOTSTRAP
    if ci is None:
        ci = config.BOOTSTRAP_CI
    
    # Remove NaN values
    data = data[~np.isnan(data)]
    
    if len(data) < 2:
        raise ValueError(f"Insufficient data for bootstrap (n={len(data)})")
    
    # Calculate original statistic
    original_mean = np.mean(data)
    
    # Generate bootstrap samples
    bootstrap_means = []
    np.random.seed(42)  # For reproducibility
    
    for _ in range(n_bootstrap):
        sample = np.random.choice(data, size=len(data), replace=True)
        bootstrap_means.append(np.mean(sample))
    
    bootstrap_means = np.array(bootstrap_means)
    
    # Calculate percentiles
    alpha = 100 - ci
    lower_percentile = alpha / 2
    upper_percentile = 100 - alpha / 2
    
    if method == 'percentile':
        ci_lower = np.percentile(bootstrap_means, lower_percentile)
        ci_upper = np.percentile(bootstrap_means, upper_percentile)
    
    elif method == 'bca':
        # Bias-corrected and accelerated bootstrap
        # Bias correction
        z0 = stats.norm.ppf(np.mean(bootstrap_means < original_mean))
        
        # Jackknife acceleration
        jack_means = []
        for i in range(len(data)):
            jack_sample = np.delete(data, i)
            jack_means.append(np.mean(jack_sample))
        
        jack_means = np.array(jack_means)
        jack_mean_all = np.mean(jack_means)
        
        numerator = np.sum((jack_mean_all - jack_means) ** 3)
        denominator = 6 * (np.sum((jack_mean_all - jack_means) ** 2) ** 1.5)
        
        acceleration = numerator / denominator if denominator != 0 else 0
        
        # BCa adjusted percentiles
        z_lower = stats.norm.ppf(lower_percentile / 100)
        z_upper = stats.norm.ppf(upper_percentile / 100)
        
        p_lower = stats.norm.cdf(
            z0 + (z0 + z_lower) / (1 - acceleration * (z0 + z_lower))
        )
        p_upper = stats.norm.cdf(
            z0 + (z0 + z_upper) / (1 - acceleration * (z0 + z_upper))
        )
        
        ci_lower = np.percentile(bootstrap_means, p_lower * 100)
        ci_upper = np.percentile(bootstrap_means, p_upper * 100)
    
    else:
        raise ValueError(f"Unknown method: {method}")
    
    return {
        'mean': original_mean,
        'bootstrap_mean': np.mean(bootstrap_means),
        'bootstrap_std': np.std(bootstrap_means, ddof=1),
        f'ci_lower_{ci}': ci_lower,
        f'ci_upper_{ci}': ci_upper,
        'ci_width': ci_upper - ci_lower,
        'bootstrap_samples': bootstrap_means,
        'method': method,
    }


# ============================================================================
# AUTOCORRELATION & EFFECTIVE SAMPLE SIZE
# ============================================================================

def autocorrelation_function(values, max_lag_ns=None, time_array=None):
    """
    Calculate autocorrelation function.
    
    Parameters
    ----------
    values : ndarray
        Data array (typically block means)
    max_lag_ns : float, optional
        Maximum lag in nanoseconds
    time_array : ndarray, optional
        Time array (ns) for lag calculation
        
    Returns
    -------
    tuple
        (lags_ns, acf_values)
    """
    if max_lag_ns is None:
        max_lag_ns = config.MAX_LAG_NS
    
    # Normalize data
    centered = values - np.mean(values)
    
    # Calculate ACF using FFT (faster for large arrays)
    if config.AUTOCORR_METHOD == 'fft':
        fft = np.fft.fft(centered, n=2*len(centered))
        power = np.abs(fft) ** 2
        acf = np.fft.ifft(power).real[:len(centered)] / np.dot(centered, centered)
    else:
        # Direct calculation
        acf = np.correlate(centered, centered, mode='full')
        acf = acf[len(acf)//2:] / acf[len(acf)//2]
    
    # Normalize
    acf = acf / acf[0]
    
    # Convert to nanoseconds if time array provided
    if time_array is not None:
        dt = np.mean(np.diff(time_array))
        max_lag_points = int(max_lag_ns / dt)
        max_lag_points = min(max_lag_points, len(acf) - 1)
        acf = acf[:max_lag_points + 1]
        lags_ns = np.arange(len(acf)) * dt
    else:
        lags_ns = np.arange(len(acf))
    
    return lags_ns, acf


def effective_sample_size(values, time_array=None):
    """
    Calculate effective sample size (Neff) from autocorrelation.
    
    Parameters
    ----------
    values : ndarray
        Data array (typically block means)
    time_array : ndarray, optional
        Time array (ns)
        
    Returns
    -------
    dict
        ESS statistics including Neff
    """
    n_total = len(values)
    
    # Calculate autocorrelation
    lags_ns, acf = autocorrelation_function(values, time_array=time_array)
    
    # Integrated autocorrelation time
    # Sum ACF until it becomes negligible
    tau_int = 0.5  # Start with self-correlation
    
    for i in range(1, len(acf)):
        if acf[i] < 0.05:  # Stop when ACF drops below 5%
            break
        tau_int += acf[i]
    
    # Effective sample size
    n_eff = n_total / (2 * tau_int) if tau_int > 0 else n_total
    n_eff = max(1, n_eff)  # Ensure at least 1
    
    # Corrected standard error
    sem_original = stats.sem(values)
    sem_corrected = sem_original * np.sqrt(n_total / n_eff)
    
    # Corrected 95% CI
    ci_width_corrected = 1.96 * sem_corrected
    
    return {
        'n_total': n_total,
        'tau_integrated': tau_int,
        'n_effective': n_eff,
        'efficiency': (n_eff / n_total) * 100,
        'sem_uncorrected': sem_original,
        'sem_corrected': sem_corrected,
        'ci_width_95_uncorrected': 1.96 * sem_original,
        'ci_width_95_corrected': ci_width_corrected,
        'acf': acf,
        'lags_ns': lags_ns,
    }


# ============================================================================
# TREND ANALYSIS
# ============================================================================

def linear_trend_analysis(time, values):
    """
    Perform linear trend analysis on time series.
    
    Parameters
    ----------
    time : ndarray
        Time array (ns)
    values : ndarray
        Data values
        
    Returns
    -------
    dict
        Trend statistics including slope, intercept, R², p-value
    """
    # Linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(time, values)
    
    # Calculate residuals
    y_pred = slope * time + intercept
    residuals = values - y_pred
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((values - np.mean(values)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    
    return {
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_squared,
        'r_value': r_value,
        'p_value': p_value,
        'std_err': std_err,
        'significant': p_value < config.TREND_P_VALUE_THRESHOLD,
        'y_pred': y_pred,
        'residuals': residuals,
    }


# ============================================================================
# CONVERGENCE TESTING
# ============================================================================

def convergence_test(time, values, windows=None):
    """
    Test convergence by comparing statistics across time windows.
    
    Parameters
    ----------
    time : ndarray
        Time array (ns)
    values : ndarray
        Data values
    windows : dict, optional
        Dictionary of {name: (t_start, t_end)} time ranges
        
    Returns
    -------
    dict
        Convergence test results
    """
    if windows is None:
        windows = config.CONVERGENCE_WINDOWS
    
    window_stats = {}
    window_data = {}
    
    # Extract data for each window
    for window_name, (t_start, t_end) in windows.items():
        mask = (time >= t_start) & (time <= t_end)
        window_vals = values[mask]
        
        if len(window_vals) > 0:
            window_data[window_name] = window_vals
            window_stats[window_name] = {
                'n': len(window_vals),
                'mean': np.mean(window_vals),
                'std': np.std(window_vals, ddof=1),
                'sem': stats.sem(window_vals),
                'min': np.min(window_vals),
                'max': np.max(window_vals),
            }
    
    # Statistical tests between windows
    test_results = {}
    window_names = list(window_data.keys())
    
    if len(window_names) >= 2:
        # Perform t-tests between consecutive windows
        for i in range(len(window_names) - 1):
            name1 = window_names[i]
            name2 = window_names[i + 1]
            
            t_stat, p_val = stats.ttest_ind(window_data[name1], window_data[name2])
            
            test_results[f"{name1}_vs_{name2}"] = {
                't_statistic': t_stat,
                'p_value': p_val,
                'converged': p_val > config.CONVERGENCE_P_THRESHOLD,
            }
    
    return {
        'window_statistics': window_stats,
        'statistical_tests': test_results,
    }


# ============================================================================
# SUMMARY STATISTICS TABLE
# ============================================================================

def create_statistics_summary(descriptor_name, raw_values, block_means, block_time):
    """
    Create comprehensive summary statistics for a descriptor.
    
    Parameters
    ----------
    descriptor_name : str
        Name of the descriptor
    raw_values : ndarray
        Raw (non-blocked) data
    block_means : ndarray
        Block-averaged means
    block_time : ndarray
        Block time points
        
    Returns
    -------
    pd.DataFrame
        Summary statistics table
    """
    # Descriptive statistics
    desc_stats = descriptive_statistics(block_means)
    
    # Bootstrap CI
    bootstrap = bootstrap_ci(block_means)
    
    # ESS
    ess = effective_sample_size(block_means, time_array=block_time)
    
    # Trend
    trend = linear_trend_analysis(block_time, block_means)
    
    # Create DataFrame
    summary = pd.DataFrame({
        'Descriptor': [descriptor_name],
        'Mean': [desc_stats['mean']],
        'Median': [desc_stats['median']],
        'SD': [desc_stats['std']],
        'SEM': [desc_stats['sem']],
        'CV (%)': [desc_stats['cv']],
        'Min': [desc_stats['min']],
        'Max': [desc_stats['max']],
        'IQR': [desc_stats['iqr']],
        '95% CI Lower': [bootstrap[f'ci_lower_{config.BOOTSTRAP_CI}']],
        '95% CI Upper': [bootstrap[f'ci_upper_{config.BOOTSTRAP_CI}']],
        'Neff': [ess['n_effective']],
        'Efficiency (%)': [ess['efficiency']],
        'Trend Slope': [trend['slope']],
        'Trend R²': [trend['r_squared']],
        'Trend p-value': [trend['p_value']],
        'Converged': [trend['significant'] == False],  # No trend = convergence
    })
    
    return summary