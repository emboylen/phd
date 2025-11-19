# 🚀 Quick Reference Guide

## One-Page Guide to Reproducible Bibliometric Analysis

---

## ⚡ Quick Start

### Generate All Analyses
```bash
python complete_analysis.py      # ~2 minutes
python generate_all_plots.py     # ~1 minute
```

### Verify Results
```bash
python verify_analysis.py
```

---

## 📊 What You Get

| Output | Location | Description |
|--------|----------|-------------|
| **All 28 Analyses** | `output/ReproducedBibliometricAnalysis.xlsx` | Complete bibliometric metrics |
| **15 Plots** | `output/plots/*.png` | Publication-quality (300 DPI) |
| **Summary** | `output/ANALYSIS_SUMMARY.md` | Key findings |

---

## 📁 Key Files

### Data
- `data/filtered_data_biblioshiny_ready.xlsx` - **Clean dataset (214 records)**
- `stopwords.csv` - Keyword filtering
- `synonyms.csv` - Keyword mapping

### Scripts
- `complete_analysis.py` - Main analysis
- `generate_all_plots.py` - Visualizations
- `verify_analysis.py` - Validation

### Documentation
- `README.md` - Full guide (12 pages)
- `METHODS.md` - Complete methodology (17 pages)
- `PROJECT_COMPLETE.md` - Final summary

---

## 🔧 Common Tasks

### Update Stopwords
```bash
# Edit stopwords.csv, then:
python complete_analysis.py
python generate_all_plots.py
```

### Modify Synonyms
```bash
# Edit synonyms.csv, then:
python complete_analysis.py
python generate_all_plots.py
```

### Check Data
```python
import pandas as pd
df = pd.read_excel('data/filtered_data_biblioshiny_ready.xlsx')
print(f"Records: {len(df)}")
print(f"Years: {df['PY'].min():.0f}-{df['PY'].max():.0f}")
```

---

## 📈 Key Results

| Metric | Value |
|--------|-------|
| **Records** | 214 papers |
| **Timespan** | 2009-2025 |
| **Sources** | 103 journals |
| **Authors** | 1,006 |
| **Countries** | 40+ |
| **Avg Citations** | 90.03 |
| **Growth Rate** | 9.05% annually |

### Top 3
- **Sources:** Renewable & Sustainable Energy Reviews (21), Bioresource Technology (20), Applied Energy (6)
- **Authors:** Chang J-S (5), Chen W-H (4), Malcata FX (4)
- **Countries:** India (67), China (32), Malaysia (22)
- **Keywords:** Carbon dioxide (78), Wastewater treatment (54), Renewable energy (53)

---

## 🐛 Troubleshooting

### Error: Module not found
```bash
pip install pandas openpyxl numpy matplotlib seaborn wordcloud
```

### Error: File not found
- Run from project root directory
- Check file paths in scripts

### Results differ from Biblioshiny
- Minor differences expected (see METHODS.md)
- Structure should match exactly

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| **README.md** | Complete guide |
| **METHODS.md** | Methodology details |
| **PROJECT_COMPLETE.md** | Final summary |
| **CLEANUP_SUMMARY.md** | Environment status |

---

## ✅ Validation

### Perfect Matches
- MainInfo ✅
- AnnualSciProd ✅
- MostRelSources ✅
- BradfordLaw ✅
- MostRelAuthors ✅

### Close Matches (Minor differences)
- AnnualCitPerYear ≈ (citable year calculation)
- MostFreqWords ≈ (keyword filtering timing)
- CorrAuthCountries ≈ (country extraction variants)

---

## 🎯 For Your PhD

**Include in Thesis:**
1. Tables from Excel file
2. Plots from `output/plots/`
3. Methods from METHODS.md
4. Results from ANALYSIS_SUMMARY.md

**For Manuscript:**
1. Methods: METHODS_MANUSCRIPT.md
2. Figures: Select key plots
3. Tables: Select key analyses
4. Cite: Aria & Cuccurullo (2017)

---

## 📞 Need Help?

1. Check README.md (Section: Troubleshooting)
2. Check METHODS.md (Section: Limitations)
3. Review verification results: `verify_analysis.py`
4. Check bibliometrix docs: https://www.bibliometrix.org/

---

## 🔄 Workflow

```
Data (214 records)
    ↓
complete_analysis.py (28 analyses)
    ↓
generate_all_plots.py (15 plots)
    ↓
verify_analysis.py (validation)
    ↓
Ready for Publication!
```

---

## ⏱️ Execution Time

- Data loading: <10 seconds
- All analyses: ~2 minutes
- All plots: ~1 minute
- **Total: ~3 minutes**

---

## 💾 File Sizes

- Input data: ~500 KB
- Output Excel: ~1 MB
- All plots: ~5 MB
- **Total: ~6.5 MB**

---

## ✨ Key Features

✅ Fully reproducible  
✅ Publication-quality outputs  
✅ Validated against Biblioshiny  
✅ Comprehensive documentation  
✅ Fast execution (<5 min)  
✅ Easy to customize  

---

**Version:** 2.0.0  
**Date:** November 19, 2025  
**Status:** Production Ready ✅

---

*For detailed information, see README.md or METHODS.md*

