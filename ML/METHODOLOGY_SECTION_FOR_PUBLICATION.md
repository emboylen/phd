# Methodology Section for Peer-Reviewed Publication
## BERTopic: Semantic Topic Modeling for Microalgae Biofuel Sustainability Research

---

## 3. Methods

### 3.1 Data Collection and Corpus Construction

The research corpus consisted of peer-reviewed scientific publications focused on microalgae biofuel sustainability, policy frameworks, and techno-economic analyses. Documents were retrieved from [*specify databases: e.g., Scopus, Web of Science, PubMed*] using systematic search queries targeting keywords related to microalgae cultivation, biofuel production, life cycle assessment (LCA), techno-economic analysis (TEA), and policy interventions. Only peer-reviewed journal articles and conference proceedings published between [*specify date range*] were included to ensure research currency and quality.

Text data were extracted from PDF documents using PyMuPDF (version 1.23.x), with full-text content compiled for each publication. Documents with insufficient extractable text (< 100 characters) or non-English content were excluded from analysis. The final corpus comprised **N** documents representing **M** peer-reviewed publications from **K** unique journals, with abstracts serving as the primary analytical unit to balance semantic richness with computational efficiency.

### 3.2 Text Preprocessing

In contrast to traditional bag-of-words approaches (e.g., Latent Dirichlet Allocation), which require extensive preprocessing to reduce vocabulary dimensionality, transformer-based topic modeling benefits from preserving natural language structure to maintain contextual information critical for accurate embeddings (Grootendorst, 2022). A lightweight preprocessing pipeline was therefore implemented:

**Noise Removal**: Regular expressions were employed to identify and remove URLs (http/https patterns), Digital Object Identifiers (DOIs), HTML tags, and email addresses that do not contribute semantic meaning but may introduce noise.

**Character Normalization**: Special characters were selectively removed while preserving domain-critical symbols including chemical notation (e.g., CO₂, NO₃⁻), abbreviations (pH, LCA, TEA), and hyphenated compound terms (e.g., "life-cycle," "techno-economic"). This domain-specific constraint ensures retention of essential terminology that would be lost under aggressive filtering.

**Critical Design Decision**: Unlike LDA preprocessing, the pipeline explicitly **excludes** lemmatization, stemming, lowercasing, and aggressive stop-word removal. These transformations damage the syntactic and semantic structure upon which transformer models depend for contextualized word representations (Devlin et al., 2019).

Documents with fewer than 50 characters after cleaning were excluded to ensure sufficient semantic content for meaningful analysis.

### 3.3 Semantic Topic Modeling with BERTopic

#### 3.3.1 Methodological Framework

BERTopic (Grootendorst, 2022) represents a paradigm shift from probabilistic generative models (LDA) to a transformer-based semantic clustering approach. The method leverages pre-trained language models to capture contextual word meanings, enabling topic discovery that aligns more closely with human interpretation of thematic coherence. The BERTopic pipeline integrates four sequential stages:

1. **Contextual Embedding Generation** using Sentence Transformers
2. **Dimensionality Reduction** via Uniform Manifold Approximation and Projection (UMAP)
3. **Density-Based Clustering** using Hierarchical DBSCAN (HDBSCAN)
4. **Topic Representation** through class-based Term Frequency-Inverse Document Frequency (c-TF-IDF)

This architecture enables discovery of semantically coherent topics while accommodating varying topic sizes and document-topic distributions without requiring prior specification of topic count.

#### 3.3.2 Stage 1: Document Embedding

Documents were transformed into dense vector representations using Sentence-BERT (SBERT; Reimers & Gurevych, 2019) with the **all-MiniLM-L6-v2** model. This model generates 384-dimensional embeddings optimized for semantic similarity tasks, achieving strong performance with computational efficiency suitable for moderately large corpora (< 100,000 documents).

SBERT extends BERT's contextualized representations to sentence-level semantics using siamese and triplet network architectures trained on Natural Language Inference (NLI) and Semantic Textual Similarity (STS) benchmarks. The resulting embeddings capture nuanced semantic relationships that transcend simple lexical overlap, enabling clustering of documents by conceptual similarity rather than keyword co-occurrence.

Formally, each document \(d_i\) is mapped to embedding \(\mathbf{e}_i \in \mathbb{R}^{384}\):

\[
\mathbf{e}_i = \text{SBERT}(d_i)
\]

#### 3.3.3 Stage 2: Dimensionality Reduction with UMAP

High-dimensional embeddings were reduced to 5 dimensions using UMAP (McInnes et al., 2018), a manifold learning technique that preserves both local and global structure in the data through optimization of fuzzy topological representations.

**UMAP Configuration**:
- **n_neighbors = 15**: Balances local neighborhood structure (small values) with global relationships (large values). This setting captures mesoscopic structure appropriate for scientific literature domains.
- **n_components = 5**: Reduced dimensionality sufficient for HDBSCAN while preserving topological structure.
- **metric = 'cosine'**: Angular distance metric appropriate for normalized text embeddings, focusing on directional similarity rather than magnitude.
- **random_state = 42**: Fixed random seed ensuring reproducibility.

