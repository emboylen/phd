# =============================================================================
# REPRODUCIBLE BIBLIOMETRIC ANALYSIS SCRIPT
# =============================================================================
# This script performs automated bibliometric analysis on filtered citation data,
# replicating the functionality of biblioshiny but in a fully reproducible manner.
#
# The script:
# 1. Loads filtered bibliometric data
# 2. Runs comprehensive bibliometric analyses
# 3. Exports results as CSV/Excel files
# 4. Generates publication-ready outputs
#
# Author: Generated Template
# Date: 2025-11-17
# =============================================================================

# -----------------------------------------------------------------------------
# SETUP AND INITIALIZATION
# -----------------------------------------------------------------------------

# Clear workspace (optional - comment out if running interactively)
# rm(list = ls())

# Load required libraries
cat("Loading required libraries...\n")

required_packages <- c("bibliometrix", "writexl", "readxl", "dplyr", "ggplot2")

for (pkg in required_packages) {
  if (!require(pkg, character.only = TRUE, quietly = TRUE)) {
    cat(paste("Installing package:", pkg, "\n"))
    install.packages(pkg, dependencies = TRUE)
    library(pkg, character.only = TRUE)
  }
}

# Load configuration file
source("config.R")

# Validate configuration
cat("Validating configuration...\n")
validate_config()

# -----------------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------------

#' Print status message with timestamp
#'
#' @param message Character string to print
#' @param verbose Logical indicating whether to print
print_status <- function(message, verbose = VERBOSE) {
  if (verbose) {
    timestamp <- format(Sys.time(), "%Y-%m-%d %H:%M:%S")
    cat(paste0("[", timestamp, "] ", message, "\n"))
  }
}

#' Save data to CSV file
#'
#' @param data Data frame to save
#' @param filename Output filename
#' @param output_dir Output directory path
save_metric_csv <- function(data, filename, output_dir) {
  if (EXPORT_CSV) {
    filepath <- file.path(output_dir, filename)
    write.csv(data, filepath, row.names = FALSE)
    print_status(paste("Saved:", filename))
  }
}

#' Truncate strings for Excel compatibility
#'
#' @param df Data frame to process
#' @return Data frame with truncated strings
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

#' Create output directory structure
#'
#' @return Path to output directory
setup_output_directory <- function() {
  # Create base output directory
  if (!dir.exists(OUTPUT_DIR)) {
    dir.create(OUTPUT_DIR, recursive = TRUE)
  }
  
  # Add timestamp subdirectory if enabled
  if (USE_TIMESTAMP) {
    timestamp <- format(Sys.time(), "%Y%m%d_%H%M%S")
    output_path <- file.path(OUTPUT_DIR, timestamp)
    dir.create(output_path, recursive = TRUE)
  } else {
    output_path <- OUTPUT_DIR
  }
  
  print_status(paste("Output directory:", output_path))
  return(output_path)
}

#' Load bibliometric data from file
#'
#' @param filepath Path to input file
#' @param format File format ("excel", "csv", or "rdata")
#' @return Data frame with bibliometric data
load_data <- function(filepath, format) {
  print_status(paste("Loading data from:", filepath))
  
  data <- tryCatch({
    if (format == "excel") {
      readxl::read_excel(filepath)
    } else if (format == "csv") {
      read.csv(filepath, stringsAsFactors = FALSE)
    } else if (format == "rdata") {
      load(filepath)
      get(ls()[1])  # Get first object in loaded environment
    } else {
      stop("Unsupported file format")
    }
  }, error = function(e) {
    stop(paste("Error loading data:", e$message))
  })
  
  # Convert to data frame if tibble
  data <- as.data.frame(data)
  
  print_status(paste("Loaded", nrow(data), "records with", ncol(data), "fields"))
  
  return(data)
}

#' Filter data by year range if specified
#'
#' @param data Bibliometric data frame
#' @param year_range Numeric vector of length 2 (start, end) or NULL
#' @return Filtered data frame
filter_by_year <- function(data, year_range) {
  if (!is.null(year_range) && length(year_range) == 2) {
    if ("PY" %in% names(data)) {
      original_count <- nrow(data)
      data <- data[data$PY >= year_range[1] & data$PY <= year_range[2], ]
      print_status(paste("Filtered to years", year_range[1], "-", year_range[2], 
                        ":", nrow(data), "of", original_count, "records retained"))
    } else {
      warning("Column 'PY' (Publication Year) not found. Skipping year filter.")
    }
  }
  return(data)
}

