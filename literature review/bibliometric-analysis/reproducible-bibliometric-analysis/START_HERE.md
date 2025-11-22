# 🎯 READY TO RUN: Complete Setup Guide

## ✅ What's Been Created

Your reproducible bibliometric analysis system is **ready to run**. Here's what you have:

```
reproducible-bibliometric-analysis/
├── wrangle_data.R              # Step 1: Extract filtered citations
├── run_bibliometric_analysis.R # Step 2: Run analysis  
├── run_all.R                   # Master script (runs both steps)
├── config.R                    # Configuration settings
├── config_example.R            # Example configuration
├── README.md                   # Full documentation
├── QUICK_START.md              # Quick start guide
└── LIT-REVIEW-SCREENED.xlsx    # Your screened paper list ✓
```

---

## 🚀 How to Run (3 Easy Steps)

### Step 1: Choose Your Method

**Option A: Terminal/Command Line (Recommended)** ⚡
```powershell
cd "C:\Github\phd\literature review\bibliometric-analysis\reproducible-bibliometric-analysis"
Rscript run_all.R
```

**Option B: RStudio or R Console**
```r
setwd("D:/Github/phd/literature review/reproducible-bibliometric-analysis")
source("run_all.R")
```

> **💡 Tip**: See `TERMINAL_USAGE.md` for detailed terminal instructions

### Step 2: The Script Runs Automatically

This will:
1. Load your screened list (LIT-REVIEW-SCREENED.xlsx)
2. Import all raw citation files from "raw data" folder
3. Match and extract filtered citations
4. Run comprehensive bibliometric analysis
5. Export all results

**Alternative: Step-by-Step Execution**
```r
# Step 1: Extract filtered citations
source("wrangle_data.R")

# Step 2: Run analysis
source("config.R")
source("run_bibliometric_analysis.R")
main()
```

### Step 3: View Results

Check these directories:
- `data/` - Filtered bibliometric dataset
- `output/` - All analysis results

---

## 📊 What You'll Get

### From Data Wrangling (Step 1):
- `data/filtered_data_biblioshiny_ready.xlsx` - Ready for analysis
- `data/filtered_data.csv` - CSV format
- `data/unmatched_papers.xlsx` - Papers that couldn't be matched (if any)
- Console output showing match rate

### From Analysis (Step 2):
- `output/Full_Bibliometric_Report.xlsx` - **All results in one Excel file**
- `output/ANALYSIS_SUMMARY.txt` - Summary report
- Individual CSV files:
  - MainInfo.csv
  - AnnualSciProd.csv
  - MostRelSources.csv
  - MostRelAuthors.csv
  - MostGlobCitDocs.csv
  - TrendTopics.csv
  - ThematicMap.csv
  - CollaborationStats.csv

---

## 🔍 What the Scripts Do

### wrangle_data.R
**Purpose**: Matches your screened papers with raw citation data

**Process**:
1. Loads `LIT-REVIEW-SCREENED.xlsx`
2. Finds the title column automatically
3. Imports all raw citation files from parent directory:
   - Scopus: `scopus.csv`, `scopus-umbrella.csv`
   - CAB: `cab.txt`, `cab(1).txt`, `cab(2).txt`, `cab-umbrella.txt`
   - Web of Science: `wos.bib`, `wos(1-4).bib`, `wos-umbrella.bib`
4. Combines all raw data
5. Matches screened papers by title (normalized matching)
6. Exports filtered dataset

**Output**: Filtered bibliometric data ready for analysis

### run_bibliometric_analysis.R
**Purpose**: Performs comprehensive bibliometric analysis

**Analyses**:
- Basic statistics (documents, authors, journals, years)
- Annual production trends
- Most relevant sources/journals
- Most relevant authors
- Most cited documents
- Keyword trends over time
- Thematic keyword clusters
- Collaboration network statistics

**Output**: Publication-ready tables and reports

---

## ⚙️ Customization (Optional)

Edit `config.R` to customize:

```r
# Number of top items in tables
TOP_K <- 20

# Filter by year range
YEAR_RANGE <- NULL  # Use all years
# YEAR_RANGE <- c(2015, 2024)  # Only 2015-2024

# Trend analysis field
TREND_FIELD <- "ID"  # Keywords Plus
# TREND_FIELD <- "DE"  # Author Keywords
# TREND_FIELD <- "TI"  # Title words

# Enable/disable specific analyses
ANALYSES <- list(
  main_info = list(enabled = TRUE, filename = "MainInfo.csv"),
  trend_topics = list(enabled = TRUE, filename = "TrendTopics.csv"),
  # ... etc
)
```

---

## 🐛 Troubleshooting

### Low Match Rate (<80%)

**Problem**: Not all screened papers were found in raw data

