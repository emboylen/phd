# Methodology Section for Peer-Reviewed Publication

## Topic Modeling of Scientific Literature: A Six-Stage Refinement Framework

### 3. Methods

#### 3.1 Corpus Construction and Text Extraction

The document corpus consisted of peer-reviewed scientific publications in the microalgae and biofuel research domain. All documents were in Portable Document Format (PDF) and were processed using PyMuPDF (version 1.23.x) to extract plain text content. The text extraction process traversed each page sequentially and compiled the full-text content for subsequent processing. Documents with insufficient content (< 100 characters) were excluded from the analysis to ensure data quality. The final corpus comprised documents that met minimum content requirements for meaningful topic extraction.

#### 3.2 Text Preprocessing Pipeline

A comprehensive six-stage text preprocessing and topic modeling pipeline was implemented to enhance the quality and interpretability of extracted topics. This methodological framework integrates established natural language processing techniques with domain-specific refinements.

##### 3.2.1 Stage 1: Hierarchical Stop-Word Filtering

A custom stop-word list was constructed using a three-tier hierarchical approach to remove non-informative terms while preserving domain-relevant vocabulary:

**Layer 1: Generic English Stop Words** (n ≈ 198) – Common function words (articles, prepositions, pronouns, conjunctions) were sourced from the Natural Language Toolkit (NLTK) English stopwords corpus (Bird et al., 2009).

**Layer 2: Academic and Publishing Artifacts** (n = 74) – Terms associated with document structure and scholarly communication that do not contribute to semantic content were systematically removed. This layer included:
- Citation artifacts (e.g., "et al.", "ibid", "op. cit.")
- Figure and table references ("fig", "table", "equation")
- Web and publishing metadata ("doi", "http", "pdf", "copyright", "publisher")
- Generic academic terminology ("introduction", "methods", "results", "discussion", "study", "research", "paper")

**Layer 3: Corpus-Specific Stop Words** (n = 14) – Domain-general terms that appeared ubiquitously across documents with insufficient discriminative power for topic differentiation were identified and excluded. For the microalgae corpus, this included terms such as "microalgae," "algae," "species," "strain," "model," "system," and "sample."

The complete custom stop-word list comprised approximately 285 unique terms.

##### 3.2.2 Stage 2: Semantic Normalization via Lemmatization and Part-of-Speech Filtering

Text normalization was performed using spaCy (version 3.7.x) with the `en_core_web_sm` language model (Honnibal & Montani, 2017). The following processing steps were applied:

1. **URL and Email Removal**: Regular expressions were employed to identify and remove web addresses (http/https URLs), DOI strings, and email addresses.

2. **Numeric Content Removal**: Standalone numbers and year references were removed using pattern matching to focus analysis on conceptual vocabulary.

3. **Lemmatization**: All tokens were reduced to their base lexical form using spaCy's rule-based lemmatizer, which normalizes morphological variants (e.g., "produced," "producing," "produces" → "produce").

4. **Part-of-Speech (POS) Filtering**: Only tokens tagged as nouns (NOUN), adjectives (ADJ), verbs (VERB), or adverbs (ADV) were retained, as these word classes carry the majority of semantic content in scientific text (Justeson & Katz, 1995).

5. **Length and Alphabetic Constraints**: Tokens were required to be (a) composed entirely of alphabetic characters and (b) contain at least three characters to eliminate abbreviations and artifacts.

This multi-criteria filtering approach ensured that only semantically meaningful, normalized vocabulary was retained for subsequent analysis.

##### 3.2.3 Stage 3: Multi-Word Expression Detection via N-gram Collocation

To preserve meaningful multi-word units and improve topic interpretability, bigram and trigram detection was performed using Gensim's Phrases module (Řehůřek & Sojka, 2010), which implements Pointwise Mutual Information (PMI) scoring:

\[
PMI(w_i, w_j) = \log \frac{P(w_i, w_j)}{P(w_i) \times P(w_j)}
\]

**Bigram Detection Parameters**:
- Minimum count: 3 (collocations must appear at least 3 times)
- PMI threshold: 50
- Example detected bigrams: "lipid_production," "carbon_dioxide," "waste_water"

