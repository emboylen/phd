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
optional_packages <- c("wordcloud", "RColorBrewer", "igraph")

for (pkg in required_packages) {
  if (!require(pkg, character.only = TRUE, quietly = TRUE)) {
    cat(paste("Installing package:", pkg, "\n"))
    install.packages(pkg, dependencies = TRUE)
    library(pkg, character.only = TRUE)
  }
}

# Install optional packages for enhanced visualizations
for (pkg in optional_packages) {
  if (!require(pkg, character.only = TRUE, quietly = TRUE)) {
    tryCatch({
      install.packages(pkg, dependencies = TRUE)
      library(pkg, character.only = TRUE)
    }, error = function(e) {
      cat(paste("Optional package", pkg, "not installed:", e$message, "\n"))
    })
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

#' Generate and export visualizations
#'
#' @param data Filtered bibliometric data frame
#' @param results Bibliometric analysis results
#' @param summary_obj Summary object
#' @param output_path Output directory path
export_visualizations <- function(data, results, summary_obj, output_path) {
  if (!EXPORT_PLOTS) return(NULL)
  
  print_status("Generating visualizations...")
  
  # Create plots subdirectory
  plots_dir <- file.path(output_path, "plots")
  if (!dir.exists(plots_dir)) {
    dir.create(plots_dir, recursive = TRUE)
  }
  
  tryCatch({
    # 1. Annual Scientific Production
    print_status("  Plotting annual production...")
    png(file.path(plots_dir, "01_Annual_Production.png"), 
        width = PLOT_WIDTH, height = PLOT_HEIGHT, units = "in", res = PLOT_DPI)
    plot(results, k = TOP_K, pause = FALSE)
    dev.off()
    
    # 2. Most Productive Authors
    print_status("  Plotting top authors...")
    if (!is.null(summary_obj$MostRelAuthors) && nrow(summary_obj$MostRelAuthors) > 0) {
      png(file.path(plots_dir, "02_Top_Authors.png"), 
          width = PLOT_WIDTH, height = PLOT_HEIGHT, units = "in", res = PLOT_DPI)
      
      top_authors <- head(summary_obj$MostRelAuthors, 20)
      par(mar = c(5, 8, 4, 2))
      barplot(rev(as.numeric(top_authors$Articles)), 
              names.arg = rev(as.character(top_authors$Authors)),
              horiz = TRUE, las = 1, col = "steelblue",
              xlab = "Number of Articles",
              main = "Most Productive Authors")
      dev.off()
    }
    
    # 3. Most Relevant Sources
    print_status("  Plotting top sources...")
    if (!is.null(summary_obj$MostRelSources) && nrow(summary_obj$MostRelSources) > 0) {
      png(file.path(plots_dir, "03_Top_Sources.png"), 
          width = PLOT_WIDTH, height = PLOT_HEIGHT, units = "in", res = PLOT_DPI)
      
      top_sources <- head(summary_obj$MostRelSources, 15)
      par(mar = c(5, 22, 4, 2))  # Increased left margin from 18 to 22
      barplot(rev(as.numeric(top_sources$Articles)), 
              names.arg = rev(as.character(top_sources$Sources)),
              horiz = TRUE, las = 1, col = "coral",
              xlab = "Number of Articles",
              main = "Most Relevant Sources",
              cex.names = 0.75)  # Slightly smaller font for readability
      dev.off()
    }
    
    # 4. Most Cited Papers
    print_status("  Plotting most cited papers...")
    if (!is.null(summary_obj$MostCitedPapers) && nrow(summary_obj$MostCitedPapers) > 0) {
      png(file.path(plots_dir, "04_Most_Cited.png"), 
          width = PLOT_WIDTH, height = PLOT_HEIGHT, units = "in", res = PLOT_DPI)
      
      top_cited <- head(summary_obj$MostCitedPapers, 15)
      # Create short labels
      labels <- paste0(substr(as.character(top_cited$Paper), 1, 50), "...")
      par(mar = c(5, 22, 4, 2))  # Increased left margin from 18 to 22
      barplot(rev(as.numeric(top_cited$TC)), 
              names.arg = rev(labels),
              horiz = TRUE, las = 1, col = "darkgreen",
              xlab = "Total Citations",
              main = "Most Globally Cited Documents",
              cex.names = 0.65)  # Smaller font for long labels
      dev.off()
    }
    
    # 5. Country Production
    print_status("  Plotting country production...")
    if (!is.null(summary_obj$MostProdCountries) && nrow(summary_obj$MostProdCountries) > 0) {
      png(file.path(plots_dir, "05_Country_Production.png"), 
          width = PLOT_WIDTH, height = PLOT_HEIGHT, units = "in", res = PLOT_DPI)
      
      top_countries <- head(summary_obj$MostProdCountries, 20)
      par(mar = c(5, 10, 4, 2))  # Increased left margin from 8 to 10
      barplot(rev(as.numeric(top_countries$Articles)), 
              names.arg = rev(as.character(top_countries$Country)),
              horiz = TRUE, las = 1, col = "purple",
              xlab = "Number of Articles",
              main = "Scientific Production by Country",
              cex.names = 0.85)  # Slightly smaller font
      dev.off()
    }
    
    # 6. Word Cloud (if keywords available)
    print_status("  Creating word cloud...")
    if ("DE" %in% names(data) || "ID" %in% names(data)) {
      tryCatch({
        # Load stopwords and synonyms
        stopwords_list <- c()
        synonyms_map <- list()
        
        # Load stopwords if file exists
        if (file.exists("stopwords.csv")) {
          tryCatch({
            stopwords_raw <- readLines("stopwords.csv", warn = FALSE)
            # Parse comma-separated values from all lines
            stopwords_list <- tolower(trimws(unlist(strsplit(stopwords_raw, ","))))
            # Remove empty entries
            stopwords_list <- stopwords_list[stopwords_list != ""]
            print_status(paste("    Loaded", length(stopwords_list), "stopwords"))
          }, error = function(e) {
            print_status(paste("    Error loading stopwords:", e$message))
          })
        }
        
        # Load synonyms if file exists
        if (file.exists("synonyms.csv")) {
          tryCatch({
            synonyms_raw <- readLines("synonyms.csv", warn = FALSE)
            for (line in synonyms_raw) {
              if (nchar(trimws(line)) > 0) {
                terms <- tolower(trimws(unlist(strsplit(line, ","))))
                terms <- terms[terms != ""]  # Remove empty entries
                if (length(terms) > 1) {
                  # First term is the canonical form, map all others to it
                  canonical <- terms[1]
                  for (term in terms[-1]) {
                    synonyms_map[[term]] <- canonical
                  }
                }
              }
            }
            print_status(paste("    Loaded", length(synonyms_map), "synonym mappings"))
          }, error = function(e) {
            print_status(paste("    Error loading synonyms:", e$message))
          })
        }
        
        png(file.path(plots_dir, "06_Word_Cloud.png"), 
            width = PLOT_WIDTH, height = PLOT_HEIGHT, units = "in", res = PLOT_DPI)
        
        # Use Keywords Plus if available, otherwise Author Keywords
        keywords_field <- if ("ID" %in% names(data)) "ID" else "DE"
        
        # Extract and process keywords
        keywords <- unlist(strsplit(data[[keywords_field]], ";"))
        keywords <- tolower(trimws(keywords))
        keywords <- keywords[!is.na(keywords) & keywords != ""]
        
        # Apply synonym mapping
        if (length(synonyms_map) > 0) {
          keywords <- sapply(keywords, function(kw) {
            if (kw %in% names(synonyms_map)) {
              return(synonyms_map[[kw]])
            }
            return(kw)
          }, USE.NAMES = FALSE)
        }
        
        # Remove stopwords
        if (length(stopwords_list) > 0) {
          keywords <- keywords[!keywords %in% stopwords_list]
        }
        
        if (length(keywords) > 0) {
          keyword_freq <- table(keywords)
          keyword_freq <- sort(keyword_freq, decreasing = TRUE)
          keyword_freq <- head(keyword_freq, 100)
          
          # Use wordcloud if available, otherwise simple plot
          if (require(wordcloud, quietly = TRUE) && require(RColorBrewer, quietly = TRUE)) {
            wordcloud::wordcloud(names(keyword_freq), keyword_freq, 
                               max.words = 100, random.order = FALSE,
                               colors = RColorBrewer::brewer.pal(8, "Dark2"),
                               scale = c(4, 0.5))
            title(main = "Keyword Word Cloud (Refined)", cex.main = 1.5)
          } else {
            # Fallback: top keywords bar chart
            top_kw <- head(keyword_freq, 20)
            par(mar = c(5, 10, 4, 2))
            barplot(rev(top_kw), horiz = TRUE, las = 1, 
                   col = "orange", main = "Top Keywords (Refined)",
                   xlab = "Frequency")
          }
        }
        dev.off()
      }, error = function(e) {
        print_status(paste("    Word cloud generation skipped:", e$message))
      })
    }
    
    # 7. Author Production Over Time
    print_status("  Creating author production over time plot...")
    tryCatch({
      if ("AU" %in% names(data) && "PY" %in% names(data) && sum(!is.na(data$AU)) > 10 && sum(!is.na(data$PY)) > 5) {
        png(file.path(plots_dir, "07_Author_Production_Over_Time.png"), 
            width = PLOT_WIDTH, height = PLOT_HEIGHT, units = "in", res = PLOT_DPI, bg = "white")
        
        # Get top authors
        author_list <- unlist(strsplit(data$AU, FIELD_SEPARATOR))
        author_freq <- sort(table(author_list), decreasing = TRUE)
        top_10_authors <- names(head(author_freq, 10))
        
        # Create time series for top authors
        years <- sort(unique(data$PY[!is.na(data$PY)]))
        author_production <- matrix(0, nrow = length(top_10_authors), ncol = length(years))
        rownames(author_production) <- top_10_authors
        colnames(author_production) <- years
        
        for (i in 1:nrow(data)) {
          if (!is.na(data$PY[i]) && !is.na(data$AU[i])) {
            authors <- unlist(strsplit(data$AU[i], FIELD_SEPARATOR))
            year_idx <- which(years == data$PY[i])
            for (author in authors) {
              author_idx <- which(top_10_authors == author)
              if (length(author_idx) > 0 && length(year_idx) > 0) {
                author_production[author_idx, year_idx] <- author_production[author_idx, year_idx] + 1
              }
            }
          }
        }
        
        # Plot
        colors <- rainbow(length(top_10_authors))
        plot(years, rep(0, length(years)), type = "n", 
             ylim = c(0, max(author_production) + 1),
             xlab = "Year", ylab = "Number of Publications",
             main = "Top 10 Authors: Production Over Time")
        
        for (i in 1:length(top_10_authors)) {
          lines(years, author_production[i,], col = colors[i], lwd = 2)
          points(years, author_production[i,], col = colors[i], pch = 19)
        }
        
        legend("topleft", legend = top_10_authors, col = colors, lwd = 2, cex = 0.7)
        
        dev.off()
        print_status("    Author production over time plot created successfully")
      } else {
        print_status("    Skipping: insufficient author or year data")
      }
    }, error = function(e) {
      if (dev.cur() > 1) dev.off()
      print_status(paste("    Author production plot error:", e$message))
    })
    
    # 8. Source Growth Over Time
    print_status("  Creating source growth over time plot...")
    tryCatch({
      if ("SO" %in% names(data) && "PY" %in% names(data) && sum(!is.na(data$SO)) > 10 && sum(!is.na(data$PY)) > 5) {
        png(file.path(plots_dir, "08_Source_Growth_Over_Time.png"), 
            width = PLOT_WIDTH, height = PLOT_HEIGHT, units = "in", res = PLOT_DPI, bg = "white")
        
        # Get top sources
        source_freq <- sort(table(data$SO), decreasing = TRUE)
        top_5_sources <- names(head(source_freq, 5))
        
        # Create time series for top sources
        years <- sort(unique(data$PY[!is.na(data$PY)]))
        source_production <- matrix(0, nrow = length(top_5_sources), ncol = length(years))
        rownames(source_production) <- top_5_sources
        colnames(source_production) <- years
        
        for (i in 1:nrow(data)) {
          if (!is.na(data$PY[i]) && !is.na(data$SO[i])) {
            source_idx <- which(top_5_sources == data$SO[i])
            year_idx <- which(years == data$PY[i])
            if (length(source_idx) > 0 && length(year_idx) > 0) {
              source_production[source_idx, year_idx] <- source_production[source_idx, year_idx] + 1
            }
          }
        }
        
        # Plot
        colors <- c("red", "blue", "green", "purple", "orange")
        plot(years, rep(0, length(years)), type = "n", 
             ylim = c(0, max(source_production) + 1),
             xlab = "Year", ylab = "Number of Publications",
             main = "Top 5 Sources: Publication Growth Over Time")
        
        for (i in 1:length(top_5_sources)) {
          lines(years, source_production[i,], col = colors[i], lwd = 3)
          points(years, source_production[i,], col = colors[i], pch = 19, cex = 1.2)
        }
        
        # Truncate long source names for legend
        legend_labels <- ifelse(nchar(top_5_sources) > 40, 
                               paste0(substr(top_5_sources, 1, 37), "..."),
                               top_5_sources)
        legend("topleft", legend = legend_labels, col = colors, lwd = 3, cex = 0.8)
        
        dev.off()
        print_status("    Source growth over time plot created successfully")
      } else {
        print_status("    Skipping: insufficient source or year data")
      }
    }, error = function(e) {
      if (dev.cur() > 1) dev.off()
      print_status(paste("    Source growth plot error:", e$message))
    })
    
    # 9. Historical Direct Citation Network
    print_status("  Creating historical citation network...")
    tryCatch({
      if ("CR" %in% names(data) && sum(!is.na(data$CR)) > 10) {
        png(file.path(plots_dir, "09_Citation_Network.png"), 
            width = 12, height = 12, units = "in", res = PLOT_DPI)
        
        histResults <- histNetwork(data, min.citations = 5, sep = ";")
        
        net <- networkPlot(histResults$histData$NetMatrix, 
                          n = 20, 
                          Title = "Historical Direct Citation Network",
                          type = "auto",
                          size = TRUE,
                          labelsize = 1,
                          alpha = 0.7)
        dev.off()
      }
    }, error = function(e) {
      print_status(paste("    Citation network skipped:", e$message))
    })
    
    print_status(paste("Visualizations saved to:", plots_dir))
    
  }, error = function(e) {
    warning(paste("Error generating visualizations:", e$message))
  })
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
      graph = TRUE
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
  
  # 7. Generate visualizations
  export_visualizations(data, biblio_analysis$results, biblio_analysis$summary, output_path)
  
  # 8. Run and export additional analyses
  trend_results <- export_trend_analysis(data, output_path)
  thematic_results <- export_thematic_map(data, output_path)
  network_results <- export_collaboration_network(data, output_path)
  
  # 9. Generate trend visualization if available
  if (!is.null(trend_results) && !is.null(trend_results$graph)) {
    tryCatch({
      png(file.path(output_path, "plots", "10_Trend_Topics.png"), 
          width = PLOT_WIDTH, height = PLOT_HEIGHT, units = "in", res = PLOT_DPI)
      print(trend_results$graph)
      dev.off()
    }, error = function(e) {
      print_status(paste("Trend plot skipped:", e$message))
    })
  }
  
  # 10. Generate thematic map visualization if available
  if (!is.null(thematic_results) && !is.null(thematic_results$map)) {
    tryCatch({
      png(file.path(output_path, "plots", "11_Thematic_Map.png"), 
          width = 12, height = 10, units = "in", res = PLOT_DPI)
      plot(thematic_results$map)
      dev.off()
    }, error = function(e) {
      print_status(paste("Thematic map plot skipped:", e$message))
    })
  }
  
  # 11. Combine all results
  all_results <- list(
    data = data,
    results = biblio_analysis$results,
    summary = biblio_analysis$summary,
    trends = trend_results,
    thematic = thematic_results,
    network = network_results
  )
  
  # 12. Export combined Excel file
  export_combined_excel(all_results, output_path)
  
  # 13. Generate summary report
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