**Solutions**:
1. Check console output for match rate
2. Review `data/unmatched_papers.xlsx`
3. Verify title column in `LIT-REVIEW-SCREENED.xlsx`
4. Ensure raw citation files are in parent directory

### Missing Packages

**Problem**: Package error when running

**Solution**: Install required packages:
```r
install.packages(c("bibliometrix", "readxl", "writexl", "dplyr", "ggplot2"))
```

### File Not Found

**Problem**: Raw citation files not found

**Solution**: Check that raw files are in the "raw data" folder:
```
D:/Github/phd/literature review/
├── reproducible-bibliometric-analysis/  (your current location)
└── raw data/                           (raw files should be here)
    ├── scopus.csv
    ├── scopus-umbrella.csv
    ├── wos.bib
    ├── wos(1).bib
    ├── cab.txt
    └── ... etc
```

If your raw data is in a different location, update `RAW_DATA_DIR` in `wrangle_data.R`:
```r
RAW_DATA_DIR <- "../raw data"  # Current setting
# Or specify full path:
# RAW_DATA_DIR <- "D:/Github/phd/literature review/raw data"
```

---

## 📋 Prerequisites Checklist

Before running, ensure:
- ✓ R installed (version ≥ 4.0.0)
- ✓ Required packages installed (`bibliometrix`, `readxl`, `writexl`)
- ✓ `LIT-REVIEW-SCREENED.xlsx` in current directory
- ✓ Raw citation files in "raw data" folder (parent directory)
- ✓ Title column exists in screened list

---

## 💡 Tips

1. **First run**: Use default settings (don't modify config.R)
2. **Check match rate**: Should be >90% for good results
3. **Review unmatched**: Check `data/unmatched_papers.xlsx` if match rate is low
4. **Customize later**: After successful first run, adjust settings in config.R
5. **Save workspace**: For large datasets, save after data wrangling:
   ```r
   save.image("workspace.RData")
   ```

---

## 🎓 Example Session

Here's what a successful run looks like:

```r
> setwd("D:/Github/phd/literature review/reproducible-bibliometric-analysis")
> source("run_all.R")

=============================================================================
COMPLETE BIBLIOMETRIC ANALYSIS WORKFLOW
=============================================================================

STEP 1/2: DATA WRANGLING
-----------------------------------------------------------------------------
[2025-11-17 10:30:15] Loading screened paper list...
[2025-11-17 10:30:16] Loaded 150 screened papers
[2025-11-17 10:30:16] Using title column: title
[2025-11-17 10:30:16] Valid screened titles: 150
[2025-11-17 10:30:16] Importing raw citation files...
[2025-11-17 10:30:20] Successfully imported 12 files
[2025-11-17 10:30:21] Combined dataset: 5432 total records
[2025-11-17 10:30:22] Matched 147 of 150 screened papers
[2025-11-17 10:30:22] Match rate: 98.0 %
[2025-11-17 10:30:23] Final dataset: 147 unique records
✓ Data wrangling completed successfully

STEP 2/2: BIBLIOMETRIC ANALYSIS
-----------------------------------------------------------------------------
[2025-11-17 10:30:25] Loading data from: data/filtered_data_biblioshiny_ready.xlsx
[2025-11-17 10:30:26] Loaded 147 records with 68 fields
[2025-11-17 10:30:26] Running bibliometric analysis...
[2025-11-17 10:30:30] Exporting standard tables...
[2025-11-17 10:30:35] Performing trend analysis...
[2025-11-17 10:30:40] Creating combined Excel report...
✓ Bibliometric analysis completed successfully

=============================================================================
WORKFLOW COMPLETED SUCCESSFULLY!
=============================================================================

Total execution time: 45.3 seconds

Output locations:
  • Filtered data:  data/
  • Analysis results: output/

Key output files:
  • data/filtered_data_biblioshiny_ready.xlsx
  • output/Full_Bibliometric_Report.xlsx
  • output/ANALYSIS_SUMMARY.txt
```

---

## 📚 Next Steps After Running

1. **Review Summary**: Open `output/ANALYSIS_SUMMARY.txt`
2. **Main Results**: Open `output/Full_Bibliometric_Report.xlsx`
3. **Check Quality**: Review match rate and unmatched papers
4. **Customize**: Adjust settings in `config.R` and re-run if needed
5. **Use Results**: Import tables into your literature review

---

## ✨ Key Features

✅ **Fully Automated** - No manual GUI interactions  
✅ **Reproducible** - Run same analysis on different datasets  
✅ **Flexible** - Highly configurable via config.R  
✅ **Production Quality** - Clean, maintainable, well-documented code  
✅ **Complete** - Replicates all major biblioshiny analyses  
✅ **Fast** - Processes thousands of citations in seconds  

---

**You're all set! Just run `source("run_all.R")` in RStudio to get started.** 🚀

