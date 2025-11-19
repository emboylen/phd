# Reproducible Bibliometric Analysis

A complete, automated workflow for performing comprehensive bibliometric analysis on scientific literature. This project provides both R-based (bibliometrix) and Python-based analysis pipelines with publication-quality visualizations.

## 📋 Overview

**Dataset:** 214 unique scientific articles (2009-2025)  
**Field:** Microalgae and biofuel research  
**Analyses:** 28 comprehensive bibliometric metrics  
**Visualizations:** 15 publication-quality plots  

### Key Features

✅ **Fully Reproducible** - Complete scripts from data cleaning to visualization  
✅ **Dual Workflows** - R (bibliometrix) and Python (custom implementation)  
✅ **Publication Ready** - High-resolution plots (300 DPI)  
✅ **Comprehensive** - All major bibliometric analyses included  
✅ **Configurable** - Stopwords and synonyms for keyword filtering  
✅ **Validated** - Verified against Biblioshiny GUI outputs  

---

## 🚀 Quick Start

### Prerequisites

#### For Python Workflow (Recommended)
```bash
pip install pandas openpyxl numpy matplotlib seaborn wordcloud
```

#### For R Workflow
```r
install.packages(c("bibliometrix", "writexl", "readxl", "dplyr", "ggplot2"))
```

### Running the Analysis

#### Python Workflow (Complete Replication)
```bash
# Generate all 28 analyses
python complete_analysis.py

# Generate all 15 plots
python generate_all_plots.py

# Verify against Biblioshiny reference
python verify_analysis.py
```

#### R Workflow (Traditional)
```bash
# Complete pipeline from raw data
Rscript run_all.R

# Or just analysis on filtered data
Rscript run_bibliometric_analysis.R
```

---

## 📊 Outputs Generated

### 1. Excel Analysis File
**File:** `output/ReproducedBibliometricAnalysis.xlsx`  
**Sheets:** 28 comprehensive analyses including:

| Sheet | Description |
|-------|-------------|
| MainInfo | Dataset overview and key statistics |
| AnnualSciProd | Publications per year |
| AnnualCitPerYear | Citation trends over time |
| MostRelSources | Top journals by publication count |
| BradfordLaw | Source distribution across Bradford zones |
| SourceLocImpact | Source impact metrics (h-index, g-index) |
| MostRelAuthors | Top authors (total & fractionalized) |
| AuthorProdOverTime | Author publication timelines |
| LotkaLaw | Author productivity distribution |
| AuthorLocImpact | Author impact metrics |
| MostRelAffiliations | Top research institutions |
| CorrAuthCountries | Country collaboration patterns |
| CountrySciProd | Scientific output by country |
| MostCitCountries | Most cited countries |
| MostGlobCitDocs | Most cited documents globally |
| MostLocCitDocs | Most cited documents locally |
| MostLocCitRefs | Most cited references |
| MostFreqWords | Most frequent keywords |
| WordCloud | Top 50 terms for visualization |
| TrendTopics | Keyword trends over time |
| CoCitNet | Co-citation network metrics |
| Historiograph | Historical citation network |
| CollabWorldMap | International collaborations |

### 2. Visualization Plots
**Directory:** `output/plots/`  
**Format:** PNG (300 DPI, publication quality)

1. Annual Scientific Production
2. Annual Citations per Year
3. Most Relevant Sources
4. Bradford's Law
5. Most Relevant Authors
6. Lotka's Law
7. Country Scientific Production
8. Most Cited Countries
9. Most Frequently Used Words
10. Keyword Word Cloud
11. Trending Topics Over Time
12. Most Globally Cited Documents
13. Source Production Over Time
14. Country Collaboration Map
15. Corresponding Author's Countries

---

## 📁 Project Structure

```
reproducible-bibliometric-analysis/
├── data/
│   ├── filtered_data_biblioshiny_ready.xlsx   # Clean dataset (214 records)
│   ├── filtered_data_biblioshiny_ready.csv    # CSV version
│   ├── filtered_data.xlsx                     # Pre-cleaning (222 records)
│   └── filtered_data.csv
├── raw data/                                   # Original database exports
│   ├── scopus.csv, scopus.bib
│   ├── wos.bib, wos(1-4).bib
│   └── cab.txt, cab(1-2).txt
├── output/
│   ├── ReproducedBibliometricAnalysis.xlsx    # All 28 analyses
│   ├── BiblioshinyReport-2025-11-19.xlsx      # Reference report
│   ├── ANALYSIS_SUMMARY.md                    # Detailed results summary
│   └── plots/                                 # All 15 visualization plots
├── complete_analysis.py                        # Main Python analysis script
├── generate_all_plots.py                       # Python plotting script
├── verify_analysis.py                          # Verification script
├── stopwords.csv                               # Keyword filtering config
├── synonyms.csv                                # Keyword mapping config
├── wrangle_data.R                              # R data cleaning script
├── run_bibliometric_analysis.R                 # R analysis script
├── run_all.R                                   # Complete R pipeline
├── config.R                                    # R configuration
├── README.md                                   # This file
├── METHODS.md                                  # Complete methodology
└── LIT-REVIEW-SCREENED.xlsx                    # Original screening list
```

---

## 🔬 Dataset Information

### Data Cleaning Process
- **Original records:** 222 (from systematic review screening)
- **Empty rows removed:** 7 (no identifiers)
- **Duplicate DOIs removed:** 1
- **Final clean dataset:** 214 unique records

### Dataset Characteristics
- **Timespan:** 2009-2025 (17 years)
- **Sources:** 103 unique journals
- **Authors:** 1,006 unique researchers
- **Countries:** 40+ represented
- **Total citations:** 19,267
- **Average citations/document:** 90.03
- **Keywords (ID):** 1,448 unique terms
- **Keywords (DE):** 692 author keywords

