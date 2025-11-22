# Bibliometric Analysis Methods

## Complete Methodological Description

This document provides a comprehensive description of the bibliometric analysis methods implemented in this reproducible workflow, covering both the R-based (bibliometrix) and Python-based approaches.

---

## 1. Data Collection and Screening

### 1.1 Database Sources
Bibliographic data were retrieved from three major scientific databases:
- **Web of Science (WoS)**: BibTeX format exports (5 files)
- **Scopus**: CSV and BibTeX format exports
- **CAB Abstracts**: ISI Web of Science plaintext format exports (3 files)

**Search period:** 2008-2025  
**Raw records:** 8,641 citations across 104 bibliometric fields

### 1.2 Screening Process
A systematic screening process was conducted to identify relevant publications:
- **Screening tool:** Microsoft Excel (`LIT-REVIEW-SCREENED.xlsx`)
- **Inclusion criteria:** Domain-specific criteria for microalgae/biofuel research
- **Screening fields:** Title, year, journal, authors, DOI, inclusion status
- **Result:** 222 papers marked as included

### 1.3 Title Normalization and Matching
To match screened papers with raw citation data, a robust normalization procedure was implemented:

**Normalization steps:**
1. Conversion to lowercase
2. Removal of leading/trailing whitespace
3. Consolidation of multiple spaces
4. Removal of special characters and punctuation
5. Standardization of dash characters (em-dash, en-dash, hyphen)

**Matching strategy:**
- Primary: Normalized title matching
- Fallback: DOI matching where title failed
- Validation: Manual review of unmatched papers

**Match rate:** 100.5% (223 matches from 222 screened papers)

---

## 2. Data Cleaning and Preparation

### 2.1 Duplicate Removal
**Process:**
- Identification via normalized title comparison
- DOI-based duplicate detection
- Retention of first occurrence

**Results:**
- Original filtered dataset: 222 records
- Duplicates found: 1 DOI (10.1007/s10811-015-0720-4)
- Duplicate removed: 1 record

### 2.2 Empty Row Removal
**Process:**
- Identification of rows missing all key identifiers (SR, DI, TI, AU, PY)
- Automated removal of empty rows

**Results:**
- Empty rows found: 7
- Empty rows removed: 7

### 2.3 Final Dataset
**Characteristics:**
- **Total records:** 214 unique articles
- **Timespan:** 2009-2025 (17 years)
- **Sources:** 103 unique journals/books
- **Authors:** 1,006 unique researchers
- **Countries:** 40+ represented
- **Fields:** 104 bibliometric fields maintained

**Data quality checks:**
- ✅ No duplicate DOIs
- ✅ No empty rows
- ✅ All records have unique SR (row identifier)
- ✅ 100% valid year values
- ✅ All required fields present

---

## 3. Keyword Processing

### 3.1 Stopword Filtering
A custom stopwords list was created to remove non-informative terms from keyword analyses:

**Stopwords file:** `stopwords.csv`  
**Count:** 18 domain-specific terms  
**Examples:** microalga, microalgae, biomass, biofuels, biodiesel, biofuel production, biodiesel production, bioenergy, bioethanol, algae, microorganisms, microalgal biomass, biogas, priority journal

**Application:**
- Applied to both Keywords Plus (ID) and Author Keywords (DE)
- Filtered before counting frequencies
- Reduced noise in trend and word cloud analyses

### 3.2 Synonym Consolidation
A synonym mapping file was used to consolidate variant terms:

**Synonyms file:** `synonyms.csv`  
**Mappings:** 38 synonym groups  
**Examples:**
- "carbon dioxide" ← CO2, carbon emissions, greenhouse gas
- "sustainable development" ← sustainability, environmental sustainability
- "wastewater treatment" ← wastewater, waste water management, bioremediation
- "biotechnology" ← genetic engineering, bioengineering
- "life cycle" ← life cycle assessment, life cycle analysis

**Application methodology:**
- Terms mapped to primary (first) term in each group
- Applied after stopword filtering
- Increased keyword consistency and interpretability

---

## 4. Bibliometric Analysis

### 4.1 Dual Implementation Approach

**R-based Analysis (Traditional):**
- Package: `bibliometrix` v4.0+
- Functions: `biblioAnalysis()`, `thematicMap()`, `histNetwork()`, etc.
- Advantage: Standard methods, widely cited
- Limitation: GUI-dependent for some features

