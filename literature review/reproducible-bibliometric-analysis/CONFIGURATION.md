# ✅ CONFIGURATION UPDATE

## Changes Made

Your system is now configured to read raw data from the **"raw data"** folder.

### Updated Files:
- ✓ `wrangle_data.R` - Updated to point to `../raw data`
- ✓ `START_HERE.md` - Updated documentation
- ✓ `QUICK_START.md` - Updated documentation

### Expected Directory Structure:

```
D:/Github/phd/literature review/
│
├── raw data/                              ← Your raw files go here
│   ├── scopus.csv
│   ├── scopus-umbrella.csv
│   ├── wos.bib
│   ├── wos(1).bib
│   ├── wos(2).bib
│   ├── wos(3).bib
│   ├── wos(4).bib
│   ├── wos-umbrella.bib
│   ├── cab.txt
│   ├── cab(1).txt
│   ├── cab(2).txt
│   └── cab-umbrella.txt
│
└── reproducible-bibliometric-analysis/   ← Your working directory
    ├── LIT-REVIEW-SCREENED.xlsx          ← Your screened list
    ├── run_all.R                         ← Run this script
    ├── wrangle_data.R                    ← Configured for "../raw data"
    ├── run_bibliometric_analysis.R
    ├── config.R
    ├── START_HERE.md
    └── ... etc
```

### Configuration in wrangle_data.R:

```r
RAW_DATA_DIR <- "../raw data"  # Points to raw data folder
```

If your folder is named differently or in a different location, edit this line in `wrangle_data.R`.

---

## Ready to Run! 🚀

Open RStudio and execute:

```r
setwd("D:/Github/phd/literature review/reproducible-bibliometric-analysis")
source("run_all.R")
```

The script will:
1. Look for `LIT-REVIEW-SCREENED.xlsx` in current directory ✓
2. Import all raw files from `../raw data` folder ✓
3. Match screened papers and create filtered dataset
4. Run comprehensive bibliometric analysis
5. Export results to `output/` folder

---

## What Gets Created:

**data/** folder (after Step 1):
- `filtered_data_biblioshiny_ready.xlsx`
- `filtered_data.csv`
- `unmatched_papers.xlsx` (if any papers couldn't be matched)

**output/** folder (after Step 2):
- `Full_Bibliometric_Report.xlsx` ← Main results file
- `ANALYSIS_SUMMARY.txt` ← Quick overview
- Individual CSV files (MainInfo, TrendTopics, etc.)

---

**All set! Your system is configured and ready to run.** ✨