# -----------------------------------------------------------------------------
# MAIN ANALYSIS FUNCTIONS
# -----------------------------------------------------------------------------

#' Run bibliometric analysis using bibliometrix
#'
#' @param data Filtered bibliometric data frame
#' @return List containing analysis results and summary
run_bibliometric_analysis <- function(data) {
  print_status("Running bibliometric analysis...")
  
  # Run main analysis
  results <- biblioAnalysis(data, sep = FIELD_SEPARATOR)
  
  # Generate summary
  summary_obj <- summary(results, k = TOP_K, pause = FALSE)
  
  print_status("Bibliometric analysis completed")
  
  return(list(results = results, summary = summary_obj))
}

#' Export standard bibliometric tables
#'
#' @param summary_obj Summary object from biblioAnalysis
#' @param output_path Output directory path
export_standard_tables <- function(summary_obj, output_path) {
  print_status("Exporting standard bibliometric tables...")
  
  # Main Information
  if (ANALYSES$main_info$enabled) {
    if (!is.null(summary_obj$MainInformation)) {
      save_metric_csv(as.data.frame(summary_obj$MainInformation), 
                     ANALYSES$main_info$filename, output_path)
    }
  }
  
  # Annual Production
  if (ANALYSES$annual_production$enabled) {
    if (!is.null(summary_obj$AnnualProduction)) {
      save_metric_csv(summary_obj$AnnualProduction, 
                     ANALYSES$annual_production$filename, output_path)
    }
  }
  
  # Country Production
  if (ANALYSES$country_production$enabled) {
    if (!is.null(summary_obj$MostProdCountries)) {
      save_metric_csv(summary_obj$MostProdCountries, 
                     ANALYSES$country_production$filename, output_path)
    }
  }
  
  # Most Relevant Sources
  if (ANALYSES$most_rel_sources$enabled) {
    if (!is.null(summary_obj$MostRelSources)) {
      save_metric_csv(summary_obj$MostRelSources, 
                     ANALYSES$most_rel_sources$filename, output_path)
    }
  }
  
  # Most Relevant Authors
  if (ANALYSES$most_rel_authors$enabled) {
    if (!is.null(summary_obj$MostRelAuthors)) {
      save_metric_csv(summary_obj$MostRelAuthors, 
                     ANALYSES$most_rel_authors$filename, output_path)
    }
  }
  
  # Most Globally Cited Documents
  if (ANALYSES$most_cited_docs$enabled) {
    if (!is.null(summary_obj$MostCitedPapers)) {
      save_metric_csv(summary_obj$MostCitedPapers, 
                     ANALYSES$most_cited_docs$filename, output_path)
    }
  }
  
  print_status("Standard tables exported")
}

#' Perform and export trend analysis
#'
#' @param data Filtered bibliometric data frame
#' @param output_path Output directory path
export_trend_analysis <- function(data, output_path) {
  if (!ANALYSES$trend_topics$enabled) return(NULL)
  
  print_status("Performing trend analysis...")
  
  tryCatch({
    # Determine time span
    if (!is.null(YEAR_RANGE)) {
      timespan <- YEAR_RANGE
    } else {
      timespan <- c(min(data$PY, na.rm = TRUE), max(data$PY, na.rm = TRUE))
    }
    
    # Run trend analysis
    trends <- fieldByYear(
      data, 
      field = TREND_FIELD, 
      timespan = timespan,
      min.freq = TREND_MIN_FREQ, 
      n.items = TREND_N_ITEMS, 
      graph = FALSE
    )
    
    # Save results
    if (!is.null(trends$df)) {
      save_metric_csv(trends$df, ANALYSES$trend_topics$filename, output_path)
    }
    
    print_status("Trend analysis completed")
    return(trends)
    
  }, error = function(e) {
    warning(paste("Trend analysis failed:", e$message))
    return(NULL)
  })
}

