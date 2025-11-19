# BERTopic Visualization Guide

**Generated:** November 19, 2025  
**Analysis:** 223 Documents, 6 Topics, BERTopic Semantic Clustering  
**Location:** `bertopic_outputs/visualizations/`

---

## Overview

This directory contains 6 publication-quality static visualizations (300 DPI PNG format) designed to complement the BERTopic analysis. All figures are ready for inclusion in your PhD thesis, publications, and presentations.

---

## Figure Descriptions

### **Figure 1: Topic Distribution Pie Chart**
**File:** `01_topic_distribution_pie.png`

**Description:** Pie chart showing the proportional distribution of 223 documents across 6 discovered topics.

**Key Features:**
- Color-coded topics with descriptive labels
- Percentage labels for each slice
- Exploded slices for emphasis (Topic 0 most prominent)

**Interpretation:**
- **Topic 0 (30.0%)**: General Production & Challenges - dominates the literature
- **Topic 5 (9.4%)**: Third-Generation Biofuels & Innovation - smallest category (research gap!)
- Shows clear imbalance in research focus

**Usage in Thesis:**
- Literature Review Chapter: Opening figure to show overall research landscape
- Introduction: Visual summary of field structure
- Discussion: Reference to justify novelty in underrepresented areas

---

### **Figure 2: Topic Sizes Horizontal Bar Chart**
**File:** `02_topic_sizes_horizontal.png`

**Description:** Horizontal bar chart comparing document counts across topics, ranked from smallest to largest.

**Key Features:**
- Topics sorted by size for easy comparison
- Exact document counts labeled on each bar
- Color-coded for visual distinction
- Grid lines for precise reading

**Interpretation:**
- Clear visual hierarchy: Topic 0 (67 docs) >> Topic 5 (21 docs)
- Nearly 3:1 ratio between largest and smallest topics
- Middle topics (1-4) relatively balanced (27-43 docs each)

**Usage in Thesis:**
- Results Section: Quantitative comparison of topic prevalence
- Literature Review: Support claims about research emphasis
- Gap Analysis: Highlight underrepresented areas

---

### **Figure 3: Confidence Distribution Box Plot**
**File:** `03_confidence_distribution_boxplot.png`

**Description:** Box plot showing document-topic assignment confidence distribution for each topic.

**Key Features:**
- Box = interquartile range (25th-75th percentile)
- Red horizontal line = median confidence per topic
- Whiskers = data range (excluding outliers)
- Red dashed line at 50% = threshold for "acceptable" confidence

**Interpretation:**
- **Topic 0**: Widest spread (0.1-1.0) - heterogeneous topic
- **Topic 5**: Narrower spread - more cohesive topic
- Most medians above 50% - good overall assignment quality
- Some topics have clearer boundaries than others

**Usage in Thesis:**
- Methodology Chapter: Demonstrate model validation and quality
- Results: Show topic coherence metrics
- Limitations: Acknowledge topics with lower confidence

---

### **Figure 4: Overall Confidence Histogram**
**File:** `04_overall_confidence_histogram.png`

**Description:** Histogram showing the distribution of all 223 document-topic assignment confidences.

**Key Features:**
- 30 bins across confidence range (0-1)
- Red dashed line = mean (0.606)
- Green dashed line = median (0.452)
- Bimodal distribution visible

**Interpretation:**
- **Bimodal pattern**: Two peaks suggest two document classes:
  - High confidence (~0.8-1.0): Documents with clear thematic fit
  - Moderate confidence (~0.3-0.5): Documents spanning multiple topics
- **47.1% high confidence (>0.8)**: Nearly half have very strong assignments
- Mean > Median: Right-skewed distribution (more high-confidence docs)

**Usage in Thesis:**
- Methodology: Validation of classification quality
- Results: Overall model performance metric
- Discussion: Acknowledge uncertainty in cross-topic documents

---

### **Figure 5: Topic Characteristics Summary (4-Panel)**
**File:** `05_topic_characteristics_summary.png`

**Description:** Comprehensive 4-panel figure showing multiple topic metrics simultaneously.

**Panel A - Document Counts:**
- Bar chart of documents per topic
- Shows Topic 0 dominance at a glance

**Panel B - Average Confidence:**
- Mean confidence score per topic
- Red line at 50% threshold
- Topics 4 and 5 have highest average confidence

**Panel C - High-Confidence Documents:**
- Count of docs with >80% confidence per topic
- Shows which topics have clearest boundaries
- Topic 0 has most high-confidence docs (expected - largest)

**Panel D - Research Focus Percentages:**
- Percentage distribution (sums to 100%)
- Quick visual reference for relative emphasis

**Interpretation:**
- **Multi-dimensional quality assessment**: Size, confidence, and focus together
- **Topic 0**: Large but lower average confidence (heterogeneous)
- **Topic 5**: Small but high average confidence (cohesive)
- **Balanced middle topics** (1-4): Similar sizes and confidences

**Usage in Thesis:**
- Results Chapter: Comprehensive overview figure
- Presentations: Single slide showing all key metrics
- Appendix: Detailed model characteristics

---

### **Figure 6: Research Maturity Analysis**
**File:** `06_research_maturity_analysis.png`

**Description:** Bar chart grouping topics into 4 research maturity categories with interpretation.

**Maturity Categories:**
1. **Fundamental Challenges** (67 docs, 30%) - Topic 0
   - Basic production, cultivation, scalability issues
   