UMAP constructs a weighted k-nearest neighbor graph in the high-dimensional space, converts it to a fuzzy simplicial complex, and optimizes a low-dimensional representation to minimize cross-entropy between fuzzy topological structures:

\[
\min_{\mathbf{y}} \sum_{i,j} \left[ w_{ij} \log \frac{w_{ij}}{v_{ij}} + (1 - w_{ij}) \log \frac{1 - w_{ij}}{1 - v_{ij}} \right]
\]

where \(w_{ij}\) and \(v_{ij}\) are fuzzy membership strengths in high- and low-dimensional spaces, respectively.

#### 3.3.4 Stage 3: Hierarchical Density-Based Clustering

HDBSCAN (McInnes et al., 2017) was employed to identify topic clusters in the UMAP-reduced space. Unlike centroid-based algorithms (e.g., k-means) that require pre-specification of cluster count and assume spherical cluster geometry, HDBSCAN discovers clusters of varying density and shape, automatically determining the number of topics while classifying noise points (outliers).

**HDBSCAN Configuration**:
- **min_cluster_size = 15**: Minimum documents required to form a topic cluster. This threshold balances granularity (small values yield more specific topics) with robustness (large values reduce spurious clusters).
- **metric = 'euclidean'**: Standard distance metric for UMAP output space.
- **prediction_data = True**: Enables soft clustering and outlier reassignment.
- **min_samples = 1**: Conservative setting allowing flexible cluster boundaries.

HDBSCAN constructs a hierarchy of clusters based on mutual reachability distance, then extracts stable clusters by analyzing cluster persistence across density thresholds. Documents that do not belong to any stable cluster are labeled as outliers (topic = -1).

**Outlier Reduction**: Following initial clustering, outliers were reassigned to the nearest topic using an embedding-based strategy. For each outlier document \(d_i\) with embedding \(\mathbf{e}_i\), the nearest topic was determined by cosine similarity to topic centroids:

\[
\text{topic}(d_i) = \arg\max_{t} \frac{\mathbf{e}_i \cdot \mathbf{c}_t}{\|\mathbf{e}_i\| \|\mathbf{c}_t\|}
\]

where \(\mathbf{c}_t\) is the centroid of topic \(t\) computed as the mean embedding of member documents.

#### 3.3.5 Stage 4: Topic Representation with c-TF-IDF

While clustering operates on semantic embeddings, topic interpretation requires human-readable keyword representations. BERTopic employs **class-based TF-IDF** (c-TF-IDF), which treats all documents in a topic cluster as a single pseudo-document and calculates term importance relative to other topics:

\[
\text{c-TF-IDF}(w, t) = \text{tf}(w, t) \times \log \frac{N}{\sum_{t'} \text{tf}(w, t')}
\]

where:
- \(\text{tf}(w, t)\) = frequency of word \(w\) in topic \(t\) (sum across all documents in topic)
- \(N\) = total number of topics
- Denominator sums word frequency across all topics

This approach identifies terms that are frequent within a topic but rare across other topics, producing interpretable keyword sets that distinguish topics from one another.

**Vectorization Configuration**:
- **stop_words = "english"**: Removed common function words
- **min_df = 2**: Terms must appear in at least 2 documents
- **ngram_range = (1, 2)**: Extracted unigrams and bigrams to capture both single concepts and multi-word expressions (e.g., "greenhouse gas," "life cycle")

### 3.4 Model Validation and Evaluation

#### 3.4.1 Topic Coherence

While BERTopic does not require pre-specification of topic count, the quality of discovered topics was assessed using coherence metrics. Coherence measures quantify the degree of semantic similarity between high-scoring words within topics, with higher values indicating more interpretable topics (Röder et al., 2015).

[*Optional: Include specific coherence scores if computed*]

#### 3.4.2 Topic Diversity

Topic diversity was calculated as the percentage of unique words across all topics, ensuring that topics capture distinct themes rather than redundant concepts:

\[
\text{Diversity} = \frac{|\bigcup_{t=1}^{T} W_t|}{T \times |W_t|}
\]

where \(W_t\) is the set of top-N words for topic \(t\), and \(T\) is the total number of topics.

#### 3.4.3 Qualitative Validation

Topic labels and keyword sets were reviewed by domain experts to assess semantic validity and alignment with established research themes in microalgae biofuel sustainability. Topics were manually annotated with descriptive labels based on the top 10 keywords and representative documents.

### 3.5 Visualization and Interpretation

#### 3.5.1 Intertopic Distance Mapping

Topic relationships were visualized using dimensionally-reduced embeddings projected onto a 2D plane via t-SNE or additional UMAP transformation. The resulting intertopic distance map displays topics as circles, with proximity indicating semantic similarity and circle size representing topic prevalence (document count).

