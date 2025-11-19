# Microalgae Biofuel Sustainability - Topic Modeling Analysis

**PhD Research Project**  
**Last Updated:** November 19, 2025  
**Current Methodology:** BERTopic (Transformer-Based Semantic Topic Modeling)

---

## Quick Start

```bash
# 1. Install dependencies
pip install bertopic sentence-transformers umap-learn hdbscan pymupdf pandas

# 2. Run BERTopic analysis
python run_bertopic_analysis.py

# 3. View results
# Open bertopic_outputs/intertopic_distance_*.html in your browser
# Review bertopic_outputs/BERTOPIC_SUMMARY_*.txt
```

---

## Project Overview

This repository contains a comprehensive topic modeling analysis of **223 peer-reviewed scientific publications** on microalgae biofuel sustainability. The analysis employs **BERTopic**, a state-of-the-art semantic topic modeling framework that leverages transformer-based embeddings to discover coherent thematic structures in scientific literature.

### **Research Questions**
1. What are the major research themes in microalgae biofuel sustainability literature?
2. How is research effort distributed across different aspects (production, economics, sustainability, policy)?
3. What topics are underrepresented and represent potential research gaps?
4. How do topics cluster hierarchically to reveal higher-order research domains?

### **Key Findings**
- **6 Major Topics** discovered automatically (no pre-specification required)
- **30% of literature** focused on fundamental production challenges (Topic 0)
- **19% on wastewater integration** and circular economy approaches (Topic 1)
- **29% combined focus** on biorefinery economics and sustainability assessment (Topics 2+3)
- **12% specialized** in biodiesel production technology (Topic 4)
- **9% forward-looking** research on next-generation innovations (Topic 5)

---

## Directory Structure

```
D:\Github\phd\ML\
│
├── included/                          # PDF corpus (223 papers)
│   └── *.pdf                          # Peer-reviewed publications
│
├── bertopic_outputs/                  # BERTopic analysis results
│   ├── topic_info_*.csv               # Topic keywords & statistics
│   ├── document_topics_*.csv          # Document assignments
│   ├── intertopic_distance_*.html     # Interactive topic map
│   ├── hierarchy_*.html               # Topic hierarchy dendrogram
│   ├── barchart_*.html                # Keyword visualizations
│   ├── BERTOPIC_SUMMARY_*.txt         # Human-readable summary
│   ├── raw_extractions_*.csv          # Extracted PDF text
│   └── bertopic_model_*/              # Trained model (reloadable)
│
├── archive/                           # Historical files
│   ├── lda_analysis/                  # Previous LDA approach (archived)
│   │   ├── refined-topic-model.py     # LDA pipeline script
│   │   ├── model_checkpoints/         # LDA models (k=2...50)
│   │   ├── outputs_*/                 # LDA visualizations & summaries
│   │   └── README.md                  # LDA archive documentation
│   └── README.md                      # Archive overview
│
├── run_bertopic_analysis.py           # Main BERTopic pipeline
├── bertopic_pipeline.py               # Reusable BERTopic module
├── create_bertopic_summary.py         # Summary generation script
│
├── BERTOPIC_ANALYSIS_SUMMARY.md       # Comprehensive analysis report
├── METHODOLOGY_SECTION_FOR_PUBLICATION.md  # Peer-reviewed methodology
├── README.md                          # This file
└── included/README.md                 # Corpus documentation
```

---

## Discovered Topics

### **Topic 0: General Microalgae Biofuel Production & Challenges** (67 docs, 30.0%)
- **Keywords:** production, microalgae, biofuel, cultivation, biomass, challenges, energy
- **Focus:** Fundamental research on scalability, cultivation optimization, carbon sequestration
- **Key Papers:** Reviews on challenges, opportunities, and carbon mitigation potential

### **Topic 1: Wastewater Treatment & Circular Bioeconomy** (43 docs, 19.3%)
- **Keywords:** wastewater, treatment, biorefinery, circular, bioremediation, phycoremediation
- **Focus:** Integration with wastewater systems, nutrient recovery, dual-purpose biorefineries
- **Key Papers:** Wastewater-coupled cultivation, circular economy models, cost reduction

### **Topic 2: Integrated Biorefinery & Value-Added Products** (34 docs, 15.2%)
- **Keywords:** biorefinery, products, biomass, valorization, co-products, value-added
- **Focus:** Multi-product strategies, cascading utilization, economic viability through diversification
- **Key Papers:** Biorefinery design, co-product optimization, holistic valorization

### **Topic 3: Sustainability Assessment & Policy Frameworks** (31 docs, 13.9%)
- **Keywords:** sustainability, assessment, life cycle, economic, analysis, environmental, policy
- **Focus:** LCA, TEA, policy barriers, socioeconomic indicators, regulatory frameworks
- **Key Papers:** Life cycle assessments, techno-economic analyses, policy reviews