**Python-based Analysis (Reproducible):**
- Custom implementation matching bibliometrix algorithms
- Packages: pandas, numpy, collections
- Advantage: Fully scriptable, no GUI required
- Validation: Verified against Biblioshiny outputs

### 4.2 Core Analyses (28 Total)

#### Sheet 1: Main Information (MainInfo)
**Metrics calculated:**
- Timespan, sources, documents
- Annual growth rate (CAGR)
- Document average age
- Average citations per document
- Total references
- Unique keywords (ID and DE)
- Total authors and appearances
- Single vs. multi-authored documents
- Co-authors per document
- International co-authorship percentage
- Document types distribution

**Formula for annual growth rate:**
```
CAGR = ((N_final / N_first)^(1 / n_years) - 1) × 100
```

**Formula for international co-authorship:**
```
Intl_coauth_% = (Docs_with_multiple_countries / Total_docs) × 100
```

#### Sheet 2: Annual Scientific Production (AnnualSciProd)
**Method:**
- Group documents by publication year
- Count documents per year
- Sort chronologically

**Output:** Year, Articles

#### Sheet 3: Annual Citations per Year (AnnualCitPerYear)
**Metrics per year:**
- Mean total citations per article
- Number of documents (N)
- Mean citations per year
- Citable years

**Formula for mean citations per year:**
```
MeanTC_per_year = MeanTC_per_art / (Current_year - Publication_year)
```

**Current year:** 2025 (as of analysis date)

#### Sheets 4-5: Three Fields Plot (Empty)
Reserved for future network visualizations

#### Sheet 6: Most Relevant Sources (MostRelSources)
**Method:**
- Count articles per source (journal)
- Sort by frequency (descending)
- List all sources

**Output:** Sources, Articles

#### Sheet 7: Bradford's Law (BradfordLaw)
**Method:**
- Sort sources by publication frequency
- Calculate cumulative frequency
- Divide into three equal zones by cumulative frequency

**Zones defined:**
- Zone 1: Top sources (first third of cumulative publications)
- Zone 2: Middle sources (second third)
- Zone 3: Tail sources (final third)

**Output:** SO, Rank, Freq, cumFreq, Zone

#### Sheet 8: Source Local Impact (SourceLocImpact)
**Metrics per source:**
- **h-index:** Maximum h where source has h papers cited ≥h times each
- **g-index:** Maximum g where top g papers have ≥g² citations combined
- **m-index:** h-index / (current_year - first_publication_year)
- **TC:** Total citations
- **NP:** Number of papers
- **PY_start:** First publication year

**h-index algorithm:**
```python
citations_sorted = sorted(citations, reverse=True)
h = max([i for i, cit in enumerate(citations_sorted, 1) if cit >= i])
```

**g-index algorithm:**
```python
citations_sorted = sorted(citations, reverse=True)
cumsum = cumulative_sum(citations_sorted)
g = max([i for i, cum in enumerate(cumsum, 1) if cum >= i²])
```

#### Sheet 9: Source Production Over Time (SourceProdOverTime)
**Method:**
- Select top 5 sources by publication count
- Count publications per year for each source
- Create time series matrix

**Output:** Year, [Top 5 source names as columns]

#### Sheet 10: Most Relevant Authors (MostRelAuthors)
**Metrics:**
- **Articles:** Total count (integer)
- **Articles Fractionalized:** Credit distributed by authorship position

**Fractionalization formula:**
```
Fractional_credit = 1 / Number_of_coauthors
```

**Output:** Authors, Articles, Articles Fractionalized

#### Sheet 11: Author Production Over Time (AuthorProdOverTime)
**Method:**
- Select top 10 authors by publication count
- List all publications for each author chronologically
- Calculate TC per year for each paper

**Formula for TC per year:**
```
TCpY = TC / (Current_year - Publication_year)
```

**Output:** Author, year, TI, SO, DOI, TC, TCpY

#### Sheet 12: Lotka's Law (LotkaLaw)
**Method:**
- Count documents per author
- Calculate observed distribution
- Calculate theoretical Lotka distribution

**Lotka's Law formula:**
```
Proportion(n) = 1 / n² / Σ(1/i² for i=1 to max)
```

**Output:** Documents written, N. of Authors, Proportion of Authors, Theoretical

#### Sheet 13: Author Local Impact (AuthorLocImpact)
**Same metrics as SourceLocImpact:**
- h-index, g-index, m-index per author
- Based on citations of author's papers in dataset