**Trigram Detection Parameters**:
- Minimum count: 3
- PMI threshold: 50
- Example detected trigrams: "life_cycle_assessment," "greenhouse_gas_emission"

The bigram model was trained first on the preprocessed corpus, followed by trigram model training on the bigram-transformed corpus. This hierarchical approach enables the detection of both two-word and three-word conceptual units. Detected phrases were treated as single tokens (connected with underscores) in subsequent modeling stages.

##### 3.2.4 Stage 4: Strategic Vocabulary Pruning via Document Frequency Filtering

To construct a refined vocabulary that balances specificity and generality, document frequency thresholds were applied using Gensim's Dictionary filtering functionality:

- **Minimum Document Frequency (min_df)**: Terms appearing in fewer than 5 documents were excluded to eliminate rare, potentially noisy terms and ensure statistical reliability.

- **Maximum Document Frequency (max_df)**: Terms appearing in more than 85% of documents were removed as these overly-common terms lack discriminative power for topic differentiation.

This filtering strategy follows established practices in information retrieval and topic modeling (Blei et al., 2003; Manning et al., 2008), removing both extremely rare terms (which may represent OCR errors or highly specialized jargon) and extremely common terms (which carry limited information for topic discrimination).

#### 3.3 Topic Model Training and Optimization

##### 3.3.1 Stage 5: Coherence-Based Model Selection

Rather than selecting the number of topics (k) arbitrarily, an empirical optimization approach was employed using the C_v coherence metric (Röder et al., 2015), which has been shown to correlate most strongly with human topic interpretability judgments among available automated metrics.

**Model Selection Protocol**:
- Topic range tested: k = 2, 4, 6, ..., 48, 50 (25 models total)
- Step size: 2 (selected to balance computational efficiency with granularity)
- Each model was trained to convergence and evaluated for coherence

The C_v coherence score for each model was calculated as:

\[
C_v(t, V^{(t)}) = \frac{2}{|V^{(t)}|(|V^{(t)}| - 1)} \sum_{m=2}^{|V^{(t)}|} \sum_{l=1}^{m-1} NPMI(v_l^{(t)}, v_m^{(t)})
\]

where t is a topic, V^(t) is the set of top words for that topic, and NPMI is normalized pointwise mutual information. The model with the highest mean C_v score across all topics was selected as optimal.

##### 3.3.2 Stage 6: Final Model Training – Latent Dirichlet Allocation

Latent Dirichlet Allocation (LDA; Blei et al., 2003) was implemented using Gensim's LdaModel with the following specifications:

**Training Parameters**:
- **Number of topics**: Empirically determined via coherence optimization
- **Inference algorithm**: Variational Bayes
- **Training passes**: 10 complete iterations through the corpus
- **Per-document iterations**: 400
- **Batch size**: 100 documents per training chunk
- **Random seed**: 100 (for reproducibility)

**Hyperparameter Learning**:
- **Alpha (document-topic density)**: Automatically learned from data using asymmetric priors
- **Eta (topic-word density)**: Automatically learned from data using asymmetric priors

The asymmetric prior learning approach allows the model to capture realistic document-topic distributions where some topics are more prevalent than others (Wallach et al., 2009).

**Generative Model**: LDA models each document as a mixture of topics, where each topic is a probability distribution over vocabulary terms. Formally:

For each document d:
1. Draw topic distribution θ_d ~ Dirichlet(α)
2. For each word position n in document d:
   - Draw topic z_{d,n} ~ Categorical(θ_d)
   - Draw word w_{d,n} ~ Categorical(β_{z_{d,n}})

where α is the document-topic prior and β represents the topic-word distributions.

**Model Persistence**: To enable reproducibility and facilitate sensitivity analyses, model checkpoints were saved at each tested k value using Gensim's native serialization format. The optimal model (highest coherence) was retained for final analysis and visualization.

#### 3.4 Validation and Evaluation

**Coherence Metric**: The C_v coherence measure was employed as the primary evaluation metric (Röder et al., 2015). Unlike perplexity-based measures, C_v correlates more strongly with human assessments of topic quality and interpretability.

**Document-Topic Assignment**: For each document, the posterior probability distribution over topics was computed, and the dominant topic (highest probability) was identified for classification purposes.

