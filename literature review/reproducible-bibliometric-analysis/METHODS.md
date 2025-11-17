# Bibliometric Analysis Methods

## Complete Methodological Description

This document provides a comprehensive description of the bibliometric analysis methods implemented in this reproducible workflow.

---

## 1. Data Collection and Screening

### 1.1 Database Sources
Bibliographic data were retrieved from three major scientific databases:
- **Web of Science (WoS)**: BibTeX format exports
- **Scopus**: CSV and BibTeX format exports  
- **CAB Abstracts**: ISI Web of Science plaintext format exports

### 1.2 Screening Process
A systematic screening process was conducted to identify relevant publications. Papers meeting inclusion criteria were recorded in a master screening list (LIT-REVIEW-SCREENED.xlsx) containing:
- Paper titles
- Publication year
- Journal source
- Authors
- DOI
- Inclusion/exclusion status
- Categorization and key findings

Only papers marked as `included=TRUE` were retained for bibliometric analysis (n=222 papers in screening list).

---

## 2. Data Wrangling and Integration

### 2.1 Data Import and Conversion
Raw bibliographic data files were imported and converted to a standardized format using the `bibliometrix` package (v4.0+) in R (v4.2.0+). The `convert2df()` function was used to parse different file formats:

- **Scopus files**: Processed with `dbsource="scopus"`, `format="csv"` or `format="bibtex"`
- **Web of Science files**: Processed with `dbsource="isi"`, `format="bibtex"`
- **CAB Abstracts files**: Processed with `dbsource="isi"`, `format="plaintext"`

### 2.2 Data Consolidation
Multiple export files from each database were merged using a custom function (`merge_with_all_columns()`) that:
1. Identified all unique field names across datasets
2. Added missing fields as NA values to ensure consistent structure
3. Combined datasets using row-binding (`rbind`)

This resulted in a comprehensive dataset of 8,641 raw citation records across 104 bibliometric fields.

### 2.3 Title Normalization and Matching
To match screened papers with raw citation data, a robust title normalization procedure was implemented:

**Normalization steps:**
1. Conversion to lowercase
2. Removal of leading and trailing whitespace
3. Consolidation of multiple spaces to single spaces
4. Removal of special characters and punctuation variations
5. Standardization of dash characters (em-dash, en-dash, hyphen)

**Matching strategy:**
- **Primary method**: Normalized title matching between screened list and raw data
- **Fallback method**: DOI matching for papers where title matching failed
- **Match validation**: Manual review of unmatched papers (exported to `unmatched_papers.xlsx`)

### 2.4 Duplicate Removal
Duplicate records were identified and removed based on normalized title comparison, retaining the first occurrence of each unique paper. This process removed 269 duplicate records.

### 2.5 Final Dataset Composition
The final filtered dataset comprised 223 unique records (from 222 screened papers + 1 near-duplicate variant), achieving a match rate of 100.5%.

---

## 3. Bibliometric Analysis

All bibliometric analyses were conducted using the `bibliometrix` package (Aria & Cuccurullo, 2017) in R.

### 3.1 Descriptive Statistics
The `biblioAnalysis()` function was used to calculate comprehensive bibliometric indicators:

**Document-level metrics:**
- Total documents
- Publication year range and timespan
- Document types (articles, reviews, etc.)
- Annual growth rate

**Source-level metrics:**
- Number of unique sources (journals, books)
- Most productive sources
- Source impact based on publication frequency

**Author-level metrics:**
- Total authors and author appearances
- Single-authored vs. multi-authored documents
- Co-authors per document
- Authors of single-authored documents
- Author fractionalization (accounting for multi-authorship)

**Citation metrics:**
- Total citations per document
- Average citations per document
- Average citations per year per document
- Normalized total citations (NTC)

**Content metrics:**
- Keywords Plus (ID field) frequency
- Author keywords (DE field) frequency
- Total references

**Collaboration metrics:**
- International co-authorship percentage
- Single country publications (SCP)
- Multiple country publications (MCP)
- MCP ratio by country

### 3.2 Temporal Analysis

**Annual scientific production:**
Time series analysis of publication frequency by year was conducted to identify research output trends and growth patterns.

**Trend topics analysis:**
The `fieldByYear()` function was used to analyze keyword evolution over time with the following parameters:
- Field: Keywords Plus (ID)
- Minimum frequency: 2 occurrences
- Number of items: Top 5 keywords per period
- Time span: Full dataset range (2008-2025)

This analysis identified emerging and declining research themes across the study period.

### 3.3 Thematic Analysis