#' Perform and export thematic map analysis
#'
#' @param data Filtered bibliometric data frame
#' @param output_path Output directory path
export_thematic_map <- function(data, output_path) {
  if (!ANALYSES$thematic_map$enabled) return(NULL)
  
  print_status("Performing thematic map analysis...")
  
  tryCatch({
    # Run thematic map analysis
    map_results <- thematicMap(
      data, 
      field = THEMATIC_FIELD, 
      n = THEMATIC_N, 
      minfreq = THEMATIC_MIN_FREQ, 
      ngrams = THEMATIC_NGRAMS, 
      size = THEMATIC_SIZE, 
      repulsion = THEMATIC_REPULSION
    )
    
    # Save map data
    if (!is.null(map_results$map)) {
      save_metric_csv(map_results$map, ANALYSES$thematic_map$filename, output_path)
    }
    
    # Save cluster data if available
    if (!is.null(map_results$clusters)) {
      save_metric_csv(map_results$clusters, "ThematicClusters.csv", output_path)
    }
    
    print_status("Thematic map analysis completed")
    return(map_results)
    
  }, error = function(e) {
    warning(paste("Thematic map analysis failed:", e$message))
    return(NULL)
  })
}

#' Perform and export collaboration network analysis
#'
#' @param data Filtered bibliometric data frame
#' @param output_path Output directory path
export_collaboration_network <- function(data, output_path) {
  if (!ANALYSES$collaboration_net$enabled) return(NULL)
  
  print_status(paste("Performing", COLLAB_NETWORK_TYPE, "collaboration network analysis..."))
  
  tryCatch({
    # Create network matrix
    net_matrix <- biblioNetwork(
      data, 
      analysis = "collaboration", 
      network = COLLAB_NETWORK_TYPE, 
      sep = FIELD_SEPARATOR
    )
    
    # Calculate network statistics
    net_stats <- networkStat(net_matrix)
    
    # Save network statistics
    if (!is.null(net_stats$vertex)) {
      save_metric_csv(net_stats$vertex, 
                     ANALYSES$collaboration_net$filename, output_path)
    }
    
    print_status("Collaboration network analysis completed")
    return(net_stats)
    
  }, error = function(e) {
    warning(paste("Collaboration network analysis failed:", e$message))
    return(NULL)
  })
}

#' Export all results to a single Excel file with multiple sheets
#'
#' @param all_results List of all analysis results
#' @param output_path Output directory path
export_combined_excel <- function(all_results, output_path) {
  if (!EXPORT_EXCEL) return(NULL)
  
  print_status("Creating combined Excel report...")
  
  tryCatch({
    # Prepare list of data frames for Excel sheets
    excel_list <- list()
    
    # Add available results
    if (!is.null(all_results$summary$MainInformation)) {
      excel_list[["Main Info"]] <- as.data.frame(all_results$summary$MainInformation)
    }
    
    if (!is.null(all_results$summary$AnnualProduction)) {
      excel_list[["Annual Production"]] <- truncate_excel_strings(all_results$summary$AnnualProduction)
    }
    
    if (!is.null(all_results$summary$MostRelSources)) {
      excel_list[["Most Rel Sources"]] <- truncate_excel_strings(all_results$summary$MostRelSources)
    }
    
    if (!is.null(all_results$summary$MostRelAuthors)) {
      excel_list[["Most Rel Authors"]] <- truncate_excel_strings(all_results$summary$MostRelAuthors)
    }
    
    if (!is.null(all_results$summary$MostCitedPapers)) {
      excel_list[["Most Cited Docs"]] <- truncate_excel_strings(all_results$summary$MostCitedPapers)
    }
    
    if (!is.null(all_results$trends$df)) {
      excel_list[["Trend Topics"]] <- truncate_excel_strings(all_results$trends$df)
    }
    
    if (!is.null(all_results$thematic$map)) {
      excel_list[["Thematic Map"]] <- truncate_excel_strings(all_results$thematic$map)
    }
    
    if (!is.null(all_results$network$vertex)) {
      excel_list[["Collaboration Net"]] <- truncate_excel_strings(all_results$network$vertex)
    }
    
    # Write to Excel
    if (length(excel_list) > 0) {
      excel_path <- file.path(output_path, "Full_Bibliometric_Report.xlsx")
      write_xlsx(excel_list, excel_path)
      print_status(paste("Combined Excel report saved:", excel_path))
    }
    
  }, error = function(e) {
    warning(paste("Failed to create combined Excel report:", e$message))
  })
}