### **Topic 4: Biodiesel Production Technology** (27 docs, 12.1%)
- **Keywords:** biodiesel, lipid, production, conversion, transesterification, fuel
- **Focus:** Lipid enhancement, extraction methods, fuel quality, aviation applications
- **Key Papers:** Biodiesel conversion technologies, lipid accumulation, aviation fuel

### **Topic 5: Third-Generation Biofuels & Future Innovations** (21 docs, 9.4%)
- **Keywords:** third generation, renewable, future, prospects, emerging, innovations
- **Focus:** Next-generation technologies, emerging trends, long-term viability
- **Key Papers:** Future prospects, post-pandemic developments, technology roadmaps

---

## Methodology

### **BERTopic Pipeline (6 Stages)**

1. **Text Extraction** - PyMuPDF extracts full text from 223 PDFs
2. **Lightweight Preprocessing** - Minimal cleaning to preserve context (URLs/DOIs removed, domain terms preserved)
3. **Embedding Generation** - Sentence-BERT (all-MiniLM-L6-v2) creates 384-dim contextual embeddings
4. **Dimensionality Reduction** - UMAP reduces to 5 dimensions (n_neighbors=15, cosine metric)
5. **Density-Based Clustering** - HDBSCAN discovers topics automatically (min_cluster_size=15)
6. **Topic Representation** - Class-based TF-IDF (c-TF-IDF) generates interpretable keywords

### **Key Advantages Over Traditional LDA**
✅ **Semantic Understanding** - Captures meaning beyond keyword co-occurrence  
✅ **Automatic Topic Discovery** - No need to test k=2...50  
✅ **Domain Term Preservation** - Retains pH, LCA, TEA, chemical symbols  
✅ **Superior Interpretability** - Clearer thematic boundaries  
✅ **Interactive Visualizations** - Dynamic exploration of relationships  
✅ **Confidence Quantification** - Document-level probability distributions  

### **Performance**
- **Documents Processed:** 223 (19.7M characters)
- **Average Confidence:** 60.6%
- **Outlier Rate:** 0% (all documents successfully categorized)
- **Runtime:** < 1 minute (standard laptop, no GPU)

---

## Usage

### **Running the Analysis**

```python
# Basic usage
python run_bertopic_analysis.py

# The script will:
# 1. Extract text from all PDFs in included/
# 2. Apply lightweight preprocessing
# 3. Generate embeddings using Sentence-BERT
# 4. Perform UMAP + HDBSCAN clustering
# 5. Create visualizations and export results
```

### **Loading Saved Model**

```python
from bertopic import BERTopic

# Load trained model
model = BERTopic.load("bertopic_outputs/bertopic_model_20251119_130232")

# Get topic info
topic_info = model.get_topic_info()

# Get topic keywords
topic_0_keywords = model.get_topic(0)
print(topic_0_keywords)

# Predict topic for new document
new_doc = ["Microalgae cultivation for sustainable biofuel production..."]
topics, probs = model.transform(new_doc)
```

### **Generating Summary**

```python
# Create human-readable summary
python create_bertopic_summary.py

# Output: bertopic_outputs/BERTOPIC_SUMMARY_*.txt
```

---

## Visualizations

### **Interactive HTML Files** (Open in browser)

1. **Intertopic Distance Map** (`intertopic_distance_*.html`)
   - 2D visualization of topic relationships
   - Circle size = topic prevalence
   - Distance = semantic similarity
   - Hover for keywords and details

2. **Hierarchical Clustering** (`hierarchy_*.html`)
   - Dendrogram showing topic relationships
   - Identify higher-order thematic categories
   - Explore multi-level structure

3. **Topic Bar Charts** (`barchart_*.html`)
   - Top keywords per topic with importance scores
   - C-TF-IDF values for each term
   - Visual comparison across topics

---

## Data Exports

### **CSV Files**

1. **topic_info_*.csv** - Complete topic information
   - Topic ID, Count, Name, Representation
   - Top keywords with c-TF-IDF scores
   - Topic metadata

2. **document_topics_*.csv** - Document assignments
   - Filename, assigned topic, confidence score
   - Use for further analysis (citation networks, trends)
   - 223 rows (one per document)

3. **raw_extractions_*.csv** - Full extracted text
   - Original PDF text for validation
   - Page counts and metadata

---

## Applications

### **1. Literature Review Organization**
- Use topic assignments to structure thesis chapters
- Group related papers for thematic synthesis
- Identify seminal works per topic (high confidence scores)