**Thematic mapping:**
The `thematicMap()` function performed keyword clustering analysis to identify:
- **Motor themes**: High centrality and density (well-developed, important themes)
- **Niche themes**: Low centrality, high density (specialized, peripheral themes)
- **Emerging/declining themes**: Low centrality and density
- **Basic themes**: High centrality, low density (important but underdeveloped)

Parameters:
- Field: Keywords Plus (ID)
- Maximum keywords (n): 250
- Minimum frequency: 5 occurrences
- N-grams: 1 (single words)
- Cluster size: 0.5
- Repulsion factor: 0.1

### 3.4 Citation Network Analysis

**Historical direct citation network:**
The `histNetwork()` function constructed a citation network of seminal papers within the dataset using:
- Minimum citations threshold: 5 citations
- Separator: ";"
- Network type: Historical direct citations

This identified the intellectual structure and foundational works of the research field.

### 3.5 Keyword Refinement

**Stopword filtering:**
A custom stopwords list (`stopwords.csv`) was applied to remove common, non-informative terms from keyword analyses. The stopwords list included domain-specific terms deemed too general for meaningful analysis (e.g., "microalgae", "biofuel", "biomass").

**Synonym consolidation:**
A synonym mapping file (`synonyms.csv`) was used to consolidate variant terms to their canonical forms. This included:
- Spelling variations (e.g., "CO2" → "carbon dioxide")
- Plural/singular forms
- Acronym expansions
- Conceptual synonyms (e.g., "greenhouse gases" → "carbon dioxide")

This procedure enhanced the semantic consistency of keyword analyses and improved the interpretability of results.

---

## 4. Visualization Methods

### 4.1 Bar Charts
Horizontal bar charts were generated for:
- Top authors by publication count
- Top sources by article frequency
- Most globally cited documents
- Country production rankings

**Specifications:**
- Resolution: 300 DPI (publication quality)
- Dimensions: 12 × 8 inches
- Format: PNG with white background
- Color schemes: Distinct colors per metric type

**Layout adjustments:**
Left margins were increased (18-22 lines) to accommodate long journal names and document titles without truncation.

### 4.2 Time Series Plots

**Annual production:**
Line graphs showing publication trends over time, generated using the base R `plot()` function from `biblioAnalysis()` results.

**Author production over time:**
Multi-line plot tracking the top 10 most productive authors' publication output across years, using rainbow color scheme for differentiation.

**Source growth over time:**
Multi-line plot showing publication trends for the top 5 most relevant sources over the study period.

### 4.3 Word Cloud
Keyword word clouds were generated using the `wordcloud` package with the following specifications:
- Maximum words: 100
- Random order: FALSE (frequency-based layout)
- Color palette: RColorBrewer "Dark2" (8 colors)
- Scale: 4 to 0.5 (largest to smallest)
- Pre-processing: Stopword removal and synonym consolidation applied

### 4.4 Citation Network Visualization
Citation networks were visualized using the `networkPlot()` function with:
- Layout algorithm: Fruchterman-Reingold
- Node size: Proportional to citation frequency
- Edge width: Proportional to connection strength
- Transparency (alpha): 0.7
- Label size: 0.8-1.0 (depending on network density)

---

## 5. Software and Packages

### 5.1 Computing Environment
- **R version**: 4.2.0+
- **Operating system**: Windows 10/11
- **Execution**: Command-line via Rscript (reproducible, non-interactive)

### 5.2 R Packages (Required)
- `bibliometrix` (4.0+): Bibliometric analysis and visualization
- `readxl` (1.4.0+): Reading Excel files
- `writexl` (1.4.0+): Writing Excel files
- `dplyr` (1.1.0+): Data manipulation
- `ggplot2` (3.4.0+): Advanced plotting

### 5.3 R Packages (Optional)
- `wordcloud` (2.6+): Word cloud generation
- `RColorBrewer` (1.1-3+): Color palettes
- `igraph` (1.4.0+): Network analysis

### 5.4 Version Control and Reproducibility
All analyses were scripted in R with:
- Configuration parameters centralized in `config.R`
- Modular functions for each analysis type
- Comprehensive error handling and logging
- Timestamped execution logs
- Deterministic output (seed-based where applicable)

---

## 6. Data Export and Reporting

### 6.1 Tabular Outputs
All analytical results were exported in multiple formats:
- **CSV files**: Individual tables for each metric type
- **Excel workbook**: Multi-sheet comprehensive report (`Full_Bibliometric_Report.xlsx`)
- **Text summary**: Plain-text analysis overview (`ANALYSIS_SUMMARY.txt`)

