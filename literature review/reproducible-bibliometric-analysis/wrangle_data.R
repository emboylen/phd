# =============================================================================
# DATA WRANGLING: EXTRACT FILTERED CITATIONS FROM RAW DATA
# =============================================================================
# This script takes a screened list of papers and extracts the full 
# bibliometric records from raw citation export files.
#
# Workflow:
# 1. Load screened paper list
# 2. Import raw citation files from multiple databases (WoS, Scopus, CAB)
# 3. Combine all raw data
# 4. Match screened papers and extract full records
# 5. Export filtered dataset for bibliometric analysis
#
# Author: Generated Template
# Date: 2025-11-17
# =============================================================================

# Clear workspace
rm(list = ls())

# Load required libraries
cat("Loading required libraries...\n")
library(bibliometrix)
library(readxl)
library(writexl)

# =============================================================================
# CONFIGURATION
# =============================================================================

# Path to screened paper list
SCREENED_LIST_FILE <- "LIT-REVIEW-SCREENED.xlsx"

# Directory containing raw citation files
# Update this path if your raw data is in a different location
RAW_DATA_DIR <- "raw data"  # Folder named "raw data" in current directory

# Output files
OUTPUT_FILTERED_CSV <- "data/filtered_data.csv"
OUTPUT_FILTERED_XLSX <- "data/filtered_data.xlsx"
OUTPUT_BIBLIOSHINY_READY <- "data/filtered_data_biblioshiny_ready.xlsx"

# Excel character limit
MAX_EXCEL_CHARS <- 32767

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

#' Print status message with timestamp
print_status <- function(message) {
  timestamp <- format(Sys.time(), "%Y-%m-%d %H:%M:%S")
  cat(paste0("[", timestamp, "] ", message, "\n"))
}

#' Normalize titles for matching (lowercase, trim whitespace, remove extra spaces and special chars)
normalize_titles <- function(titles) {
  # Convert to lowercase
  titles <- tolower(titles)
  # Remove leading/trailing whitespace
  titles <- trimws(titles)
  # Replace multiple spaces with single space
  titles <- gsub("\\s+", " ", titles)
  # Remove common punctuation variations (various dashes)
  titles <- gsub("[\u2013\u2014\u2015\u002D]", " ", titles)
  # Remove special characters that might cause encoding issues
  titles <- gsub("[^[:alnum:][:space:]]", " ", titles)
  # Clean up any resulting multiple spaces
  titles <- gsub("\\s+", " ", titles)
  titles <- trimws(titles)
  return(titles)
}

#' Merge multiple data frames preserving all columns
merge_with_all_columns <- function(dfs) {
  # Get union of all column names
  all_columns <- unique(unlist(lapply(dfs, names)))
  
  # Align all data frames to have same columns
  dfs_aligned <- lapply(dfs, function(df) {
    missing_cols <- setdiff(all_columns, names(df))
    for (col in missing_cols) {
      df[[col]] <- NA
    }
    df <- df[all_columns]
    return(df)
  })
  
  # Combine by rows
  combined <- do.call(rbind, dfs_aligned)
  return(combined)
}

#' Truncate strings for Excel compatibility
truncate_excel_strings <- function(df) {
  for (col in names(df)) {
    if (is.character(df[[col]])) {
      df[[col]] <- sapply(df[[col]], function(x) {
        if (!is.na(x) && nchar(x) > MAX_EXCEL_CHARS) {
          substr(x, 1, MAX_EXCEL_CHARS)
        } else {
          x
        }
      }, USE.NAMES = FALSE)
    }
  }
  return(df)
}

# =============================================================================
# STEP 1: LOAD SCREENED PAPER LIST
# =============================================================================

print_status("Loading screened paper list...")

screened_list <- tryCatch({
  read_excel(SCREENED_LIST_FILE)
}, error = function(e) {
  stop(paste("Error loading screened list:", e$message))
})

print_status(paste("Loaded", nrow(screened_list), "screened papers"))
print_status(paste("Columns in screened list:", paste(names(screened_list), collapse = ", ")))

# Detect title column (common variations)
title_col <- NULL
for (col in c("title", "Title", "TITLE", "TI", "Article Title")) {
  if (col %in% names(screened_list)) {
    title_col <- col
    break
  }
}

if (is.null(title_col)) {
  stop("Cannot find title column. Available columns: ", paste(names(screened_list), collapse = ", "))
}

print_status(paste("Using title column:", title_col))

# Filter to only include papers where included=TRUE
if ("included" %in% names(screened_list)) {
  original_count <- nrow(screened_list)
  screened_list <- screened_list[screened_list$included == TRUE | screened_list$included == "TRUE", ]
  print_status(paste("Filtered to included papers:", nrow(screened_list), "of", original_count))
} else {
  print_status("WARNING: 'included' column not found. Using all screened papers.")
}

