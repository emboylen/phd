#!/usr/bin/env Rscript
# =============================================================================
# DIAGNOSTIC: Find Missing Papers
# =============================================================================
# This script identifies which papers from your screened list are missing
# from the matched dataset.
# =============================================================================

library(readxl)
library(writexl)

cat("Loading data...\n")

# Load screened list
screened <- read_excel("LIT-REVIEW-SCREENED.xlsx")

# Filter to included papers
screened_included <- screened[screened$included == TRUE | screened$included == "TRUE", ]

# Normalize titles
normalize_titles <- function(x) {
  tolower(trimws(x))
}

# Find title column
title_col <- NULL
for (col in c("title", "Title", "TITLE", "TI", "Article Title")) {
  if (col %in% names(screened_included)) {
    title_col <- col
    break
  }
}

screened_included$Title_norm <- normalize_titles(screened_included[[title_col]])

# Load filtered data
filtered <- read_excel("data/filtered_data.xlsx")
filtered$Title_norm <- normalize_titles(filtered$TI)

# Find unmatched papers
unmatched <- screened_included[!screened_included$Title_norm %in% filtered$Title_norm, ]

cat("\n")
cat("=============================================================================\n")
cat("DIAGNOSTIC REPORT\n")
cat("=============================================================================\n")
cat(paste("Total screened papers (included=TRUE):", nrow(screened_included), "\n"))
cat(paste("Papers found in raw data:", nrow(filtered), "\n"))
cat(paste("Missing papers:", nrow(unmatched), "\n"))
cat("\n")

if (nrow(unmatched) > 0) {
  cat("First 10 missing papers:\n")
  cat("-----------------------------------------------------------------------------\n")
  print(head(unmatched[, c(title_col, "year", "journal")], 10))
  cat("\n")
  
  # Export all unmatched
  write_xlsx(unmatched, "data/MISSING_PAPERS.xlsx")
  cat("Full list exported to: data/MISSING_PAPERS.xlsx\n")
  cat("\n")
  cat("Possible reasons:\n")
  cat("  1. These papers weren't in your database exports\n")
  cat("  2. Title formatting differences between screened list and raw data\n")
  cat("  3. Papers may need to be downloaded separately\n")
} else {
  cat("All papers matched successfully!\n")
}

cat("=============================================================================\n")