### 6.2 Excel Formatting
Excel exports included special handling:
- String truncation to 32,767 characters (Excel cell limit)
- Proper encoding of special characters
- Sheet naming for easy navigation
- Header preservation

### 6.3 Output Organization
All outputs were organized in a structured directory:
```
output/
├── CSV files (individual metrics)
├── Full_Bibliometric_Report.xlsx (combined results)
├── ANALYSIS_SUMMARY.txt (overview)
└── plots/ (all visualizations)
```

---

## 7. Quality Control and Validation

### 7.1 Data Validation
- **Match rate verification**: 100.5% match rate between screened list and raw data
- **Duplicate checking**: Automated detection and removal of duplicate records
- **Field completeness**: Validation of required fields (TI, AU, PY, SO, etc.)
- **Unmatched papers tracking**: Export of unmatched records for manual review

### 7.2 Analysis Validation
- **Biblioshiny comparison**: Results verifiable via manual upload to biblioshiny GUI
- **Consistent parameters**: All analyses use identical settings across runs
- **Reproducibility**: Complete workflow executable via single command (`Rscript run_all.R`)

### 7.3 Visualization Quality Control
- **File size checking**: Automated validation of plot file sizes (>50 KB indicates successful generation)
- **Error logging**: Comprehensive logging of plot generation failures
- **Fallback methods**: Alternative visualizations when primary methods fail

---

## 8. Workflow Automation

### 8.1 Complete Pipeline
The entire workflow from raw data to final results was automated via `run_all.R`:

**Stage 1: Data Wrangling** (`wrangle_data.R`)
1. Load screened paper list
2. Import raw citation files from multiple databases
3. Normalize titles and DOIs
4. Match screened papers with raw data
5. Remove duplicates
6. Export filtered dataset

**Stage 2: Bibliometric Analysis** (`run_bibliometric_analysis.R`)
1. Load filtered dataset
2. Run comprehensive bibliometric analyses
3. Generate visualizations
4. Export tabular results
5. Create summary report

**Execution time**: Approximately 2-3 minutes for 223 papers

### 8.2 Configuration Management
All analysis parameters are centralized in `config.R`:
- Number of top items (TOP_K = 20)
- Year range filtering (optional)
- Trend analysis parameters
- Thematic map parameters
- Plot dimensions and resolution
- Enable/disable specific analyses

This allows for easy customization without modifying core analysis code.

---

## 9. Limitations and Considerations

### 9.1 Data Source Dependencies
- Results depend on completeness of database exports
- Missing fields (e.g., author affiliations) limit certain network analyses
- Database-specific formatting variations may affect field availability

### 9.2 Title Matching
- Normalized title matching achieves high accuracy but may miss papers with significant title variations
- DOI matching serves as fallback but requires DOI availability in both datasets

### 9.3 Keyword Analysis
- Keywords Plus (ID) and Author Keywords (DE) coverage varies by source
- Stopword and synonym lists require domain-specific customization
- Keyword co-occurrence networks depend on sufficient keyword overlap

### 9.4 Citation Data
- Citation counts reflect snapshot at time of export
- Self-citations are not distinguished from external citations
- Citation networks limited to papers citing other papers within the dataset

---

## 10. Reproducibility Statement

This analysis is fully reproducible. To replicate results:

1. **Data**: Use the provided `filtered_data_biblioshiny_ready.xlsx` (223 papers)
2. **Software**: R version 4.2.0+ with specified packages
3. **Execution**: Run `Rscript run_all.R` from project directory
4. **Verification**: Compare outputs with provided results or verify via biblioshiny upload

All analysis code, configuration files, and data are available in the project repository. The workflow adheres to FAIR principles (Findable, Accessible, Interoperable, Reusable) for computational research.

---

## References

Aria, M., & Cuccurullo, C. (2017). bibliometrix: An R-tool for comprehensive science mapping analysis. *Journal of Informetrics*, 11(4), 959-975. https://doi.org/10.1016/j.joi.2017.08.007

R Core Team (2022). R: A language and environment for statistical computing. R Foundation for Statistical Computing, Vienna, Austria. https://www.R-project.org/

---

## Citation

When using this methodology in publications, please cite:

1. The bibliometrix package (Aria & Cuccurullo, 2017)
2. R software (R Core Team, 2022)
3. This analysis workflow (if publicly available)

---

*Document Version: 1.0*  
*Last Updated: 2025-11-18*  
*Corresponding to: 223 papers, 2008-2025 timespan*

