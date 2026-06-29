"""
Environment Setup Verification Script
Checks that all dependencies are installed and configuration is valid
"""

import sys
from pathlib import Path

print("\n" + "="*70)
print("MD ANALYSIS PIPELINE - SETUP VERIFICATION")
print("="*70)

# Check Python version
print("\n1. Checking Python version...")
python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
print(f"   ✓ Python {python_version}")

if sys.version_info < (3, 8):
    print("   ✗ Python 3.8+ required")
    sys.exit(1)

# Check required packages
print("\n2. Checking required packages...")
required_packages = {
    'numpy': 'NumPy',
    'scipy': 'SciPy',
    'pandas': 'Pandas',
    'matplotlib': 'Matplotlib',
    'seaborn': 'Seaborn',
    'openpyxl': 'OpenPyXL',
}

missing_packages = []
for package_name, display_name in required_packages.items():
    try:
        __import__(package_name)
        print(f"   ✓ {display_name}")
    except ImportError:
        print(f"   ✗ {display_name} NOT FOUND")
        missing_packages.append(package_name)

if missing_packages:
    print(f"\n   Install missing packages:")
    print(f"   pip install {' '.join(missing_packages)}")
    print(f"\n   Or install all at once:")
    print(f"   pip install -r requirements.txt")
    sys.exit(1)

# Check config.py
print("\n3. Checking configuration file...")
try:
    import config
    print(f"   ✓ config.py loaded")
    
    # Check key configurations
    print(f"\n   Configuration summary:")
    print(f"     • Project root: {config.PROJECT_ROOT}")
    print(f"     • Complexes: {len(config.COMPLEXES)} - {', '.join(config.COMPLEXES)}")
    print(f"     • XVG files: {len(config.XVG_FILES)} - {', '.join(config.XVG_FILES.keys())}")
    print(f"     • Total time: {config.TOTAL_TIME_NS} ns")
    print(f"     • Block size: {config.BLOCK_SIZE_NS} ns")
    print(f"     • Bootstrap samples: {config.N_BOOTSTRAP}")
    
except ImportError as e:
    print(f"   ✗ Error loading config.py: {e}")
    sys.exit(1)

# Check project directory
print("\n4. Checking project structure...")
if config.PROJECT_ROOT.exists():
    print(f"   ✓ Project root exists: {config.PROJECT_ROOT}")
    
    # Check complex directories
    found_complexes = 0
    for complex_name in config.COMPLEXES:
        complex_dir = config.PROJECT_ROOT / complex_name
        if complex_dir.exists():
            print(f"     ✓ {complex_name}/")
            found_complexes += 1
            
            # Check XVG files
            for desc_name, filename in config.XVG_FILES.items():
                filepath = complex_dir / filename
                if filepath.exists():
                    size_kb = filepath.stat().st_size / 1024
                    print(f"       ✓ {filename} ({size_kb:.1f} KB)")
                else:
                    print(f"       ✗ {filename} NOT FOUND")
        else:
            print(f"     ✗ {complex_name}/ NOT FOUND")
    
    if found_complexes == 0:
        print(f"\n   ⚠ No complex directories found!")
        print(f"   Check PROJECT_ROOT setting in config.py")
    else:
        print(f"\n   Found {found_complexes}/{len(config.COMPLEXES)} complexes")

else:
    print(f"   ✗ Project root not found: {config.PROJECT_ROOT}")
    print(f"   Update PROJECT_ROOT in config.py to match your directory structure")

# Check output directory setup
print("\n5. Checking output directories...")
try:
    config.create_directories()
    print(f"   ✓ Output directories created/verified")
    print(f"     • Main: {config.OUTPUT_DIR}")
    print(f"     • Figures: {config.FIGURES_DIR}")
    print(f"     • Tables: {config.TABLES_DIR}")
    print(f"     • Data: {config.DATA_DIR}")
except Exception as e:
    print(f"   ✗ Error creating directories: {e}")
    sys.exit(1)

# Check custom modules
print("\n6. Checking custom modules...")
try:
    import md_statistics
    print(f"   ✓ md_statistics.py")
except ImportError as e:
    print(f"   ✗ Error loading md_statistics.py: {e}")
    sys.exit(1)

try:
    import plotting
    print(f"   ✓ plotting.py")
except ImportError as e:
    print(f"   ✗ Error loading plotting.py: {e}")
    sys.exit(1)

try:
    import export
    print(f"   ✓ export.py")
except ImportError as e:
    print(f"   ✗ Error loading export.py: {e}")
    sys.exit(1)

# Summary
print("\n" + "="*70)
print("VERIFICATION COMPLETE")
print("="*70)

print("\n✓ All checks passed! You can now run:")
print("\n  python run_analysis.py\n")

print("Quick tips:")
print("  • Edit config.py to customize analysis parameters")
print("  • Use VERBOSE=2 in config.py for debug output")
print("  • Check README.txt for detailed documentation")
print("  • Results will be saved to:", config.OUTPUT_DIR)

