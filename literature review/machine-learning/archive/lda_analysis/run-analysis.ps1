# ============================================================================
# PDF Topic Knowledge Graph - Setup and Run Script
# ============================================================================
#
# HOW TO RUN THIS SCRIPT:
#   Option 1 (Recommended): Right-click this file → "Run with PowerShell"
#   Option 2: Open PowerShell, navigate to this folder, then run: .\run-analysis.ps1
#
# PREREQUISITES:
#   - Python 3.12 or 3.11 must be installed
#   - Download from: https://www.python.org/downloads/
#   - Make sure to check "Add Python to PATH" during installation
#
# WHAT THIS SCRIPT DOES:
#   1. Sets execution policy to allow scripts to run
#   2. Creates a Python 3.12 virtual environment
#   3. Activates the virtual environment
#   4. Installs required Python packages
#   5. Runs the PDF analysis
#
# ============================================================================

# Step 1: Set execution policy to allow PowerShell scripts to run
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Step 2: Create Python 3.12 virtual environment (named venv312)
py -3.12 -m venv venv312

# Step 3: Activate the virtual environment
.\venv312\Scripts\Activate.ps1

# Step 4: Install Jupyter (optional - only needed if you want to use notebooks)
pip install jupyter

# Step 5: Install required packages for PDF analysis
# This may take several minutes on first run
pip install PyMuPDF bertopic scikit-learn networkx pyvis pandas sentence-transformers

# Step 6: Run the PDF analysis script
# This will process all PDFs in D:\Github\phd\ML\included
# Output will be saved as pdf_knowledge_graph.html

# Set console to UTF-8 encoding to handle Unicode characters
chcp 65001 > $null
$env:PYTHONIOENCODING = "utf-8"

python advanced-ML.py