#### Sheets 14-15: Affiliations
**Method:**
- Extract institutions from C1 (affiliation) field
- Parse by semicolon delimiter
- Extract institution name (before first comma)
- Count frequency and track over time

#### Sheets 16-19: Country Analyses
**Country extraction method:**
- Parse C1 (affiliation) field
- Match against 45+ country patterns
- Handle variants (e.g., "PEOPLES R CHINA" → "CHINA")

**Metrics:**
- **SCP:** Single-country publications
- **MCP:** Multi-country publications
- **MCP %:** (MCP / Total) × 100
- **Collaboration frequency:** Country pair co-occurrences

#### Sheets 20-21: Most Cited Documents
**Global citations:** TC field (from database)  
**Local citations:** Citations from within dataset (CR parsing)

**Normalized citations formula:**
```
Normalized_TC = TC / Mean_TC_for_same_year
```

#### Sheet 22: Most Local Cited References (MostLocCitRefs)
**Method:**
- Parse CR (cited references) field
- Split by semicolon
- Count reference frequencies across all documents

**Output:** Cited References, Citations

#### Sheets 23-24: Keyword Analyses
**Processing pipeline:**
1. Extract keywords from ID and DE fields
2. Split by semicolon
3. Convert to lowercase
4. Apply stopword filtering
5. Apply synonym consolidation
6. Count frequencies

**MostFreqWords:** All keywords sorted by frequency  
**WordCloud:** Top 50 keywords for visualization

#### Sheet 25: Trend Topics (TrendTopics)
**Method:**
- Collect publication years for each keyword
- Calculate quartiles (Q1, Median, Q3)
- Filter keywords with ≥5 occurrences

**Interpretation:**
- Low Q1: Recently emerging terms
- High Q3: Established terms
- Spread (Q3-Q1): Term evolution rate

#### Sheet 26: Co-Citation Network (CoCitNet)
**Simplified implementation:**
- Top 50 most cited references
- Network metrics: Betweenness, Closeness, PageRank
- Cluster assignment (simple grouping)

**Note:** Full network analysis requires graph algorithms (future enhancement)

#### Sheet 27: Historiograph
**Method:**
- Select highly cited papers (TC > 50)
- Extract metadata and keywords
- Calculate local citation score (LCS)
- Assign to clusters

**Output:** Paper, Title, Author_Keywords, KeywordsPlus, DOI, Year, LCS, GCS, cluster

#### Sheet 28: Collaboration World Map (CollabWorldMap)
**Method:**
- Extract countries from each document's affiliations
- Identify country pairs (multi-country papers)
- Count collaboration frequency

**Output:** From, To, Frequency

---

## 5. Visualization Methods

### 5.1 Technical Specifications
**Resolution:** 300 DPI (publication quality)  
**Format:** PNG with transparent or white background  
**Dimensions:** 12 × 6 to 16 × 10 inches (varying by plot type)  
**Color schemes:** 
- Distinct colors per analysis type
- Seaborn palettes for consistency
- Colorblind-friendly options

### 5.2 Plot Types

#### 5.2.1 Bar Charts
**Used for:**
- Most relevant sources, authors, countries
- Most frequent words
- Citation rankings

**Features:**
- Horizontal orientation for long labels
- Top 15-30 items displayed
- Clear axis labels and titles
- Grid lines for readability

#### 5.2.2 Time Series
**Used for:**
- Annual production
- Citations over time
- Source/author production trends

**Features:**
- Line plots with markers
- Dual-axis where appropriate
- Trend lines
- Clear legends

#### 5.2.3 Bradford's Law Scatter Plot
**Features:**
- Color-coded zones (green, orange, red)
- Cumulative frequency on y-axis
- Source rank on x-axis
- Zone boundaries visible

#### 5.2.4 Lotka's Law Log Plot
**Features:**
- Logarithmic y-axis
- Observed vs. theoretical comparison
- Clear markers for both series
- Grid for interpretation

#### 5.2.5 Word Cloud
**Specifications:**
- Package: `wordcloud` (Python)
- Max words: 50
- Color map: viridis
- Size: Proportional to frequency
- Layout: Frequency-based (not random)

#### 5.2.6 Trend Topics (Range Plot)
**Features:**
- Horizontal lines showing Q1-Q3 range
- Median marked with distinct symbol
- Terms sorted by frequency
- Time on x-axis, terms on y-axis

