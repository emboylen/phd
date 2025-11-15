# ============================================================================
# Setup Script for Refined Topic Modeling
# ============================================================================
#
# This script will:
# 1. Remove the old Python 3.14 virtual environment
# 2. Create a new Python 3.12 virtual environment
# 3. Install all required packages
# 4. Run the refined topic modeling script
#
# ============================================================================

Write-Host "=== Refined Topic Modeling Setup ===" -ForegroundColor Cyan
Write-Host ""

# Step 1: Set execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

# Step 2: Remove old virtual environment if it exists
if (Test-Path "venv312") {
    Write-Host "Removing old virtual environment..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force venv312
    Write-Host "✓ Old environment removed" -ForegroundColor Green
}

# Step 3: Create new Python 3.12 virtual environment
Write-Host "`nCreating Python 3.12 virtual environment..." -ForegroundColor Yellow
try {
    py -3.12 -m venv venv312
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Python 3.12 not found!" -ForegroundColor Red
    Write-Host "Please install Python 3.12 from: https://www.python.org/downloads/" -ForegroundColor Red
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Red
    pause
    exit 1
}

# Step 4: Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
& ".\venv312\Scripts\Activate.ps1"
Write-Host "✓ Environment activated" -ForegroundColor Green

# Step 5: Upgrade pip
Write-Host "`nUpgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Step 6: Install required packages for refined model
Write-Host "`nInstalling required packages (this may take several minutes)..." -ForegroundColor Yellow
Write-Host "  - Installing NLP packages: spaCy and NLTK..."
python -m pip install spacy nltk --quiet

Write-Host "  - Installing topic modeling packages: Gensim..."
python -m pip install gensim --quiet

Write-Host "  - Installing visualization packages..."
python -m pip install matplotlib networkx pyvis --quiet

Write-Host "  - Installing PDF processing: PyMuPDF..."
python -m pip install PyMuPDF --quiet

Write-Host "  - Installing data processing: pandas and scikit-learn..."
python -m pip install pandas scikit-learn --quiet

Write-Host "✓ All packages installed" -ForegroundColor Green

# Step 7: Download spaCy language model
Write-Host "`nDownloading spaCy English language model..." -ForegroundColor Yellow
python -m spacy download en_core_web_sm --quiet
Write-Host "✓ Language model downloaded" -ForegroundColor Green

# Step 8: Run the refined topic modeling script
Write-Host "`n" + "=" * 80 -ForegroundColor Cyan
Write-Host "Starting Refined Topic Modeling Analysis..." -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""

python refined-topic-model.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n" + "=" * 80 -ForegroundColor Green
    Write-Host "✓ Analysis Complete!" -ForegroundColor Green
    Write-Host "=" * 80 -ForegroundColor Green
    Write-Host "`nOutput files created:" -ForegroundColor Cyan
    Write-Host "  1. refined_topics_summary.html - Detailed topics table"
    Write-Host "  2. refined_knowledge_graph.html - Interactive visualization"
    Write-Host "  3. coherence_plot.png - Topic optimization chart"
    Write-Host ""
} else {
    Write-Host "`n✗ An error occurred during analysis" -ForegroundColor Red
}

Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

