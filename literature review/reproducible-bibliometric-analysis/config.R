# =============================================================================
# CONFIGURATION FILE FOR REPRODUCIBLE BIBLIOMETRIC ANALYSIS
# =============================================================================
# This file contains all parameters and settings for the bibliometric analysis.
# Modify these settings to customize the analysis for your dataset.
#
# Author: Generated Template
# Date: 2025-11-17
# =============================================================================

# -----------------------------------------------------------------------------
# INPUT DATA SETTINGS
# -----------------------------------------------------------------------------

# Path to your filtered bibliometric data file
# Supported formats: .xlsx, .csv, .RData
# The data should be in bibliometrix format (with columns like TI, AU, PY, etc.)
INPUT_FILE <- "data/filtered_data_biblioshiny_ready.xlsx"

# File format type: "excel", "csv", or "rdata"
INPUT_FORMAT <- "excel"

# -----------------------------------------------------------------------------
# OUTPUT SETTINGS
# -----------------------------------------------------------------------------

# Directory where all outputs will be saved
OUTPUT_DIR <- "output"

# Timestamp for unique output folders (set to TRUE for production runs)
USE_TIMESTAMP <- FALSE

# Export format options
EXPORT_CSV <- TRUE
EXPORT_EXCEL <- TRUE
EXPORT_PLOTS <- TRUE

# -----------------------------------------------------------------------------
# ANALYSIS PARAMETERS
# -----------------------------------------------------------------------------

# Number of top items to include in "Most Relevant" tables
TOP_K <- 20

# Year range for analysis (NULL = use all available years)
# Example: c(2015, 2024) to analyze only 2015-2024
YEAR_RANGE <- NULL

# -----------------------------------------------------------------------------
# TREND ANALYSIS SETTINGS
# -----------------------------------------------------------------------------

# Field for trend analysis
# Options: "ID" (Keywords Plus), "DE" (Author Keywords), "TI" (Title words)
TREND_FIELD <- "ID"

# Minimum frequency for keywords to be included in trends
TREND_MIN_FREQ <- 2

# Number of top trending items to analyze
TREND_N_ITEMS <- 5

# -----------------------------------------------------------------------------
# THEMATIC MAP SETTINGS
# -----------------------------------------------------------------------------

# Field for thematic map
# Options: "ID" (Keywords Plus), "DE" (Author Keywords)
THEMATIC_FIELD <- "ID"

# Maximum number of keywords to analyze
THEMATIC_N <- 250

# Minimum frequency for keywords to be included
THEMATIC_MIN_FREQ <- 5

# N-grams to consider (1 = single words, 2 = two-word phrases)
THEMATIC_NGRAMS <- 1

# Cluster size parameter (0.5 = default)
THEMATIC_SIZE <- 0.5

# Repulsion force for clustering (0.1 = default)
THEMATIC_REPULSION <- 0.1

# -----------------------------------------------------------------------------
# NETWORK ANALYSIS SETTINGS
# -----------------------------------------------------------------------------

# Type of collaboration network to analyze
# Options: "countries", "authors", "universities"
COLLAB_NETWORK_TYPE <- "countries"

# Minimum number of collaborations to include
COLLAB_MIN_EDGES <- 1

# -----------------------------------------------------------------------------
# ADVANCED SETTINGS
# -----------------------------------------------------------------------------

# Separator for multi-value fields (e.g., multiple authors)
FIELD_SEPARATOR <- ";"

# Remove duplicates based on title similarity
REMOVE_DUPLICATES <- TRUE

# Print progress messages
VERBOSE <- TRUE

# Maximum characters for Excel cells (Excel limit is 32767)
MAX_EXCEL_CHARS <- 32767

# =============================================================================
# CUSTOM OUTPUT FILES
# =============================================================================

# Define which analyses to run and their output filenames
ANALYSES <- list(
  main_info = list(enabled = TRUE, filename = "MainInfo.csv"),
  annual_production = list(enabled = TRUE, filename = "AnnualSciProd.csv"),
  country_production = list(enabled = TRUE, filename = "CountrySciProd.csv"),
  most_rel_sources = list(enabled = TRUE, filename = "MostRelSources.csv"),
  most_rel_authors = list(enabled = TRUE, filename = "MostRelAuthors.csv"),
  most_cited_docs = list(enabled = TRUE, filename = "MostGlobCitDocs.csv"),
  trend_topics = list(enabled = TRUE, filename = "TrendTopics.csv"),
  thematic_map = list(enabled = TRUE, filename = "ThematicMap.csv"),
  collaboration_net = list(enabled = TRUE, filename = "CollaborationStats.csv")
)

# =============================================================================
# VALIDATION FUNCTION
# =============================================================================

validate_config <- function() {
  errors <- character()
  
  # Check if input file exists
  if (!file.exists(INPUT_FILE)) {
    errors <- c(errors, paste("Input file not found:", INPUT_FILE))
  }
  
  # Check valid input format
  if (!INPUT_FORMAT %in% c("excel", "csv", "rdata")) {
    errors <- c(errors, "INPUT_FORMAT must be 'excel', 'csv', or 'rdata'")
  }
  
  # Check valid field options
  if (!TREND_FIELD %in% c("ID", "DE", "TI", "AB")) {
    errors <- c(errors, "TREND_FIELD must be 'ID', 'DE', 'TI', or 'AB'")
  }
  
  if (!THEMATIC_FIELD %in% c("ID", "DE")) {
    errors <- c(errors, "THEMATIC_FIELD must be 'ID' or 'DE'")
  }
  
  if (!COLLAB_NETWORK_TYPE %in% c("countries", "authors", "universities")) {
    errors <- c(errors, "COLLAB_NETWORK_TYPE must be 'countries', 'authors', or 'universities'")
  }
  
  # Return validation results
  if (length(errors) > 0) {
    stop(paste("Configuration errors:\n", paste(errors, collapse = "\n")))
  }
  
  return(TRUE)
}

# =============================================================================
# END OF CONFIGURATION
# =============================================================================