#### 5.2.7 Dual-Metric Plots
**Examples:**
- Total citations + Average citations per country
- Single vs. multi-country publications
- Articles + fractionalized articles for authors

**Features:**
- Dual x-axes or twin axes
- Distinct colors for each metric
- Clear legends

---

## 6. Software and Computing Environment

### 6.1 Python Environment
**Version:** Python 3.8+  
**OS:** Windows 10/11  
**Execution:** Command-line scripts

**Required packages:**
```
pandas==2.0+
numpy==1.24+
openpyxl==3.1+
matplotlib==3.7+
seaborn==0.12+
wordcloud==1.9+
```

**Installation:**
```bash
pip install pandas openpyxl numpy matplotlib seaborn wordcloud
```

### 6.2 R Environment (Optional)
**Version:** R 4.2.0+  
**Required packages:**
```r
bibliometrix (4.0+)
readxl (1.4.0+)
writexl (1.4.0+)
dplyr (1.1.0+)
ggplot2 (3.4.0+)
```

### 6.3 Reproducibility Features
**Python scripts:**
- Deterministic algorithms (no random seeds needed)
- Consistent sorting and ordering
- Fixed current year (2025) for calculations
- Identical parameter sets across runs

**Version control:**
- Git repository
- Documented code
- Changelog maintained

---

## 7. Quality Control and Validation

### 7.1 Data Validation Checks
✅ **No duplicate SR identifiers** (row names)  
✅ **No duplicate DOIs** (except intentionally removed)  
✅ **No empty rows** (all records have ≥1 key field)  
✅ **Valid year range** (2009-2025, no outliers)  
✅ **Source consistency** (journal names standardized)

### 7.2 Analysis Validation

**Method:** Comparison with Biblioshiny GUI outputs

**Verification script:** `verify_analysis.py`

**Results:**
- ✅ **Perfect match:** MainInfo, AnnualSciProd, MostRelSources, BradfordLaw, MostRelAuthors
- ≈ **Close match:** AnnualCitPerYear (±0.01 difference in averages)
- ≈ **Close match:** MostFreqWords (different stopword timing)
- ≈ **Close match:** CorrAuthCountries (country extraction variants)

**Acceptable differences explained:**
1. **Citable year calculation:** Python uses fixed 2025, Biblioshiny uses current date
2. **Keyword filtering order:** Stopwords applied before vs. after synonym mapping
3. **Country extraction:** Heuristic-based matching has minor variants

**Structural validation:** ✅ All sheets match expected format and column names

### 7.3 Plot Quality Control
**Automated checks:**
- File size >50 KB (indicates successful generation)
- File exists in output directory
- Error logging for failed plots

**Manual verification:**
- Visual inspection of all 15 plots
- Axis labels correct
- Data matches corresponding tables
- High resolution (300 DPI confirmed)

---

## 8. Workflow Automation

### 8.1 Python Pipeline
**Execution:**
```bash
# Complete workflow
python complete_analysis.py   # Generates all 28 analyses
python generate_all_plots.py  # Creates all 15 plots
python verify_analysis.py     # Validates against reference
```

**Execution time:** ~2-3 minutes for 214 papers

### 8.2 R Pipeline (Alternative)
**Execution:**
```bash
Rscript run_all.R   # Complete pipeline from raw data
# OR
Rscript run_bibliometric_analysis.R   # Analysis only (filtered data)
```

**Execution time:** ~3-5 minutes

### 8.3 Configuration Management
**Python:** Parameters embedded in scripts (easily modifiable)  
**R:** Centralized in `config.R` file

**Key parameters:**
- TOP_K = 20 (number of top items)
- CURRENT_YEAR = 2025 (for calculations)
- Stopwords file = "stopwords.csv"
- Synonyms file = "synonyms.csv"

---

## 9. Limitations and Considerations

### 9.1 Data-Related Limitations
- **Citation counts:** Snapshot at export time (not real-time)
- **Field availability:** Some records missing keywords or affiliations
- **Database coverage:** Limited to three databases (WoS, Scopus, CAB)
- **Language:** Primarily English-language publications

### 9.2 Methodological Considerations
- **Title matching:** 100.5% rate (1 near-duplicate variant included)
- **Country extraction:** Heuristic-based, may miss unconventional formats
- **Local citations:** Limited to citations within dataset
- **Keyword analysis:** Dependent on quality of database keyword assignment