# Normalize screened titles for matching
screened_list$Title_norm <- normalize_titles(screened_list[[title_col]])

# Remove any empty titles
screened_list <- screened_list[!is.na(screened_list$Title_norm) & screened_list$Title_norm != "", ]

print_status(paste("Valid screened titles:", nrow(screened_list)))

# =============================================================================
# STEP 2: IMPORT RAW CITATION FILES
# =============================================================================

print_status("Importing raw citation files from multiple databases...")

# Define file paths (relative to RAW_DATA_DIR)
raw_files <- list(
  # Scopus files
  scopus_umbrella = list(path = "scopus-umbrella.csv", dbsource = "scopus", format = "csv"),
  scopus_broad_csv = list(path = "scopus.csv", dbsource = "scopus", format = "csv"),
  scopus_broad_bib = list(path = "scopus.bib", dbsource = "scopus", format = "bibtex"),
  scopus_broad_ris = list(path = "scopus.ris", dbsource = "scopus", format = "endnote"),
  
  # CAB Abstract files
  cab_umbrella = list(path = "cab-umbrella.txt", dbsource = "isi", format = "plaintext"),
  cab_broad = list(path = "cab.txt", dbsource = "isi", format = "plaintext"),
  cab_broad_1 = list(path = "cab(1).txt", dbsource = "isi", format = "plaintext"),
  cab_broad_2 = list(path = "cab(2).txt", dbsource = "isi", format = "plaintext"),
  
  # Web of Science files
  wos_umbrella = list(path = "wos-umbrella.bib", dbsource = "isi", format = "bibtex"),
  wos_broad = list(path = "wos.bib", dbsource = "isi", format = "bibtex"),
  wos_broad_1 = list(path = "wos(1).bib", dbsource = "isi", format = "bibtex"),
  wos_broad_2 = list(path = "wos(2).bib", dbsource = "isi", format = "bibtex"),
  wos_broad_3 = list(path = "wos(3).bib", dbsource = "isi", format = "bibtex"),
  wos_broad_4 = list(path = "wos(4).bib", dbsource = "isi", format = "bibtex")
)

# Import each file
all_data_list <- list()
import_count <- 0

for (file_name in names(raw_files)) {
  file_info <- raw_files[[file_name]]
  file_path <- file.path(RAW_DATA_DIR, file_info$path)
  
  # Check if file exists
  if (!file.exists(file_path)) {
    print_status(paste("WARNING: File not found, skipping:", file_path))
    next
  }
  
  # Import file
  tryCatch({
    print_status(paste("Importing:", file_info$path))
    data <- convert2df(file_path, 
                      dbsource = file_info$dbsource, 
                      format = file_info$format)
    
    if (!is.null(data) && nrow(data) > 0) {
      all_data_list[[file_name]] <- data
      import_count <- import_count + 1
      print_status(paste("  -> Loaded", nrow(data), "records"))
    }
  }, error = function(e) {
    print_status(paste("ERROR importing", file_info$path, ":", e$message))
  })
}

print_status(paste("Successfully imported", import_count, "files"))

if (length(all_data_list) == 0) {
  stop("No data files were successfully imported!")
}

# =============================================================================
# STEP 3: COMBINE ALL RAW DATA
# =============================================================================

print_status("Combining all raw citation data...")

data_full_combined <- merge_with_all_columns(all_data_list)

print_status(paste("Combined dataset:", nrow(data_full_combined), "total records"))
print_status(paste("Total fields:", ncol(data_full_combined)))

# =============================================================================
# STEP 4: MATCH AND FILTER
# =============================================================================

print_status("Matching screened papers with raw citation data...")

# Normalize titles in combined data
if (!"TI" %in% names(data_full_combined)) {
  stop("Column 'TI' (Title) not found in combined data. Cannot perform matching.")
}

data_full_combined$Title_norm <- normalize_titles(data_full_combined$TI)

# Method 1: Match by normalized title
matched_by_title <- data_full_combined[data_full_combined$Title_norm %in% screened_list$Title_norm, ]
print_status(paste("Matched by title:", nrow(matched_by_title), "records"))

# Method 2: Match by DOI (if DOI column exists)
matched_by_doi <- data.frame()
if ("doi" %in% tolower(names(screened_list)) && "DI" %in% names(data_full_combined)) {
  # Find DOI column in screened list
  doi_col <- names(screened_list)[tolower(names(screened_list)) == "doi"][1]
  
  # Normalize DOIs (remove spaces, lowercase, remove URL prefix)
  normalize_doi <- function(dois) {
    dois <- tolower(trimws(dois))
    dois <- gsub("https?://doi.org/", "", dois)
    dois <- gsub("https?://dx.doi.org/", "", dois)
    return(dois)
  }
  
  screened_doi_norm <- normalize_doi(screened_list[[doi_col]])
  data_doi_norm <- normalize_doi(data_full_combined$DI)
  
  # Match by DOI
  screened_doi_norm <- screened_doi_norm[!is.na(screened_doi_norm) & screened_doi_norm != ""]
  matched_by_doi <- data_full_combined[data_doi_norm %in% screened_doi_norm, ]
  print_status(paste("Matched by DOI:", nrow(matched_by_doi), "records"))
}

