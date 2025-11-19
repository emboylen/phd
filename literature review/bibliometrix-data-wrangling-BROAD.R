# Load necessary libraries for bibliometric and data handling
library(revtools)      # Tools for systematic reviews
library(bibliometrix)  # Bibliometric analysis and data conversion (convert2df)
library(writexl)       # Export data frames to Excel format

#bibliometrix::biblioshiny()

# -----------------------------------------------------------------------------
# Load screened lists containing selected studies (broad and scoping)
# These are CSV files with filtered bibliometric records
# ----------------------------------------------------------------------------
screened_umbrella <- read.csv("umbrella.csv", stringsAsFactors = FALSE)
screened_broad  <- read.csv("broad.csv", stringsAsFactors = FALSE)  # to be updated as still reading

# -----------------------------------------------------------------------------
# Define file paths to the bibliometric data files (various formats and sources)
# -----------------------------------------------------------------------------

# Set working directory to folder containing raw data files
setwd("C:/Users/")

# Umbrella review raw data  
scholar         <- "scholar.enw"              # EndNote file from Scholar
scopus_umbrella <- "scopus-umbrella.csv"
cab_umbrella    <- "cab-umbrella.txt" # CAB files (ISI format, plaintext)
wos_umbrella  <- "wos-umbrella.bib" # Web of Science (WOS) files (.bib format)

### Now broad review raw data
scopus_broad  <- "scopus.csv"       # Scopus csv files
cab_broad     <- "cab.txt" 
cab_broad_1     <- "cab(1).txt" 
cab_broad_2     <- "cab(2).txt" 
wos_broad_1 <- "wos(1).bib"
wos_broad_2 <- "wos(2).bib"
wos_broad_3 <- "wos(3).bib"
wos_broad_4 <- "wos(4).bib"
wos_broad   <- "wos.bib"


# -----------------------------------------------------------------------------
# Convert raw bibliometric files into data frames for analysis
# Using bibliometrix::convert2df() which standardizes formats
# -----------------------------------------------------------------------------

# Convert CAB files (database source "isi", plaintext format)
data_cab_umbrella <- convert2df(cab_umbrella, dbsource = "isi", format = "plaintext")
data_cab_broad  <- convert2df(cab_broad, dbsource = "isi", format = "plaintext")
data_cab_broad_1  <- convert2df(cab_broad_1, dbsource = "isi", format = "plaintext")
data_cab_broad_2  <- convert2df(cab_broad_2, dbsource = "isi", format = "plaintext")


# Convert Scholar and Scopus files (Scopus CSV files)
# Note: Scholar file commented out because convert2df may require format matching
# data_scholar <- convert2df(scholar, dbsource = "wos", format = "endnote")
data_scopus_umbrella <- convert2df(scopus_umbrella, dbsource = "scopus", format = "csv")
data_scopus_broad  <- convert2df(scopus_broad, dbsource = "scopus", format = "csv")


# Convert Web of Science (ISI source, bibtex format) files: multiple parts of broad and umbrella
data_wos_umbrella  <- convert2df(wos_umbrella, dbsource = "isi", format = "bibtex")
data_wos_broad_1 <- convert2df(wos_broad_1, dbsource = "isi", format = "bibtex")
data_wos_broad_2 <- convert2df(wos_broad_2, dbsource = "isi", format = "bibtex")
data_wos_broad_3 <- convert2df(wos_broad_3, dbsource = "isi", format = "bibtex")
data_wos_broad_4 <- convert2df(wos_broad_4, dbsource = "isi", format = "bibtex")
data_wos_broad    <- convert2df(wos_broad, dbsource = "isi", format = "bibtex")


# -----------------------------------------------------------------------------
# Helper function to merge multiple data frames by adding missing columns as NA
# Ensures all columns from all datasets are preserved in the combined data frame
# -----------------------------------------------------------------------------
merge_with_all_columns <- function(dfs) {
  # Get union of all column names across data frames
  all_columns <- unique(unlist(lapply(dfs, names)))
  
  # For each data frame, add missing columns filled with NA and reorder columns
  dfs_aligned <- lapply(dfs, function(df) {
    missing_cols <- setdiff(all_columns, names(df))
    for (col in missing_cols) {
      df[[col]] <- NA
    }
    df <- df[all_columns]
    return(df)
  })
  
  # Combine all data frames by rows (rbind)
  combined <- do.call(rbind, dfs_aligned)
  return(combined)
}

# -----------------------------------------------------------------------------
# Combine all imported bibliometric datasets into one master data frame
# This includes CAB, WOS (scoping + umbrella), and Scopus datasets
# -----------------------------------------------------------------------------
all_data_list <- list(
  data_cab_umbrella, 
  data_cab_broad, 
  data_cab_broad_1, 
  data_cab_broad_2,
  data_scopus_umbrella, 
  data_scopus_broad,
  data_wos_umbrella, 
  data_wos_broad_1, 
  data_wos_broad_2, 
  data_wos_broad_3, 
  data_wos_broad_4, 
  data_wos_broad
)

# Merge all datasets into one combined data frame, preserving all columns
data_full_combined <- merge_with_all_columns(all_data_list)


# Combine screened lists, removing duplicate entries
master_screened <- unique(rbind(screened_broad, screened_umbrella))

# -----------------------------------------------------------------------------
# Define helper function to normalize titles: lowercase and trim whitespace
# This ensures matching titles across datasets despite minor differences like case or spaces
# -----------------------------------------------------------------------------
normalize_titles <- function(x) {
  tolower(trimws(x))
}

# Normalize titles in screened master list
master_screened$Title_norm <- normalize_titles(master_screened$title)

# Normalize titles in the combined full dataset (bibliometrix uses column "TI" for title)
data_full_combined$Title_norm <- normalize_titles(data_full_combined$TI)

# -----------------------------------------------------------------------------
# Filter combined bibliometric data to keep only entries present in screened master list
# Matching done on normalized titles
# -----------------------------------------------------------------------------
filtered_data <- data_full_combined[data_full_combined$Title_norm %in% master_screened$Title_norm, ]

# Remove helper normalized title column after filtering
filtered_data$Title_norm <- NULL

# Remove duplicate entries based on normalized titles (if any remain)
filtered_data <- filtered_data[!duplicated(tolower(trimws(filtered_data$TI))), ]

# -----------------------------------------------------------------------------
# Export filtered bibliometric dataset for further analysis
# To CSV and Excel formats
# -----------------------------------------------------------------------------
write.csv(filtered_data, "filtered_data.csv", row.names = FALSE)
write_xlsx(filtered_data, "filtered_data.xlsx")

# -----------------------------------------------------------------------------
# Handle Excel-specific character limits in cells (max 32767 characters)
# Define function to truncate character fields exceeding this limit
# -----------------------------------------------------------------------------
max_excel_char <- 32767

truncate_excel_strings <- function(df) {
  for (col in names(df)) {
    if (is.character(df[[col]])) {
      # Truncate each cell if length exceeds maximum allowed in Excel
      df[[col]] <- sapply(df[[col]], function(x) {
        if (!is.na(x) && nchar(x) > max_excel_char) {
          substr(x, 1, max_excel_char)
        } else {
          x
        }
      }, USE.NAMES = FALSE)
    }
  }
  return(df)
}

# Apply truncation to filtered data before exporting for biblioshiny compatibility
filtered_data_truncated <- truncate_excel_strings(filtered_data)

# Export the truncated dataset as Excel file ready to import into biblioshiny
write_xlsx(filtered_data_truncated, "filtered_data_biblioshiny_ready.xlsx")

bibliometrix::biblioshiny()
Run TALL
library(tall)
tall()
