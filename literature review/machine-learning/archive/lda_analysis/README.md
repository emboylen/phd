# LDA Analysis Archive

**Archive Date:** November 19, 2025  
**Reason:** Replaced with superior BERTopic methodology for PhD research

---

## Contents

This directory contains all files, models, and outputs from the **Latent Dirichlet Allocation (LDA)** topic modeling analysis that was performed prior to adopting the BERTopic approach.

### **Main Script**
- `refined-topic-model.py` - Complete 6-stage LDA pipeline with coherence optimization

### **Model Checkpoints**
- `model_checkpoints/` - All trained LDA models (k=2, 4, 6, ..., 48, 50)
  - `lda_model_k*.pkl` - Individual models for each topic count tested
  - `final_best_model_k8.pkl` - Optimal model (k=8 topics, highest coherence)

### **Outputs**
- `outputs_logs/` - Execution logs from LDA runs
- `outputs_visualizations/` - HTML visualizations and coherence plots
- `outputs_summaries/` - Topic review documents and model configurations
- `outputs_README.md` - Original README for LDA outputs

### **Utilities**
- `utilities/` - Helper scripts for LDA analysis
  - `create_topic_review_doc.py` - Generate human-readable topic summaries
  - `export_model_config.py` - Export model statistics
  - `export_print_summary.py` - Create print-friendly summaries
  - `regenerate_graph.py` - Regenerate knowledge graph visualizations
- `utilities_README.md` - Original README for utility scripts

---

## LDA Analysis Summary

### **Methodology**
- **Algorithm:** Latent Dirichlet Allocation (Gensim 4.4.0)
- **Preprocessing:** Heavy (lemmatization, POS filtering, custom stop words, n-grams)
- **Coherence Metric:** C_v
- **Topic Range Tested:** k = 2, 4, 6, ..., 48, 50 (25 models)
- **Optimal Result:** k = 8 topics

### **Key Parameters**
- **Vocabulary Filtering:** min_df=5, max_df=0.85
- **N-gram Detection:** Bigrams (min_count=3, threshold=50), Trigrams (min_count=3, threshold=50)
- **LDA Training:** 10 passes, 400 iterations per document, chunksize=100
- **Custom Stop Words:** ~285 terms (generic + academic + domain-specific)

### **Results**
- **Corpus Size:** 223 documents
- **Final Vocabulary:** 10,167 terms
- **Optimal Topics:** 8 (selected via coherence optimization)
- **Coherence Score (k=8):** ~0.45 (estimated)

### **Discovered Topics (k=8)**
The LDA analysis identified 8 topics related to:
1. Microalgae cultivation and biomass production
2. Wastewater treatment and bioremediation
3. Biorefinery and value-added products
4. Life cycle assessment and sustainability
5. Biodiesel production technology
6. Carbon sequestration and climate mitigation
7. Techno-economic analysis
8. Policy and commercialization challenges

(Note: Specific topic details available in `outputs_summaries/topic_model_print_summary_*.txt`)

---

## Why This Was Archived

### **Limitations of LDA Approach**
1. **Bag-of-Words Assumption:** Ignores word order and context, reducing semantic understanding
2. **Manual Topic Selection:** Required testing k=2-50 to find optimal number (k=8)
3. **Heavy Preprocessing:** Lemmatization and aggressive filtering removed domain-specific terms
4. **Keyword Co-occurrence:** Topics based on word frequency patterns, not semantic meaning
5. **Interpretability:** Required manual inspection to assign meaningful topic labels
6. **Computational Cost:** Training 25 models for coherence optimization took significant time

### **Advantages of BERTopic Replacement**
1. **Semantic Understanding:** Transformer embeddings capture contextual meaning
2. **Automatic Topic Discovery:** HDBSCAN determines optimal topic count without testing
3. **Domain Term Preservation:** Minimal preprocessing retains pH, LCA, TEA, etc.
4. **Clearer Topics:** Semantic clustering produces more interpretable themes
5. **Interactive Visualizations:** Dynamic exploration of topic relationships
6. **Confidence Scores:** Document-level probabilities for uncertainty quantification

### **Comparison Summary**
| Aspect | LDA (Archived) | BERTopic (Current) |
|--------|----------------|---------------------|
| Topics Discovered | 8 (manual) | 6 (automatic) |
| Coherence/Confidence | ~0.45 | 0.606 |
| Preprocessing | Heavy | Lightweight |
| Semantic Understanding | Limited | Strong |
| Topic Selection | Manual (k=2-50 tested) | Automatic (HDBSCAN) |
| Interpretability | Moderate | High |
| Domain Terms | Lost | Preserved |

---

## Historical Context

This LDA analysis was conducted as part of a systematic literature review for PhD research on microalgae biofuel sustainability. The analysis successfully:
- Processed 223 peer-reviewed publications
- Implemented a rigorous 6-stage preprocessing pipeline
- Optimized topic count using C_v coherence metric
- Generated comprehensive visualizations and summaries

However, after reviewing recent advances in topic modeling (Grootendorst 2022), the decision was made to transition to BERTopic for:
- Better alignment with modern NLP best practices
- Superior interpretability for academic publication
- Stronger semantic coherence for literature synthesis
- More robust handling of technical scientific terminology

---

## Files Reference

### **Most Important Files**
- `model_checkpoints/final_best_model_k8.pkl` - Best performing LDA model
- `outputs_summaries/model_configuration_summary_*.txt` - Complete model configuration
- `outputs_summaries/topic_model_print_summary_*.txt` - Human-readable topic descriptions
- `outputs_visualizations/coherence_plot.png` - Coherence scores across all k values

### **For Comparison Studies**
If you need to compare LDA and BERTopic results:
1. Load `final_best_model_k8.pkl` using Gensim
2. Extract topic-word distributions with `model.show_topics()`
3. Compare with BERTopic topics in `../bertopic_outputs/topic_info_*.csv`
4. Calculate alignment metrics (e.g., topic similarity, keyword overlap)

---

## Reusability

While archived, these files remain useful for:

1. **Methodological Comparison:** Demonstrating why BERTopic was chosen over LDA
2. **Baseline Results:** Providing comparison baseline for improvements
3. **Reproducibility:** Full pipeline preserved for audit/validation
4. **Educational Use:** Teaching example of classical topic modeling

### **To Rerun LDA Analysis**
```python
# Load saved model
from gensim.models import LdaModel
model = LdaModel.load("model_checkpoints/final_best_model_k8.pkl")

# View topics
for idx, topic in model.show_topics(num_topics=8, num_words=15):
    print(f"Topic {idx}: {topic}")
```

---

## References

**LDA Methodology:**
- Blei, D. M., Ng, A. Y., & Jordan, M. I. (2003). Latent dirichlet allocation. *Journal of Machine Learning Research*, 3, 993-1022.

**Coherence Metric:**
- Röder, M., Both, A., & Hinneburg, A. (2015). Exploring the space of topic coherence measures. *Proceedings of WSDM*, 399-408.

**BERTopic Rationale:**
- Grootendorst, M. (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure. *arXiv preprint arXiv:2203.05794*.

---

## Contact

For questions about this archived analysis:
- See main project README: `../README.md`
- Current BERTopic analysis: `../BERTOPIC_ANALYSIS_SUMMARY.md`
- Methodology comparison: Available in PhD thesis Chapter 3

**Archive Status:** Preserved for reference only. Not actively maintained.