# Combine matches from both methods
if (nrow(matched_by_doi) > 0) {
  filtered_data <- rbind(matched_by_title, matched_by_doi)
  # Remove duplicates
  filtered_data <- filtered_data[!duplicated(filtered_data$Title_norm), ]
  print_status(paste("Combined matching (title + DOI):", nrow(filtered_data), "records"))
} else {
  filtered_data <- matched_by_title
}

print_status(paste("Matched", nrow(filtered_data), "of", nrow(screened_list), "screened papers"))

# Check match rate
match_rate <- round(nrow(filtered_data) / nrow(screened_list) * 100, 1)
print_status(paste("Match rate:", match_rate, "%"))

if (match_rate < 80) {
  warning(paste("Low match rate (", match_rate, "%). Check if title formats match between files."))
}

# Remove the normalized title column
filtered_data$Title_norm <- NULL

# Remove duplicates based on title
original_count <- nrow(filtered_data)
filtered_data <- filtered_data[!duplicated(normalize_titles(filtered_data$TI)), ]

if (nrow(filtered_data) < original_count) {
  print_status(paste("Removed", original_count - nrow(filtered_data), "duplicate records"))
}

print_status(paste("Final dataset:", nrow(filtered_data), "unique records"))

# =============================================================================
# STEP 5: EXPORT FILTERED DATA
# =============================================================================

print_status("Exporting filtered data...")

# Create data directory if it doesn't exist
if (!dir.exists("data")) {
  dir.create("data", recursive = TRUE)
}

# Export as CSV
write.csv(filtered_data, OUTPUT_FILTERED_CSV, row.names = FALSE)
print_status(paste("Saved:", OUTPUT_FILTERED_CSV))

# Export as Excel
write_xlsx(filtered_data, OUTPUT_FILTERED_XLSX)
print_status(paste("Saved:", OUTPUT_FILTERED_XLSX))

# Export biblioshiny-ready version (with truncated strings)
filtered_data_truncated <- truncate_excel_strings(filtered_data)
write_xlsx(filtered_data_truncated, OUTPUT_BIBLIOSHINY_READY)
print_status(paste("Saved:", OUTPUT_BIBLIOSHINY_READY))

# =============================================================================
# SUMMARY REPORT
# =============================================================================

cat("\n")
cat("=============================================================================\n")
cat("DATA WRANGLING SUMMARY\n")
cat("=============================================================================\n")
cat(paste("Screened papers loaded:", nrow(screened_list), "\n"))
cat(paste("Raw citation files imported:", import_count, "\n"))
cat(paste("Total raw records:", nrow(data_full_combined), "\n"))
cat(paste("Matched records:", nrow(filtered_data), "\n"))
cat(paste("Match rate:", match_rate, "%\n"))
cat("\n")
cat("Output files created:\n")
cat(paste("  -", OUTPUT_FILTERED_CSV, "\n"))
cat(paste("  -", OUTPUT_FILTERED_XLSX, "\n"))
cat(paste("  -", OUTPUT_BIBLIOSHINY_READY, "\n"))
cat("\n")
cat("Next steps:\n")
cat("  1. Review the match rate above\n")
cat("  2. Run bibliometric analysis: source('run_bibliometric_analysis.R')\n")
cat("=============================================================================\n")

# =============================================================================
# DIAGNOSTICS: Show unmatched papers (if any)
# =============================================================================

if (match_rate < 100) {
  cat("\n")
  cat("DIAGNOSTICS: Unmatched Papers\n")
  cat("-----------------------------------------------------------------------------\n")
  
  # Find titles in screened list but not in filtered data
  filtered_titles_norm <- normalize_titles(filtered_data$TI)
  unmatched <- screened_list[!screened_list$Title_norm %in% filtered_titles_norm, ]
  
  if (nrow(unmatched) > 0) {
    cat(paste("Number of unmatched papers:", nrow(unmatched), "\n"))
    cat("\n")
    cat("First 10 unmatched titles:\n")
    print(head(unmatched[[title_col]], 10))
    cat("\n")
    cat("Possible reasons:\n")
    cat("  - Title formatting differences (punctuation, spacing)\n")
    cat("  - Paper not present in raw citation exports\n")
    cat("  - Typos or errors in either screened list or raw data\n")
    cat("\n")
    
    # Export unmatched list for review
    write_xlsx(unmatched, "data/unmatched_papers.xlsx")
    cat("Exported unmatched papers to: data/unmatched_papers.xlsx\n")
  }
}

cat("\n")
print_status("Data wrangling completed successfully!")