### Top Metrics
**Most Productive Sources:**
1. Renewable and Sustainable Energy Reviews (21 articles)
2. Bioresource Technology (20 articles)
3. Applied Energy (6 articles)

**Most Productive Authors:**
1. Chang J-S (5 articles)
2. Chen W-H (4 articles)
3. Malcata FX (4 articles)

**Top Countries:**
1. India (67 documents)
2. China (32 documents)
3. Malaysia (22 documents)

---

## ⚙️ Configuration

### Keyword Filtering

**Stopwords** (`stopwords.csv`):
18 domain-specific terms filtered from analysis:
- microalga, microalgae, biomass, biofuels, biodiesel, etc.

**Synonyms** (`synonyms.csv`):
38 keyword mappings to consolidate variants:
- "CO2" → "carbon dioxide"
- "greenhouse gases" → "carbon dioxide"
- "wastewater treatment" → standardized form
- etc.

### Analysis Parameters

Both R and Python workflows use consistent parameters:
- **Top K items:** 20 (for "Most Relevant" analyses)
- **Minimum frequency:** 2 (for trend analysis)
- **Current year:** 2025 (for citable years calculation)
- **Bradford zones:** Equal thirds distribution
- **Impact metrics:** h-index, g-index, m-index

---

## 📈 Key Findings

### Temporal Trends
- **Annual growth rate:** 9.05%
- **Peak publication year:** 2024 (29 articles)
- **Emerging topics:** Carbon dioxide, bioremediation, sustainability
- **Stable research themes:** Cultivation methods, bioconversion, extraction

### Collaboration Patterns
- **International co-authorship:** 26.17%
- **Single-country publications (SCP):** 73.83%
- **Multi-country publications (MCP):** 26.17%
- **Top collaborations:** India-Ireland, India-Portugal, India-UK

### Citation Impact
- **Most cited paper:** 1,638 citations
- **Average document age:** 5.32 years
- **Total references:** 18,487
- **Self-citation rate:** Calculated via local citation analysis

---

## 🔧 Customization

### Modifying Stopwords/Synonyms

Edit the CSV files to customize keyword filtering:

```csv
# stopwords.csv
microalga,microalgae,biomass,your_custom_stopword

# synonyms.csv
carbon dioxide,CO2,carbon emissions,greenhouse gas
your_term,synonym1,synonym2,synonym3
```

### Adding Custom Analyses

For Python workflow, extend `complete_analysis.py`:

```python
def gen_custom_analysis(self):
    """Your custom analysis"""
    # Your code here
    results = pd.DataFrame(...)
    return results

# Add to run_all():
self.results['CustomAnalysis'] = self.gen_custom_analysis()
```

For R workflow, extend `run_bibliometric_analysis.R`:

```r
export_custom_analysis <- function(data, output_path) {
  # Your code here
  results <- your_analysis(data)
  save_metric_csv(results, "CustomAnalysis.csv", output_path)
  return(results)
}
```

---

## ✅ Validation

### Verification Against Biblioshiny

Run verification to compare outputs:
```bash
python verify_analysis.py
```

**Validation results:**
- ✅ Perfect match: MainInfo, AnnualSciProd, MostRelSources, BradfordLaw
- ≈ Close match: AnnualCitPerYear, MostFreqWords, CorrAuthCountries

**Minor differences explained:**
1. Citable year calculation methodology
2. Keyword stopword/synonym application timing
3. Country extraction heuristics from affiliations

---

## 📚 Methodology

For complete methodological details, see [`METHODS.md`](METHODS.md).

Key points:
- Data collected from Web of Science, Scopus, and CAB Abstracts
- Systematic screening process (222 papers)
- Title normalization and matching
- Duplicate removal
- Comprehensive bibliometric analysis using bibliometrix
- Custom Python implementation for reproducibility
- Publication-quality visualizations

---

## 🐛 Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'wordcloud'"**
```bash
pip install wordcloud
```

**"File not found" error**
- Check paths in scripts match your directory structure
- Ensure you're running from project root directory

**Plots not generating**
- Install matplotlib: `pip install matplotlib seaborn`
- Check output/plots/ directory exists

**Different results from Biblioshiny**
- Minor differences are expected due to calculation methods
- Structure and trends should match closely
- See verification section for details

---

## 📝 Citation

If you use this workflow in your research, please cite:

**For bibliometrix package:**
```
Aria, M., & Cuccurullo, C. (2017). bibliometrix: An R-tool for comprehensive 
science mapping analysis. Journal of Informetrics, 11(4), 959-975.
https://doi.org/10.1016/j.joi.2017.08.007
```

**For Python implementation:**
```
This reproducible bibliometric analysis workflow
https://github.com/your-repo/reproducible-bibliometric-analysis
```

---

## 📧 Support

For questions or issues:
1. Check [METHODS.md](METHODS.md) for methodology details
2. Review [output/ANALYSIS_SUMMARY.md](output/ANALYSIS_SUMMARY.md) for results
3. See troubleshooting section above
4. Consult [bibliometrix documentation](https://www.bibliometrix.org/)

---

## 📄 License

This workflow is provided for academic and research purposes.

---

**Last Updated:** November 19, 2025  
**Version:** 2.0.0  
**Python Version:** 3.8+  
**R Version:** 4.2.0+  
**Dataset:** 214 papers (2009-2025)

---

## 🎉 Project Status

✅ **Data cleaning:** Complete  
✅ **All 28 analyses:** Generated  
✅ **All 15 plots:** Created  
✅ **Validation:** Verified against Biblioshiny  
✅ **Documentation:** Complete  

**Ready for publication and PhD thesis inclusion!**