#### 3.5.2 Hierarchical Topic Clustering

A dendrogram was constructed to illustrate hierarchical relationships between topics, enabling identification of higher-order thematic categories and sub-topic structure. This visualization supports multi-level interpretation aligned with the hierarchical nature of scientific knowledge domains.

#### 3.5.3 Topic-Document Assignment

Each document was assigned a primary topic (highest probability) along with a confidence score. This deterministic assignment facilitates downstream analyses including temporal trend analysis, policy mapping, and cross-topic comparisons.

### 3.6 Comparison to Traditional Approaches

The BERTopic framework offers several methodological advantages over traditional LDA for scientific literature analysis:

1. **Semantic Understanding**: Transformer embeddings capture contextual word meanings, enabling discovery of topics defined by semantic coherence rather than lexical co-occurrence.

2. **Preservation of Domain Terminology**: Minimal preprocessing retains critical acronyms (LCA, TEA, pH) and technical terminology that would be lost under aggressive normalization.

3. **Automatic Topic Discovery**: HDBSCAN eliminates the need for arbitrary selection of topic count, with cluster stability metrics providing principled model selection.

4. **Handling of Short Text**: Sentence-level embeddings perform effectively on abstracts and short documents, whereas LDA often requires longer texts for stable topic inference.

5. **Dynamic Topic Modeling**: The framework naturally extends to temporal analysis and topic evolution tracking without requiring specialized algorithms.

### 3.7 Software and Computational Environment

All analyses were conducted in Python 3.12 with the following libraries:

- **BERTopic 0.16.x**: Topic modeling framework (Grootendorst, 2022)
- **Sentence-Transformers 2.2.x**: Pre-trained embedding models (Reimers & Gurevych, 2019)
- **UMAP-learn 0.5.x**: Dimensionality reduction (McInnes et al., 2018)
- **HDBSCAN 0.8.x**: Clustering algorithm (McInnes et al., 2017)
- **Scikit-learn 1.3.x**: Text vectorization and preprocessing
- **Pandas 2.1.x**: Data manipulation
- **Plotly 5.x**: Interactive visualizations

Computations were performed on [*specify hardware: e.g., Intel Xeon CPU, 32GB RAM, NVIDIA GPU if used*]. Embedding generation for the full corpus required approximately [*X*] hours, with subsequent UMAP and clustering completing in [*Y*] minutes. All code, configuration parameters, and model artifacts are available in the supplementary materials to ensure full reproducibility.

---

## References

Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). BERT: Pre-training of deep bidirectional transformers for language understanding. In *Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies* (pp. 4171-4186).

Grootendorst, M. (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure. *arXiv preprint arXiv:2203.05794*.

McInnes, L., Healy, J., & Astels, S. (2017). hdbscan: Hierarchical density based clustering. *Journal of Open Source Software*, 2(11), 205.

McInnes, L., Healy, J., & Melville, J. (2018). UMAP: Uniform manifold approximation and projection for dimension reduction. *arXiv preprint arXiv:1802.03426*.

Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence embeddings using Siamese BERT-networks. In *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing* (pp. 3982-3992).

Röder, M., Both, A., & Hinneburg, A. (2015). Exploring the space of topic coherence measures. In *Proceedings of the eighth ACM international conference on Web search and data mining* (pp. 399-408).

---

## Supplementary Materials Checklist

For peer-reviewed publication, include:

✓ **Complete corpus details**: Document count, date range, journals, search queries  
✓ **Full preprocessing code**: With domain-specific regex patterns  
✓ **Model hyperparameters**: All configuration values in structured format  
✓ **Topic-keyword tables**: Top 15 keywords per topic with c-TF-IDF scores  
✓ **Topic-document assignments**: CSV with document IDs, topics, and probabilities  
✓ **Intertopic distance visualization**: High-resolution interactive HTML  
✓ **Coherence scores**: Validation metrics for model quality  
✓ **Reproducibility package**: GitHub repository with code, environment specifications, and sample data  

---

## Notes for Authors

**Word Count Management**: This methodology section is comprehensive (~2,500 words). For journals with strict limits:
- Condense Section 3.3.3 (HDBSCAN) and 3.3.4 (c-TF-IDF) with references to original papers
- Move detailed configuration parameters to supplementary tables
- Simplify mathematical notation if not required by journal style

**Domain Customization**: Replace bracketed placeholders with:
- Your specific corpus size and date range (Section 3.1)
- Actual computational time estimates (Section 3.7)
- Hardware specifications (Section 3.7)
- Coherence scores if computed (Section 3.4.1)

**Comparative Analysis**: If contrasting with LDA results, add a subsection comparing:
- Topic coherence scores (BERTopic vs. LDA)
- Topic diversity metrics
- Qualitative assessment of keyword interpretability
- Computational efficiency (time and memory)

**Field-Specific Terminology**: Ensure citations include domain-relevant applications of topic modeling in sustainability science, environmental policy analysis, or bioenergy research to strengthen methodological justification.

