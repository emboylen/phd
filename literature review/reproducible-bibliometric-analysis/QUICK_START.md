# =============================================================================
# QUICK START GUIDE: Complete Workflow
# =============================================================================
# This guide walks you through the complete workflow from screened papers
# to final bibliometric analysis results.
# =============================================================================

## WORKFLOW OVERVIEW

**Step 1: Data Wrangling** (wrangle_data.R)
- Input: Screened paper list + Raw citation files
- Output: Filtered bibliometric dataset

**Step 2: Bibliometric Analysis** (run_bibliometric_analysis.R)  
- Input: Filtered bibliometric dataset
- Output: Analysis results (CSVs, Excel, reports)

# =============================================================================
# STEP 1: DATA WRANGLING
# =============================================================================

## What You Need:
1. Screened paper list: `LIT-REVIEW-SCREENED.xlsx` 
   - Must contain a "title" column (case-insensitive)
   
2. Raw citation export files in "raw data" folder (parent directory):
   - Scopus: scopus.csv, scopus-umbrella.csv
   - CAB: cab.txt, cab(1).txt, cab(2).txt, cab-umbrella.txt  
   - Web of Science: wos.bib, wos(1-4).bib, wos-umbrella.bib

## How to Run:

### Option A: RStudio/R Console
```r
setwd("reproducible-bibliometric-analysis")
source("wrangle_data.R")
```

### Option B: Command Line
```bash
cd reproducible-bibliometric-analysis
Rscript wrangle_data.R
```

## What Gets Created:
- `data/filtered_data.csv` - Filtered dataset (CSV format)
- `data/filtered_data.xlsx` - Filtered dataset (Excel format)
- `data/filtered_data_biblioshiny_ready.xlsx` - Ready for analysis
- `data/unmatched_papers.xlsx` - Papers that couldn't be matched (if any)

## Troubleshooting:

**Low match rate (<80%)**
- Check title column name in your screened list
- Verify titles match between screened list and raw files
- Check that raw files are in the correct location

**File not found errors**
- Ensure raw citation files are in parent directory (`..`)
- Update `RAW_DATA_DIR` in wrangle_data.R if needed

# =============================================================================
# STEP 2: BIBLIOMETRIC ANALYSIS  
# =============================================================================

## Prerequisites:
- Completed Step 1 (data wrangling)
- File exists: `data/filtered_data_biblioshiny_ready.xlsx`

## How to Run:

### Option A: RStudio/R Console
```r
setwd("reproducible-bibliometric-analysis")
source("config.R")
source("run_bibliometric_analysis.R")
main()
```

### Option B: Command Line
```bash
cd reproducible-bibliometric-analysis
Rscript run_bibliometric_analysis.R
```

## What Gets Created:
- `output/MainInfo.csv` - Basic metadata
- `output/AnnualSciProd.csv` - Publications per year
- `output/MostRelSources.csv` - Top journals
- `output/MostRelAuthors.csv` - Top authors
- `output/MostGlobCitDocs.csv` - Most cited papers
- `output/TrendTopics.csv` - Keyword trends over time
- `output/ThematicMap.csv` - Keyword clusters
- `output/CollaborationStats.csv` - Network statistics
- `output/Full_Bibliometric_Report.xlsx` - All results in one file
- `output/ANALYSIS_SUMMARY.txt` - Summary report

## Customization:

Edit `config.R` to customize:
- Number of top items (TOP_K = 20)
- Year range filter (YEAR_RANGE = NULL for all years)
- Trend analysis field (TREND_FIELD = "ID" for Keywords Plus)
- Thematic map parameters
- Enable/disable specific analyses

# =============================================================================
# COMPLETE WORKFLOW IN ONE GO
# =============================================================================

If you want to run both steps automatically:

```r
# Set working directory
setwd("reproducible-bibliometric-analysis")

# Step 1: Wrangle data
source("wrangle_data.R")

# Step 2: Run analysis
source("config.R")
source("run_bibliometric_analysis.R")
main()
```

Or create a master script `run_all.R`:

```r
#!/usr/bin/env Rscript
# Complete workflow: Data wrangling → Analysis

cat("=============================================================================\n")
cat("COMPLETE BIBLIOMETRIC ANALYSIS WORKFLOW\n")
cat("=============================================================================\n\n")

# Step 1: Data Wrangling
cat("STEP 1/2: DATA WRANGLING\n")
cat("-----------------------------------------------------------------------------\n")
source("wrangle_data.R")

cat("\n\n")

# Step 2: Bibliometric Analysis
cat("STEP 2/2: BIBLIOMETRIC ANALYSIS\n")
cat("-----------------------------------------------------------------------------\n")
source("config.R")
source("run_bibliometric_analysis.R")
results <- main()

cat("\n\n")
cat("=============================================================================\n")
cat("WORKFLOW COMPLETED!\n")
cat("=============================================================================\n")
cat("Check the 'output/' directory for results.\n")
```

# =============================================================================
# FILE STRUCTURE
# =============================================================================

```
reproducible-bibliometric-analysis/
├── wrangle_data.R              # Step 1: Extract filtered citations
├── config.R                    # Configuration settings
├── run_bibliometric_analysis.R # Step 2: Run analysis
├── QUICK_START.R               # This guide
├── README.md                   # Full documentation
├── LIT-REVIEW-SCREENED.xlsx    # Your screened paper list
│
├── data/                       # Generated by wrangle_data.R
│   ├── filtered_data.csv
│   ├── filtered_data.xlsx
│   ├── filtered_data_biblioshiny_ready.xlsx
│   └── unmatched_papers.xlsx (if any)
│
└── output/                     # Generated by run_bibliometric_analysis.R
    ├── MainInfo.csv
    ├── AnnualSciProd.csv
    ├── MostRelSources.csv
    ├── MostRelAuthors.csv
    ├── MostGlobCitDocs.csv
    ├── TrendTopics.csv
    ├── ThematicMap.csv
    ├── CollaborationStats.csv
    ├── Full_Bibliometric_Report.xlsx
    └── ANALYSIS_SUMMARY.txt
```

# =============================================================================
# REQUIRED R PACKAGES
# =============================================================================

Install all required packages:

```r
install.packages(c(
  "bibliometrix",  # Bibliometric analysis
  "readxl",        # Read Excel files
  "writexl",       # Write Excel files
  "dplyr",         # Data manipulation
  "ggplot2"        # Plotting (optional)
))
```

# =============================================================================
# TIPS & BEST PRACTICES
# =============================================================================

1. **Keep raw files unchanged** - Never modify original citation exports

2. **Version control** - Use meaningful filenames or timestamps
   - Set `USE_TIMESTAMP <- TRUE` in config.R

3. **Document your process** - The ANALYSIS_SUMMARY.txt is auto-generated

4. **Review match rate** - After wrangling, check that >90% papers matched

5. **Customize carefully** - Test with default settings first

6. **Save workspace** - For large datasets:
   ```r
   save.image("analysis_workspace.RData")
   ```

# =============================================================================
# SUPPORT
# =============================================================================

For issues:
1. Check console output for specific error messages
2. Review ANALYSIS_SUMMARY.txt for diagnostics
3. Check data/unmatched_papers.xlsx if match rate is low
4. Ensure all required packages are installed
5. Verify file paths in configuration

Common fixes:
- Update R to version ≥ 4.0.0
- Reinstall bibliometrix: `install.packages("bibliometrix")`
- Check working directory: `getwd()`
- Verify file permissions

# =============================================================================

