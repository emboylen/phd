# 📊 Reproducible Bibliometric Analysis - Overview

**Analysis Date:** 2025-11-19  
**Dataset:** 222 papers from screened literature review  
**Status:** ✅ Complete and Ready

---

## 🎯 What This Is

A **fully automated and reproducible** bibliometric analysis workflow that:
- Takes your screened paper list
- Matches it against raw database exports
- Performs comprehensive bibliometric analysis
- Generates all visualizations and tables
- Can be re-run anytime with a single command

---

## 📁 Project Structure

```
reproducible-bibliometric-analysis/
├── 📄 Core Scripts (Required)
│   ├── run_all.R                    # Master script - runs everything
│   ├── wrangle_data.R               # Loads and filters raw data
│   ├── run_bibliometric_analysis.R  # Performs analysis & creates outputs
│   └── config.R                     # All configuration settings
│
├── 📊 Input Data (Required)
│   ├── LIT-REVIEW-SCREENED.xlsx     # Your screened paper list
│   ├── stopwords.csv                # Stopwords for keyword analysis
│   ├── synonyms.csv                 # Synonym mappings for keywords
│   └── raw data/                    # Database exports (11 files)
│       ├── scopus.csv, scopus.bib, scopus.ris
│       ├── cab.txt, cab(1).txt, cab(2).txt
│       └── wos.bib, wos(1-4).bib
│
├── 💾 Generated Data (Output)
│   └── data/
│       ├── filtered_data.csv                    # Matched papers (CSV)
│       ├── filtered_data.xlsx                   # Matched papers (Excel)
│       └── filtered_data_biblioshiny_ready.xlsx # Upload to biblioshiny
│
├── 📈 Analysis Results (Output)
│   └── output/
│       ├── Full_Bibliometric_Report.xlsx  # All tables in one file
│       ├── ANALYSIS_SUMMARY.txt           # Overview of analysis
│       ├── AnnualSciProd.csv              # Publications per year
│       ├── CountrySciProd.csv             # Country production
│       ├── MostRelSources.csv             # Top journals
│       ├── MostRelAuthors.csv             # Top authors
│       ├── MostGlobCitDocs.csv            # Most cited papers
│       ├── TrendTopics.csv                # Keyword trends
│       └── plots/                         # 10 visualization files
│           ├── 01_Annual_Production.png
│           ├── 02_Top_Authors.png
│           ├── 03_Top_Sources.png
│           ├── 04_Most_Cited.png
│           ├── 05_Country_Production.png
│           ├── 06_Word_Cloud.png
│           ├── 07_Author_Production_Over_Time.png
│           ├── 08_Source_Growth_Over_Time.png
│           ├── 09_Most_Cited_References.png
│           └── 10_Trend_Topics.png
│
└── 📚 Documentation
    ├── README.md              # Main documentation
    ├── START_HERE.md          # Getting started guide
    ├── METHODS.md             # Full technical methods
    ├── METHODS_MANUSCRIPT.md  # Methods for manuscript
    └── OVERVIEW.md            # This file
```

---

## ⚡ Quick Start

### Run Complete Analysis

**Option 1: From Terminal (Recommended)**
```powershell
cd "D:\Github\phd\literature review\reproducible-bibliometric-analysis"
& "C:\Program Files\R\R-4.2.0\bin\Rscript.exe" run_all.R
```

**Option 2: From R Console**
```r
setwd("D:/Github/phd/literature review/reproducible-bibliometric-analysis")
source("run_all.R")
```

**Time:** ~20 seconds  
**Output:** All CSV files, Excel report, and 10 plots

---

## 📊 Analysis Summary

### Dataset
- **Total Papers:** 222 (from screened list where `included=TRUE`)
- **Timespan:** 2009-2025
- **Unique Documents:** 216 (after deduplication)
- **Sources:** 103 journals
- **Authors:** 1,006
- **Average Citations:** 89.61 per document

### Key Findings
- **Annual Growth Rate:** 9.05%
- **Top Journal:** Renewable and Sustainable Energy Reviews (21 papers)
- **Top Author:** CHANG J-S (5 papers)
- **Most Cited:** WIJFFELS RH, 2010, Science (1,638 citations)
- **Top Country:** India (39 papers)

---

## 🔧 Configuration

All settings are in `config.R`:
- Input/output paths
- Analysis parameters (top K items, year range)
- Plot settings (size, resolution)
- Enable/disable specific analyses

---

## 📤 For Biblioshiny Verification

Upload this file to biblioshiny for interactive exploration:
```
data/filtered_data_biblioshiny_ready.xlsx
```

Launch biblioshiny:
```r
library(bibliometrix)
biblioshiny()
```

Then upload the file via the web interface.

---

## 🔄 Reproducibility

The analysis is **fully reproducible**:
1. All data wrangling steps are automated
2. All configuration is in `config.R`
3. Duplicate removal is automated (DOI: 10.1016/j.rser.2018.05.052)
4. Stopwords and synonyms are version-controlled
5. All outputs regenerate from scratch each run

**To reproduce:** Just run `run_all.R` again!

---

## 📝 Methods Documentation

- **Full technical details:** `METHODS.md`
- **Manuscript-ready version:** `METHODS_MANUSCRIPT.md`
- **Getting started guide:** `START_HERE.md`
- **Main documentation:** `README.md`

---

## ✅ Quality Checks

- ✅ 100% match rate (222/222 papers from screened list)
- ✅ 1 duplicate removed automatically
- ✅ All 10 plots generated successfully
- ✅ Word cloud refined with stopwords & synonyms
- ✅ Y-axis labels properly formatted
- ✅ All CSV exports created
- ✅ Excel report complete
- ✅ Ready for biblioshiny verification

---

## 🆘 Need Help?

1. **First time running?** → See `START_HERE.md`
2. **Customize analysis?** → Edit `config.R`
3. **Understand methods?** → See `METHODS.md`
4. **Include in paper?** → Use `METHODS_MANUSCRIPT.md`

---

**Ready to use! Run `run_all.R` to regenerate all outputs.** 🚀

