# PhD Literature Review: Microalgae Biofuel Analysis

This project contains comprehensive analyses for a PhD literature review investigating why algae-based biofuel production has not achieved commercial viability despite showing promise.

## Research Question

**Why is algae not being used for biofuel production despite its potential?**

The research combines multiple analytical approaches to elucidate barriers and opportunities in microalgae biofuel commercialization.

## Project Structure

### 1. **Bibliometric Analysis** (`bibliometric-analysis/`)
Quantitative analysis of 214 peer-reviewed publications (2009-2025) using bibliometrix:
- Publication trends and citation patterns
- Key authors, institutions, and countries
- Research themes and keyword evolution
- Collaboration networks

### 2. **Machine Learning / Topic Modeling** (`machine-learning/`)
Natural Language Processing using BERTopic on 223 scientific papers:
- Semantic topic discovery and classification
- Research gap identification
- Thematic structure analysis
- Integration with policy and patent data

### 3. **Policy Analysis** (`machine-learning/policy-analysis/`)
Analysis of biofuel-related policy documents:
- Policy document collection and archival
- Thematic analysis using BERTopic
- Policy framework assessment

### 4. **Patent Analysis** (`machine-learning/patent-analysis/`)
Patent landscape analysis for algae biofuel technologies:
- Google BigQuery patent data extraction
- Technology trend identification
- Innovation pattern analysis

## Quick Start

### Bibliometric Analysis
```bash
cd bibliometric-analysis/reproducible-bibliometric-analysis
# Python approach
python complete_analysis.py
python generate_all_plots.py

# R approach
Rscript run_all.R
```

### Topic Modeling (BERTopic)
```bash
cd machine-learning
python run_bertopic_analysis.py
```

### Policy Analysis
```bash
cd machine-learning/policy-analysis
python bulk_policy_downloader.py
```

## Key Findings

The research addresses barriers across multiple dimensions:
- **Technical**: Production efficiency, cultivation challenges, harvesting costs
- **Economic**: Capital requirements, operational expenses, market competitiveness
- **Policy**: Regulatory frameworks, subsidies, sustainability standards
- **Innovation**: Patent activity, technological maturity, R&D investment

## Documentation

Each subdirectory contains detailed README files with:
- Methodology documentation
- Installation requirements
- Usage instructions
- Output descriptions

## Contact & Citation

**PhD Candidate**: [Your Name]  
**Institution**: [Your University]  
**Year**: 2025

For detailed methodology and results, see individual folder README files.