### **2. Research Gap Identification**
- **Underrepresented:** Topic 5 (innovations, 9.4%) = opportunity
- **Oversaturated:** Topic 0 (general challenges, 30%) = limited novelty
- **Emerging:** Intersection of Topics 1+2 (wastewater biorefineries) = promising

### **3. Citation Strategy**
- High-confidence papers = essential citations
- Cross-topic papers = interdisciplinary context
- Topic-specific = domain expertise demonstration

### **4. Trend Analysis** (if temporal data added)
- Topic prevalence over time
- Shifting research priorities
- Emerging sub-topics

---

## Requirements

### **Python Dependencies**
```
bertopic>=0.16.0
sentence-transformers>=2.2.0
umap-learn>=0.5.0
hdbscan>=0.8.0
pymupdf>=1.23.0
pandas>=2.1.0
numpy>=1.24.0
scikit-learn>=1.3.0
plotly>=5.0.0
```

### **Installation**
```bash
pip install bertopic sentence-transformers umap-learn hdbscan pymupdf pandas plotly
```

### **System Requirements**
- **Python:** 3.10+
- **RAM:** 2+ GB
- **Storage:** 500+ MB for outputs
- **GPU:** Optional (faster embedding generation)

---

## Publication Materials

### **Methodology Section**
See `METHODOLOGY_SECTION_FOR_PUBLICATION.md` for:
- Complete mathematical formulation (SBERT, UMAP, HDBSCAN, c-TF-IDF)
- Academic citations (Grootendorst 2022, Reimers & Gurevych 2019, etc.)
- Justification for methodological choices
- Comparison with traditional approaches
- Reproducibility details

### **Comprehensive Report**
See `BERTOPIC_ANALYSIS_SUMMARY.md` for:
- Executive summary
- Detailed topic descriptions
- Representative papers per topic
- Research maturity insights
- Comparison with LDA
- Applications for PhD research
- Validation and evaluation

---

## Troubleshooting

### **Common Issues**

**1. Module not found errors**
```bash
pip install [missing_module]
```

**2. PDF extraction fails**
- Check PDF files are valid (not corrupted)
- Ensure sufficient disk space
- Verify file permissions

**3. Memory errors**
- Reduce batch size in embedding generation
- Process PDFs in smaller batches
- Increase system swap file

**4. Slow performance**
- Install GPU-accelerated PyTorch for embeddings
- Use fewer documents for testing
- Reduce UMAP n_neighbors

### **Configuration**

Edit `run_bertopic_analysis.py` to adjust:
- `PDF_FOLDER`: Source directory for PDFs
- `HDBSCAN_MIN_CLUSTER_SIZE`: Minimum documents per topic (default: 15)
- `UMAP_N_NEIGHBORS`: Balance local/global structure (default: 15)
- `CV_MIN_DF`: Minimum document frequency for terms (default: 2)

---

## Archive

### **Previous LDA Analysis**
The project originally used Latent Dirichlet Allocation (LDA) with coherence optimization (k=2-50 tested). This approach was replaced by BERTopic for superior semantic understanding and interpretability.

**Archived files:** `archive/lda_analysis/`
- LDA script, models, outputs, and utilities
- Comparison summary and rationale for transition
- See `archive/lda_analysis/README.md` for details

---

## References

**BERTopic Framework:**
- Grootendorst, M. (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure. *arXiv preprint arXiv:2203.05794*.

**Sentence-BERT Embeddings:**
- Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence embeddings using Siamese BERT-networks. *EMNLP*, 3982-3992.

**UMAP Dimensionality Reduction:**
- McInnes, L., Healy, J., & Melville, J. (2018). UMAP: Uniform manifold approximation and projection. *arXiv preprint arXiv:1802.03426*.

**HDBSCAN Clustering:**
- McInnes, L., Healy, J., & Astels, S. (2017). hdbscan: Hierarchical density based clustering. *Journal of Open Source Software*, 2(11), 205.

---

## Citation

If you use this analysis or methodology in your research, please cite:

```bibtex
@misc{microalgae_bertopic2025,
  author = {[Your Name]},
  title = {BERTopic Analysis of Microalgae Biofuel Sustainability Literature},
  year = {2025},
  publisher = {GitHub},
  url = {[Your Repository URL]}
}
```

---

## Contact & Support

**Author:** PhD Candidate  
**Institution:** [Your University]  
**Email:** [Your Email]  

**Issues:** Please report bugs or request features via GitHub issues  
**Questions:** See `BERTOPIC_ANALYSIS_SUMMARY.md` for detailed FAQ

---

## License

This project is part of PhD research. Data (published papers) remains under original copyright. Analysis code and methodology are available for academic use with proper citation.

---

**Last Analysis Run:** November 19, 2025  
**Next Steps:** Temporal analysis, subtopic discovery, integration with bibliometric data
