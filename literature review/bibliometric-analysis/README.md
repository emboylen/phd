# Bibliometric Analysis

This directory contains data and scripts for bibliometric analysis of microalgae biofuel research literature.

## Overview

The bibliometric analysis examines 214 unique scientific articles (2009-2025) to understand publication trends, key contributors, citation patterns, and research themes in the microalgae biofuel field.

## Contents

### Data Files
- **`broad.csv`** - Broad search results from literature databases
- **`filtered_data.csv/xlsx`** - Cleaned dataset after screening
- **`filtered_data_biblioshiny_ready.xlsx`** - Final dataset formatted for Biblioshiny import
- **`lit-review-overview-biblio.drawio.png`** - Workflow diagram

### R Scripts
- **`bibliometrix-data-wrangling-BROAD.R`** - Data cleaning and preparation script

### Export Results
- **`export results/`** - Contains Biblioshiny analysis reports from various iterations

### Reproducible Analysis (Primary)
- **`reproducible-bibliometric-analysis/`** - Complete automated analysis pipeline
  - See dedicated [README.md](reproducible-bibliometric-analysis/README.md) for full documentation
  - Contains both R and Python implementations
  - Generates 28 comprehensive bibliometric analyses
  - Creates 15 publication-quality visualizations

## Quick Start

### Option 1: Use Complete Automated Pipeline (Recommended)
```bash
cd reproducible-bibliometric-analysis

# Python approach
python complete_analysis.py
python generate_all_plots.py

# R approach
Rscript run_all.R
```

### Option 2: Manual Analysis in Biblioshiny
1. Open RStudio
2. Install bibliometrix: `install.packages("bibliometrix")`
3. Launch Biblioshiny: `bibliometrix::biblioshiny()`
4. Import `filtered_data_biblioshiny_ready.xlsx`
5. Run analyses through GUI

## Key Outputs

### Dataset Statistics
- **Records**: 214 unique articles
- **Timespan**: 2009-2025 (17 years)
- **Sources**: 103 unique journals
- **Authors**: 1,006 researchers
- **Countries**: 40+ represented
- **Total Citations**: 19,267

### Top Findings
**Most Productive Journals:**
1. Renewable and Sustainable Energy Reviews (21 articles)
2. Bioresource Technology (20 articles)
3. Applied Energy (6 articles)

**Most Productive Authors:**
1. Chang J-S (5 articles)
2. Chen W-H (4 articles)
3. Malcata FX (4 articles)

**Top Contributing Countries:**
1. India (67 documents)
2. China (32 documents)
3. Malaysia (22 documents)

## Workflow

```
Raw Data (Scopus, WoS, CAB)
        ↓
Data Cleaning (R)
        ↓
Filtered Dataset (214 records)
        ↓
Bibliometric Analysis (R/Python)
        ↓
Visualizations & Reports
```

## Data Sources

Literature was collected from three major databases:
- **Web of Science** (WoS)
- **Scopus**
- **CAB Abstracts**

Papers were screened using Rayyan for relevance to microalgae biofuel sustainability.

## Dependencies

**For R Scripts:**
```r
install.packages(c("bibliometrix", "readxl", "writexl", "dplyr", "ggplot2"))
```

**For Python Scripts:**
```bash
pip install pandas openpyxl numpy matplotlib seaborn wordcloud
```

## Documentation

For detailed methodology, analysis descriptions, and reproducibility information, see:
- [reproducible-bibliometric-analysis/README.md](reproducible-bibliometric-analysis/README.md) - Complete documentation
- [reproducible-bibliometric-analysis/METHODS.md](reproducible-bibliometric-analysis/METHODS.md) - Detailed methodology

## Integration with PhD Research

This bibliometric analysis provides the quantitative foundation for understanding:
- Research productivity trends over time
- Geographic distribution of research effort
- Key research themes and their evolution
- Citation impact and influential works
- Collaboration patterns

The findings inform the broader PhD research question: **Why is algae not being used for biofuel despite its promise?**

## Citation

If using this analysis or methodology:

**For bibliometrix package:**
```
Aria, M., & Cuccurullo, C. (2017). bibliometrix: An R-tool for comprehensive 
science mapping analysis. Journal of Informetrics, 11(4), 959-975.
https://doi.org/10.1016/j.joi.2017.08.007
```

**For this workflow:**
See main project README.md for citation details.

---

**Last Updated**: November 22, 2025  
**Dataset Version**: 214 papers (2009-2025)  
**Status**: Analysis complete and validated

