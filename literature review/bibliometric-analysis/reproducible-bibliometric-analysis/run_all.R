#!/usr/bin/env Rscript
# =============================================================================
# COMPLETE BIBLIOMETRIC ANALYSIS WORKFLOW
# =============================================================================
# This master script runs the complete workflow:
#   1. Data Wrangling: Extract filtered citations from raw data
#   2. Bibliometric Analysis: Generate all analysis outputs
#
# Usage:
#   Rscript run_all.R
#
# Or in R console:
#   source("run_all.R")
# =============================================================================

cat("\n")
cat("=============================================================================\n")
cat("COMPLETE BIBLIOMETRIC ANALYSIS WORKFLOW\n")
cat("=============================================================================\n")
cat("\n")

# Record start time
workflow_start <- Sys.time()

# =============================================================================
# STEP 1: DATA WRANGLING
# =============================================================================

cat("STEP 1/2: DATA WRANGLING\n")
cat("-----------------------------------------------------------------------------\n")
cat("Extracting filtered citations from raw data files...\n")
cat("\n")

tryCatch({
  source("wrangle_data.R")
  cat("\n")
  cat("✓ Data wrangling completed successfully\n")
}, error = function(e) {
  cat("\n")
  cat("✗ ERROR in data wrangling:\n")
  cat(paste("  ", e$message, "\n"))
  cat("\n")
  cat("Please fix the error and run again.\n")
  stop("Workflow stopped due to data wrangling error")
})

cat("\n")
Sys.sleep(1)  # Brief pause for readability

# =============================================================================
# STEP 2: BIBLIOMETRIC ANALYSIS
# =============================================================================

cat("\n")
cat("=============================================================================\n")
cat("STEP 2/2: BIBLIOMETRIC ANALYSIS\n")
cat("-----------------------------------------------------------------------------\n")
cat("Running comprehensive bibliometric analysis...\n")
cat("\n")

tryCatch({
  # Load configuration
  source("config.R")
  
  # Load and run analysis script
  source("run_bibliometric_analysis.R")
  
  # Execute main analysis
  results <- main()
  
  cat("\n")
  cat("✓ Bibliometric analysis completed successfully\n")
  
}, error = function(e) {
  cat("\n")
  cat("✗ ERROR in bibliometric analysis:\n")
  cat(paste("  ", e$message, "\n"))
  cat("\n")
  cat("Please fix the error and run again.\n")
  stop("Workflow stopped due to analysis error")
})

# =============================================================================
# WORKFLOW SUMMARY
# =============================================================================

workflow_end <- Sys.time()
total_time <- difftime(workflow_end, workflow_start, units = "secs")

cat("\n")
cat("=============================================================================\n")
cat("WORKFLOW COMPLETED SUCCESSFULLY!\n")
cat("=============================================================================\n")
cat("\n")
cat(paste("Total execution time:", round(total_time, 2), "seconds\n"))
cat("\n")
cat("Output locations:\n")
cat("  • Filtered data:  data/\n")
cat("  • Analysis results: output/\n")
cat("\n")
cat("Key output files:\n")
cat("  • data/filtered_data_biblioshiny_ready.xlsx\n")
cat("  • output/Full_Bibliometric_Report.xlsx\n")
cat("  • output/ANALYSIS_SUMMARY.txt\n")
cat("\n")
cat("Next steps:\n")
cat("  1. Review output/ANALYSIS_SUMMARY.txt for overview\n")
cat("  2. Open output/Full_Bibliometric_Report.xlsx for detailed results\n")
cat("  3. Check data/unmatched_papers.xlsx if match rate was < 100%\n")
cat("\n")
cat("=============================================================================\n")

# Return results invisibly if running interactively
if (interactive()) {
  invisible(results)
}