2. **Application Development** (70 docs, 31%) - Topics 1+4
   - Wastewater treatment, biodiesel production
   
3. **Economic Viability** (65 docs, 29%) - Topics 2+3
   - Biorefineries, LCA, TEA, policy
   
4. **Future Innovations** (21 docs, 9%) - Topic 5
   - Next-generation technologies

**Key Insight Box:**
- 30% still addressing fundamentals → field maturing
- 29% on economic viability → major concern
- 9% on innovations → underrepresented (opportunity!)

**Interpretation:**
- **Nearly balanced** between applications (31%) and economics (29%)
- **30% fundamentals** suggests field not yet mature for commercialization
- **9% innovations** = clear research gap for novel contributions
- Natural progression: fundamentals → applications → economics → innovations

**Usage in Thesis:**
- **Literature Review**: Justify positioning within research landscape
- **Research Justification**: Use 9% gap to motivate innovation focus
- **Contribution Claims**: Reference maturity distribution to show novelty
- **Future Work**: Point to innovation deficit as field priority

---

## Statistical Summary

### **Overall Metrics**
- **Total Documents:** 223
- **Topics Discovered:** 6
- **Mean Confidence:** 0.606 (60.6%)
- **Median Confidence:** 0.452 (45.2%)
- **Std Dev:** 0.379
- **High Confidence (>0.8):** 105 docs (47.1%)

### **Topic Distribution**
| Topic | Documents | Percentage | Theme |
|-------|-----------|------------|-------|
| 0 | 67 | 30.0% | General Production & Challenges |
| 1 | 43 | 19.3% | Wastewater Treatment & Circular Economy |
| 2 | 34 | 15.2% | Integrated Biorefinery & Value-Added Products |
| 3 | 31 | 13.9% | Sustainability Assessment & Policy |
| 4 | 27 | 12.1% | Biodiesel Production Technology |
| 5 | 21 | 9.4% | Third-Generation Biofuels & Innovation |

---

## Usage Guidelines

### **For PhD Thesis**

**Chapter 1 (Introduction):**
- Use Figure 1 (pie chart) to introduce research landscape
- Use Figure 6 (maturity) to justify research focus

**Chapter 2 (Literature Review):**
- Use Figure 2 (bar chart) to structure review sections
- Use Figure 6 (maturity) to organize by development stage
- Reference specific percentages to support claims

**Chapter 3 (Methodology):**
- Use Figure 3 (box plot) to show classification quality
- Use Figure 4 (histogram) to demonstrate model validation
- Cite 47.1% high-confidence rate

**Chapter 4 (Results):**
- Use Figure 5 (4-panel) as comprehensive results overview
- Reference topic sizes and confidences in text
- Use specific metrics from each panel

**Chapter 5 (Discussion):**
- Use Figure 6 (maturity) to contextualize contribution
- Reference 9.4% innovation gap as motivation
- Discuss implications of 30% fundamental focus

### **For Publications**

**Journal Articles:**
- All figures are 300 DPI (meets most journal requirements)
- PNG format easily convertible to TIFF if needed
- Color figures (check journal policy on color charges)
- Consider converting to grayscale for print journals

**Conference Presentations:**
- Figure 5 (4-panel) ideal for single-slide overview
- Figure 1 (pie) and Figure 6 (maturity) great for talks
- High resolution ensures clarity on projectors

**Posters:**
- Use Figure 1 or 2 as main visual element
- Figure 6 with insight box is self-explanatory
- Color coding helps with visual hierarchy

---

## Technical Details

**Format:** PNG (Portable Network Graphics)  
**Resolution:** 300 DPI (publication quality)  
**Color Space:** RGB  
**Size:** ~500-800 KB per figure  
**Dimensions:** Varies by figure (8-14 inches wide)  
**Generated with:** Matplotlib 3.8.x, Seaborn, Python 3.12  

---

## Reproducibility

To regenerate these visualizations:

```bash
python create_visualizations.py
```

The script will:
1. Load topic and document data from CSV files
2. Generate all 6 figures with consistent styling
3. Save to `bertopic_outputs/visualizations/`
4. Print summary statistics

**Dependencies:**
- pandas
- matplotlib
- seaborn
- numpy

---

## Companion Files

These static visualizations complement:

1. **Interactive HTML Visualizations**
   - `intertopic_distance_*.html` - Explore topic relationships dynamically
   - `hierarchy_*.html` - Interactive hierarchical clustering
   - `barchart_*.html` - Dynamic keyword bars

2. **Data Files**
   - `topic_info_*.csv` - Complete topic metadata
   - `document_topics_*.csv` - All assignments with confidence
   - `BERTOPIC_SUMMARY_*.txt` - Human-readable summary

3. **Documentation**
   - `BERTOPIC_ANALYSIS_SUMMARY.md` - Comprehensive analysis report
   - `METHODOLOGY_SECTION_FOR_PUBLICATION.md` - Peer-reviewed methodology
   - Main `README.md` - Project overview

---

## Citation

If using these visualizations in publications:

```bibtex
@misc{microalgae_bertopic_viz2025,
  author = {[Your Name]},
  title = {BERTopic Analysis Visualizations: Microalgae Biofuel Sustainability Literature},
  year = {2025},
  note = {Generated using BERTopic 0.16.x and Matplotlib 3.8.x}
}
```

---

**Questions?** See main project README or BERTOPIC_ANALYSIS_SUMMARY.md for details.

**Last Updated:** November 19, 2025