**Topic Characterization**: Each topic was represented by its 15 highest-probability terms, ordered by the term's contribution to the topic distribution (β values).

#### 3.5 Visualization and Knowledge Representation

Two complementary visualization approaches were employed to facilitate interpretation:

1. **Coherence Optimization Plot**: A line graph displaying C_v coherence scores across all tested k values, with the optimal k highlighted. This visualization demonstrates the empirical basis for model selection.

2. **Interactive Knowledge Graph**: A network visualization was constructed using NetworkX (Hagberg et al., 2008) and Pyvis, representing topics, documents, and keywords as nodes with weighted edges indicating:
   - Document-to-topic edges (weighted by topic probability)
   - Topic-to-keyword edges (weighted by term probability within topic)

Node sizes were scaled according to prominence (document count for topics, term probability for keywords), and physics-based layout algorithms were employed for optimal spatial arrangement.

#### 3.6 Software and Implementation

All analyses were conducted in Python 3.12. Key libraries included:
- **spaCy 3.7.x**: Linguistic annotation and lemmatization
- **NLTK 3.8.x**: Stop-word resources
- **Gensim 4.4.x**: Topic modeling and coherence evaluation
- **PyMuPDF (fitz) 1.23.x**: PDF text extraction
- **NetworkX 3.2.x**: Graph construction
- **Pyvis 0.3.x**: Interactive network visualization
- **Matplotlib 3.8.x**: Static visualization

All code and configuration parameters are available in the supplementary materials to ensure reproducibility.

---

### References

Blei, D. M., Ng, A. Y., & Jordan, M. I. (2003). Latent dirichlet allocation. *Journal of Machine Learning Research*, 3, 993-1022.

Bird, S., Klein, E., & Loper, E. (2009). *Natural language processing with Python: Analyzing text with the natural language toolkit*. O'Reilly Media, Inc.

Hagberg, A. A., Schult, D. A., & Swart, P. J. (2008). Exploring network structure, dynamics, and function using NetworkX. In *Proceedings of the 7th Python in Science Conference* (pp. 11-15).

Honnibal, M., & Montani, I. (2017). spaCy 2: Natural language understanding with Bloom embeddings, convolutional neural networks and incremental parsing. *To appear*, 7(1), 411-420.

Justeson, J. S., & Katz, S. M. (1995). Technical terminology: some linguistic properties and an algorithm for identification in text. *Natural Language Engineering*, 1(1), 9-27.

Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to information retrieval*. Cambridge University Press.

Řehůřek, R., & Sojka, P. (2010). Software framework for topic modelling with large corpora. In *Proceedings of the LREC 2010 workshop on new challenges for NLP frameworks* (pp. 45-50).

Röder, M., Both, A., & Hinneburg, A. (2015). Exploring the space of topic coherence measures. In *Proceedings of the eighth ACM international conference on Web search and data mining* (pp. 399-408).

Wallach, H. M., Mimno, D. M., & McCallum, A. (2009). Rethinking LDA: Why priors matter. In *Advances in neural information processing systems* (Vol. 22).

---

### Notes for Authors

**Parameter Reporting**: This methodology section provides comprehensive detail on all preprocessing steps, hyperparameters, and model configuration. When preparing your manuscript:

1. **Abbreviate if needed**: Some journals may require condensed methods. The hierarchical stop-word section (3.2.1) can be shortened to reference "a three-tier custom stop-word list comprising 285 terms" with details in supplementary materials.

2. **Corpus Details**: Section 3.1 should be expanded with specific corpus statistics (number of documents, publication years, journals, total word count) for your dataset.

3. **Results Integration**: The optimal k value and final coherence score should be reported in Section 3.3.1 with reference to the corresponding figure.

4. **Supplementary Materials**: Consider providing:
   - Complete stop-word list
   - Example detected n-grams
   - Full coherence scores table for all k values
   - Source code and configuration files
   - Representative topic-word distributions

5. **Ethical Considerations**: If applicable, add a statement regarding open access to publications or data sharing agreements.

This methodology is compliant with reporting standards for computational linguistics and text mining research, ensuring transparency and reproducibility of results.

