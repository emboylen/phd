# =============================================================================
# EXAMPLE: Quick Start Configuration
# =============================================================================
# Copy this file to create custom configurations for different datasets
#
# This example shows how to analyze the filtered_data_biblioshiny_ready.xlsx
# file from the literature review screening process.
# =============================================================================

# Load this example with: source("config_example.R")

INPUT_FILE <- "data/filtered_data_biblioshiny_ready.xlsx"
INPUT_FORMAT <- "excel"

OUTPUT_DIR <- "output"
USE_TIMESTAMP <- FALSE

EXPORT_CSV <- TRUE
EXPORT_EXCEL <- TRUE
EXPORT_PLOTS <- TRUE

TOP_K <- 20

# Analyze publications from 2015 onwards
# YEAR_RANGE <- c(2015, 2024)
# Or analyze all years:
YEAR_RANGE <- NULL

TREND_FIELD <- "ID"        # Keywords Plus
TREND_MIN_FREQ <- 2
TREND_N_ITEMS <- 5

THEMATIC_FIELD <- "ID"     # Keywords Plus
THEMATIC_N <- 250
THEMATIC_MIN_FREQ <- 5
THEMATIC_NGRAMS <- 1
THEMATIC_SIZE <- 0.5
THEMATIC_REPULSION <- 0.1

COLLAB_NETWORK_TYPE <- "countries"
COLLAB_MIN_EDGES <- 1

FIELD_SEPARATOR <- ";"
REMOVE_DUPLICATES <- TRUE
VERBOSE <- TRUE
MAX_EXCEL_CHARS <- 32767

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

validate_config <- function() {
  errors <- character()
  
  if (!file.exists(INPUT_FILE)) {
    errors <- c(errors, paste("Input file not found:", INPUT_FILE))
  }
  
  if (!INPUT_FORMAT %in% c("excel", "csv", "rdata")) {
    errors <- c(errors, "INPUT_FORMAT must be 'excel', 'csv', or 'rdata'")
  }
  
  if (!TREND_FIELD %in% c("ID", "DE", "TI", "AB")) {
    errors <- c(errors, "TREND_FIELD must be 'ID', 'DE', 'TI', or 'AB'")
  }
  
  if (!THEMATIC_FIELD %in% c("ID", "DE")) {
    errors <- c(errors, "THEMATIC_FIELD must be 'ID' or 'DE'")
  }
  
  if (!COLLAB_NETWORK_TYPE %in% c("countries", "authors", "universities")) {
    errors <- c(errors, "COLLAB_NETWORK_TYPE must be 'countries', 'authors', or 'universities'")
  }
  
  if (length(errors) > 0) {
    stop(paste("Configuration errors:\n", paste(errors, collapse = "\n")))
  }
  
  return(TRUE)
}