### 9.3 Algorithm Differences
Python implementation approximates bibliometrix algorithms:
- **Core metrics:** Identical (counts, sums, averages)
- **Impact metrics:** h-index, g-index calculated identically
- **Network metrics:** Simplified (full graph analysis not implemented)
- **Thematic mapping:** Not implemented (complex clustering algorithm)

---

## 10. Reproducibility Statement

This analysis is **fully reproducible** with the following requirements:

### 10.1 Data Requirements
- **Input file:** `data/filtered_data_biblioshiny_ready.xlsx` (214 records)
- **Configuration:** `stopwords.csv` and `synonyms.csv`

### 10.2 Software Requirements
- Python 3.8+ with specified packages
- OR R 4.2.0+ with bibliometrix package

### 10.3 Execution
```bash
# Python workflow (recommended)
python complete_analysis.py
python generate_all_plots.py

# R workflow (alternative)
Rscript run_all.R
```

### 10.4 Expected Outputs
- `output/ReproducedBibliometricAnalysis.xlsx` (28 sheets)
- `output/plots/*.png` (15 PNG files)
- All outputs match provided reference within validation tolerances

### 10.5 FAIR Principles Compliance
- **Findable:** DOI assignable, GitHub repository
- **Accessible:** Open source scripts, standard formats
- **Interoperable:** Standard bibliometric formats, CSV/Excel outputs
- **Reusable:** Documented code, clear methodology, MIT license

---

## 11. References

### Primary Citations

Aria, M., & Cuccurullo, C. (2017). bibliometrix: An R-tool for comprehensive science mapping analysis. *Journal of Informetrics*, 11(4), 959-975. https://doi.org/10.1016/j.joi.2017.08.007

R Core Team (2022). R: A language and environment for statistical computing. R Foundation for Statistical Computing, Vienna, Austria. https://www.R-project.org/

### Software and Packages

- Python Software Foundation. (2023). Python Language Reference, version 3.8+. https://www.python.org
- McKinney, W. (2010). Data Structures for Statistical Computing in Python. *Proceedings of the 9th Python in Science Conference*, 56-61.
- Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & Engineering*, 9(3), 90-95.
- Waskom, M. (2021). seaborn: statistical data visualization. *Journal of Open Source Software*, 6(60), 3021.

### Bibliometric Methods

Bradford, S. C. (1934). Sources of information on specific subjects. *Engineering*, 137, 85-86.

Lotka, A. J. (1926). The frequency distribution of scientific productivity. *Journal of the Washington Academy of Sciences*, 16(12), 317-323.

Hirsch, J. E. (2005). An index to quantify an individual's scientific research output. *Proceedings of the National Academy of Sciences*, 102(46), 16569-16572.

---

## 12. Appendices

### Appendix A: Field Code Descriptions

| Code | Description | Source |
|------|-------------|--------|
| TI | Title | All databases |
| AU | Authors | All databases |
| AF | Author Full Names | WoS, Scopus |
| PY | Publication Year | All databases |
| SO | Source (Journal) | All databases |
| AB | Abstract | All databases |
| DE | Author Keywords | All databases |
| ID | Keywords Plus | WoS |
| TC | Total Citations | WoS, Scopus |
| CR | Cited References | WoS, Scopus |
| C1 | Author Affiliations | All databases |
| DI | DOI | All databases |
| NR | Number of References | WoS |

### Appendix B: Country Extraction Patterns

Full list of 45+ country patterns used for affiliation parsing available in source code (`complete_analysis.py`, `extract_country_from_c1()` function).

### Appendix C: Stopwords and Synonyms

Complete lists available in:
- `stopwords.csv` (18 terms)
- `synonyms.csv` (38 mappings, 120+ individual terms)

---

## 13. Citation

When using this methodology in publications, cite:

1. **For bibliometrix methods:** Aria & Cuccurullo (2017)
2. **For R software:** R Core Team (2022)
3. **For Python implementation:** This repository and workflow

**Recommended citation format:**
```
[Your Name]. (2025). Reproducible Bibliometric Analysis: Python and R workflows
for comprehensive science mapping. GitHub repository. 
https://github.com/your-username/reproducible-bibliometric-analysis
```

---

*Document Version: 2.0*  
*Last Updated: November 19, 2025*  
*Corresponding to: 214 papers, 2009-2025 timespan*  
*Analysis Date: November 19, 2025*

---

**End of Methods Document**