#' Generate analysis summary report
#'
#' @param data Input data
#' @param analysis_results Analysis results
#' @param output_path Output directory path
generate_summary_report <- function(data, analysis_results, output_path) {
  print_status("Generating analysis summary...")
  
  summary_text <- c(
    "=============================================================================",
    "BIBLIOMETRIC ANALYSIS SUMMARY REPORT",
    "=============================================================================",
    paste("Analysis Date:", format(Sys.time(), "%Y-%m-%d %H:%M:%S")),
    paste("Input File:", INPUT_FILE),
    "",
    "--- DATASET OVERVIEW ---",
    paste("Total Documents:", nrow(data)),
    paste("Total Fields:", ncol(data)),
    ""
  )
  
  # Add year range if available
  if ("PY" %in% names(data)) {
    summary_text <- c(
      summary_text,
      paste("Year Range:", min(data$PY, na.rm = TRUE), "-", max(data$PY, na.rm = TRUE)),
      ""
    )
  }
  
  summary_text <- c(
    summary_text,
    "--- ANALYSES PERFORMED ---",
    paste("Main Information:", ifelse(ANALYSES$main_info$enabled, "Yes", "No")),
    paste("Annual Production:", ifelse(ANALYSES$annual_production$enabled, "Yes", "No")),
    paste("Source Analysis:", ifelse(ANALYSES$most_rel_sources$enabled, "Yes", "No")),
    paste("Author Analysis:", ifelse(ANALYSES$most_rel_authors$enabled, "Yes", "No")),
    paste("Citation Analysis:", ifelse(ANALYSES$most_cited_docs$enabled, "Yes", "No")),
    paste("Trend Analysis:", ifelse(ANALYSES$trend_topics$enabled, "Yes", "No")),
    paste("Thematic Map:", ifelse(ANALYSES$thematic_map$enabled, "Yes", "No")),
    paste("Collaboration Network:", ifelse(ANALYSES$collaboration_net$enabled, "Yes", "No")),
    "",
    "--- OUTPUT LOCATION ---",
    paste("Output Directory:", output_path),
    "",
    "=============================================================================",
    "Analysis completed successfully!",
    "============================================================================="
  )
  
  # Write summary to file
  summary_file <- file.path(output_path, "ANALYSIS_SUMMARY.txt")
  writeLines(summary_text, summary_file)
  
  # Print to console
  cat(paste(summary_text, collapse = "\n"), "\n")
}

# =============================================================================
# MAIN EXECUTION
# =============================================================================

main <- function() {
  # Start timing
  start_time <- Sys.time()
  
  print_status("=============================================================================")
  print_status("STARTING REPRODUCIBLE BIBLIOMETRIC ANALYSIS")
  print_status("=============================================================================")
  
  # 1. Setup output directory
  output_path <- setup_output_directory()
  
  # 2. Load data
  data <- load_data(INPUT_FILE, INPUT_FORMAT)
  
  # 3. Filter by year if specified
  data <- filter_by_year(data, YEAR_RANGE)
  
  # 4. Remove duplicates if enabled
  if (REMOVE_DUPLICATES && "TI" %in% names(data)) {
    original_count <- nrow(data)
    data <- data[!duplicated(tolower(trimws(data$TI))), ]
    if (nrow(data) < original_count) {
      print_status(paste("Removed", original_count - nrow(data), "duplicate records"))
    }
  }
  
  # 5. Run main bibliometric analysis
  biblio_analysis <- run_bibliometric_analysis(data)
  
  # 6. Export standard tables
  export_standard_tables(biblio_analysis$summary, output_path)
  
  # 7. Run and export additional analyses
  trend_results <- export_trend_analysis(data, output_path)
  thematic_results <- export_thematic_map(data, output_path)
  network_results <- export_collaboration_network(data, output_path)
  
  # 8. Combine all results
  all_results <- list(
    data = data,
    results = biblio_analysis$results,
    summary = biblio_analysis$summary,
    trends = trend_results,
    thematic = thematic_results,
    network = network_results
  )
  
  # 9. Export combined Excel file
  export_combined_excel(all_results, output_path)
  
  # 10. Generate summary report
  generate_summary_report(data, all_results, output_path)
  
  # Calculate execution time
  end_time <- Sys.time()
  execution_time <- difftime(end_time, start_time, units = "secs")
  
  print_status("=============================================================================")
  print_status(paste("ANALYSIS COMPLETED IN", round(execution_time, 2), "SECONDS"))
  print_status("=============================================================================")
  
  # Return results invisibly
  invisible(all_results)
}

# Run main function
if (!interactive()) {
  main()
} else {
  cat("\n")
  cat("=============================================================================\n")
  cat("REPRODUCIBLE BIBLIOMETRIC ANALYSIS SCRIPT LOADED\n")
  cat("=============================================================================\n")
  cat("\n")
  cat("To run the analysis, execute: main()\n")
  cat("\n")
  cat("To modify settings, edit 'config.R' before running.\n")
  cat("\n")
  cat("=============================================================================\n")
}

