#!/usr/bin/env Rscript
# =============================================================================
# DETAILED DIAGNOSTIC: Title Matching Issues
# =============================================================================

library(readxl)
library(writexl)

cat("Analyzing title matching...\n\n")

# Load screened list
screened <- read_excel("LIT-REVIEW-SCREENED.xlsx")
screened_included <- screened[screened$included == TRUE | screened$included == "TRUE", ]

# Find title column
title_col <- NULL
for (col in c("title", "Title", "TITLE", "TI", "Article Title")) {
  if (col %in% names(screened_included)) {
    title_col <- col
    break
  }
}

# Normalize function
normalize_titles <- function(x) {
  tolower(trimws(x))
}

screened_included$Title_norm <- normalize_titles(screened_included[[title_col]])
screened_included <- screened_included[!is.na(screened_included$Title_norm) & screened_included$Title_norm != "", ]

# Load filtered data
filtered <- read_excel("data/filtered_data.xlsx")
filtered$Title_norm <- normalize_titles(filtered$TI)

# Find unmatched
unmatched <- screened_included[!screened_included$Title_norm %in% filtered$Title_norm, ]

cat("=============================================================================\n")
cat("TITLE MATCHING DIAGNOSTIC\n")
cat("=============================================================================\n\n")

cat(paste("Screened papers (included=TRUE):", nrow(screened_included), "\n"))
cat(paste("Matched in raw data:", nrow(filtered), "\n"))
cat(paste("Unmatched:", nrow(unmatched), "\n\n"))

# Show example of unmatched titles
cat("Sample of unmatched titles from screened list:\n")
cat("-----------------------------------------------------------------------------\n")
for (i in 1:min(5, nrow(unmatched))) {
  cat(paste0(i, ". ", unmatched[[title_col]][i], "\n"))
  cat(paste0("   Normalized: ", unmatched$Title_norm[i], "\n\n"))
}

# Try to find similar titles in raw data
cat("\nSearching for potential matches in raw data...\n")
cat("-----------------------------------------------------------------------------\n")

# Check first unmatched title
if (nrow(unmatched) > 0) {
  test_title <- unmatched$Title_norm[1]
  cat(paste0("Looking for: ", test_title, "\n\n"))
  
  # Find titles in raw data that contain key words from unmatched title
  words <- strsplit(test_title, " ")[[1]]
  words <- words[nchar(words) > 4]  # Only words longer than 4 chars
  
  if (length(words) > 0) {
    cat("Checking for titles containing key words:", paste(head(words, 3), collapse=", "), "\n")
    
    potential_matches <- filtered[grepl(words[1], filtered$Title_norm, fixed=TRUE), ]
    
    if (nrow(potential_matches) > 0) {
      cat("\nPotential matches found in raw data:\n")
      print(head(potential_matches$TI, 3))
    } else {
      cat("\nNo potential matches found with keyword:", words[1], "\n")
    }
  }
}

cat("\n")
cat("=============================================================================\n")
cat("CONCLUSION\n")
cat("=============================================================================\n")

if (nrow(unmatched) > 0) {
  cat("\nTitle matching is failing for some papers.\n")
  cat("\nPossible causes:\n")
  cat("  1. Titles in screened list have different formatting than raw exports\n")
  cat("  2. Special characters, punctuation, or encoding differences\n")
  cat("  3. Truncated titles in one dataset vs. full titles in another\n")
  cat("  4. Some papers genuinely not in the raw data files\n")
  cat("\n")
  cat("Exported full unmatched list to: data/MISSING_PAPERS.xlsx\n")
  cat("  - Check if titles look different between screened list and raw exports\n")
  cat("  - Consider using DOI matching instead of title matching\n")
} else {
  cat("\nAll papers matched successfully!\n")
}

cat("=============================================================================\n")

# Export unmatched with more details
write_xlsx(unmatched, "data/MISSING_PAPERS.xlsx")

