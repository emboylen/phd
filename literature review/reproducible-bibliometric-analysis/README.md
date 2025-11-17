# Reproducible Bibliometric Analysis

A production-ready, fully automated template for performing bibliometric analysis on filtered citation data. This tool replicates the functionality of [biblioshiny](https://www.bibliometrix.org/home/index.php/layout/biblioshiny) in a reproducible, scriptable manner.

## 📋 Overview

This template automates the entire bibliometric analysis workflow:
- **Input**: Filtered bibliometric data (Excel, CSV, or RData)
- **Processing**: Comprehensive bibliometric analyses using the `bibliometrix` package
- **Output**: Publication-ready tables, statistics, and reports

### Key Features

✅ **Fully Reproducible** - All analyses run via script, no manual GUI interactions  
✅ **Configurable** - All parameters centralized in `config.R`  
✅ **Modular** - Clean, well-documented functions following senior R developer standards  
✅ **Comprehensive** - Replicates all major biblioshiny outputs  
✅ **Flexible** - Works with any bibliometric dataset in standard format  

---

## 🚀 Quick Start

### 1. Prerequisites

Ensure you have R (≥ 4.0.0) installed with the following packages:
```r
install.packages(c("bibliometrix", "writexl", "readxl", "dplyr", "ggplot2"))
```

### 2. Setup Your Data

Place your filtered bibliometric data file in the `data/` directory:
```
reproducible-bibliometric-analysis/
├── data/
│   └── your_filtered_data.xlsx  # Your input file here
├── config.R
├── run_bibliometric_analysis.R
└── README.md
```

### 3. Configure Analysis

Edit `config.R` to point to your data file:
```r
INPUT_FILE <- "data/your_filtered_data.xlsx"
INPUT_FORMAT <- "excel"  # or "csv" or "rdata"
```

### 4. Run Analysis

#### Option A: Command Line (Recommended for Reproducibility)
```bash
Rscript run_bibliometric_analysis.R
```

#### Option B: Interactive R Session
```r
source("config.R")
source("run_bibliometric_analysis.R")
main()
```

### 5. View Results

All outputs are saved in the `output/` directory:
```
output/
├── MainInfo.csv
├── AnnualSciProd.csv
├── MostRelSources.csv
├── MostRelAuthors.csv
├── MostGlobCitDocs.csv
├── TrendTopics.csv
├── ThematicMap.csv
├── CollaborationStats.csv
├── Full_Bibliometric_Report.xlsx  # All results in one file
└── ANALYSIS_SUMMARY.txt           # Summary report
```

---

## 📊 Analyses Performed

| Analysis | Output File | Description |
|----------|-------------|-------------|
| **Main Information** | `MainInfo.csv` | Basic metadata: total docs, sources, authors, keywords |
| **Annual Production** | `AnnualSciProd.csv` | Publications per year |
| **Country Production** | `CountrySciProd.csv` | Scientific production by country |
| **Most Relevant Sources** | `MostRelSources.csv` | Top journals/sources by publication count |
| **Most Relevant Authors** | `MostRelAuthors.csv` | Top authors by publication count |
| **Most Cited Documents** | `MostGlobCitDocs.csv` | Highest cited papers in dataset |
| **Trend Topics** | `TrendTopics.csv` | Keyword frequency trends over time |
| **Thematic Map** | `ThematicMap.csv` | Keyword clusters (centrality & density) |
| **Collaboration Network** | `CollaborationStats.csv` | Network statistics for collaborations |

---

## ⚙️ Configuration Options

### Basic Settings

```r
# Input file
INPUT_FILE <- "data/filtered_data.xlsx"
INPUT_FORMAT <- "excel"  # "excel", "csv", or "rdata"

# Output settings
OUTPUT_DIR <- "output"
USE_TIMESTAMP <- FALSE  # TRUE to create timestamped subdirectories
EXPORT_CSV <- TRUE
EXPORT_EXCEL <- TRUE
```

### Analysis Parameters

```r
# Number of top items in "Most Relevant" tables
TOP_K <- 20

# Year range filter (NULL = all years)
YEAR_RANGE <- NULL  # or c(2015, 2024) for specific range

# Trend analysis settings
TREND_FIELD <- "ID"  # "ID" (Keywords Plus), "DE" (Author Keywords), "TI" (Title)
TREND_MIN_FREQ <- 2
TREND_N_ITEMS <- 5

# Thematic map settings
THEMATIC_FIELD <- "ID"
THEMATIC_N <- 250
THEMATIC_MIN_FREQ <- 5

# Collaboration network type
COLLAB_NETWORK_TYPE <- "countries"  # "countries", "authors", or "universities"
```

### Enable/Disable Specific Analyses

```r
ANALYSES <- list(
  main_info = list(enabled = TRUE, filename = "MainInfo.csv"),
  annual_production = list(enabled = TRUE, filename = "AnnualSciProd.csv"),
  trend_topics = list(enabled = TRUE, filename = "TrendTopics.csv"),
  # ... etc
)
```

---

## 📁 Data Format Requirements

Your input data must be in **bibliometrix format** with standard field codes:

| Field Code | Description |
|------------|-------------|
| `TI` | Title |
| `AU` | Authors |
| `PY` | Publication Year |
| `SO` | Source (Journal) |
| `AB` | Abstract |
| `DE` | Author Keywords |
| `ID` | Keywords Plus |
| `TC` | Total Citations |
| `CR` | Cited References |

### Converting Raw Data

If you have raw citation data (not yet filtered), use the data wrangling workflow:

```r
# Example: Convert and filter data
library(bibliometrix)

# Load raw data
raw_data <- convert2df("raw_export.bib", dbsource = "isi", format = "bibtex")

# Filter by your screening criteria
filtered_data <- raw_data[raw_data$TI %in% your_screened_titles, ]

# Export for analysis
library(writexl)
write_xlsx(filtered_data, "data/filtered_data.xlsx")
```

---

## 🔧 Customization

### Adding Custom Analyses

Add your own analysis functions following this pattern:

```r
#' Custom analysis function
#'
#' @param data Filtered bibliometric data frame
#' @param output_path Output directory path
export_custom_analysis <- function(data, output_path) {
  print_status("Running custom analysis...")
  
  # Your analysis code here
  results <- your_analysis_function(data)
  
  # Save results
  save_metric_csv(results, "CustomAnalysis.csv", output_path)
  
  return(results)
}
```

Then call it in the `main()` function:
```r
# Add to main() function
custom_results <- export_custom_analysis(data, output_path)
```

### Modifying Output Formats

To change CSV delimiter or add additional export formats:

```r
# Example: Export as tab-separated
save_metric_csv <- function(data, filename, output_dir) {
  filepath <- file.path(output_dir, filename)
  write.table(data, filepath, sep = "\t", row.names = FALSE)
}
```

---

## 🎯 Use Cases

### 1. Systematic Literature Reviews
Analyze your screened citations to identify:
- Most influential papers and authors
- Emerging research trends
- Collaboration patterns

### 2. Research Domain Mapping
Generate thematic maps to understand:
- Core vs. peripheral topics
- Research cluster relationships
- Evolution of research themes

### 3. Comparative Studies
Run the same analysis on multiple datasets:
```bash
# Configure for dataset 1
Rscript run_bibliometric_analysis.R

# Update config.R for dataset 2
Rscript run_bibliometric_analysis.R
```

### 4. Longitudinal Analysis
Track research evolution over time:
```r
# Analyze by time periods
YEAR_RANGE <- c(2015, 2019)  # Period 1
# Run analysis...

YEAR_RANGE <- c(2020, 2024)  # Period 2
# Run analysis...
```

---

## 🐛 Troubleshooting

### Common Issues

**Error: "Input file not found"**
- Check that `INPUT_FILE` path in `config.R` is correct
- Ensure file is in the `data/` directory

**Error: "Package not found"**
- Install missing packages: `install.packages("package_name")`

**Warning: "Trend analysis failed"**
- Check that your data has the required field (e.g., `ID` for Keywords Plus)
- Reduce `TREND_MIN_FREQ` if you have a small dataset

**Empty outputs**
- Verify your data is in bibliometrix format
- Check that required columns exist (run `names(your_data)`)

### Data Quality Issues

**Low keyword coverage**
- Some sources don't include Keywords Plus (`ID` field)
- Use `TREND_FIELD <- "DE"` for Author Keywords instead

**Missing citations**
- Not all databases export citation counts
- Focus on structural analyses (sources, authors, trends) instead

---

## 📚 Additional Resources

- [bibliometrix Documentation](https://www.bibliometrix.org/)
- [bibliometrix Tutorial](https://bibliometrix.org/vignettes/Introduction_to_bibliometrix.html)
- [Aria & Cuccurullo (2017). bibliometrix: An R-tool for comprehensive science mapping analysis](https://doi.org/10.1016/j.joi.2017.08.007)

---

## 📝 Citation

If you use this template in your research, please cite:

```
Aria, M. & Cuccurullo, C. (2017). bibliometrix: An R-tool for comprehensive 
science mapping analysis. Journal of Informetrics, 11(4), 959-975.
https://doi.org/10.1016/j.joi.2017.08.007
```

---

## 🤝 Contributing

Suggestions and improvements welcome! This template is designed to be:
- **Clear**: Well-documented code
- **Concise**: No unnecessary complexity
- **Supportable**: Easy to maintain and extend
- **Maintainable**: Follows R best practices

---

## 📄 License

This template is provided as-is for academic and research purposes.

---

## 📧 Support

For issues or questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review [bibliometrix documentation](https://www.bibliometrix.org/)
3. Consult your R environment documentation

---

**Last Updated**: 2025-11-17  
**Version**: 1.0.0  
**R Version Required**: ≥ 4.0.0

