# Topic Modeling Pipeline for Scientific Literature Analysis

A comprehensive 6-stage framework for topic modeling with enhanced coherence optimization, designed for analyzing scientific literature (specifically microalgae/biofuel research).

## 📁 Directory Structure

```
ML/
├── refined-topic-model.py          # Main topic modeling pipeline (RUN THIS FIRST)
├── create_topic_review_doc.py      # Generate printable topic review (RUN AFTER MAIN)
├── regenerate_graph.py              # Regenerate knowledge graph if needed
├── included/                        # Your PDF files go here (223 PDFs)
├── model_checkpoints/               # Saved models (auto-created)
├── refined_topics_summary.html      # Interactive topic summary (OUTPUT)
├── refined_knowledge_graph.html     # Interactive network graph (OUTPUT)
├── coherence_plot.png               # Topic optimization chart (OUTPUT)
├── topics_for_manual_review_*.txt   # Printable review document (OUTPUT)
└── topic_modeling_*.log             # Execution log (OUTPUT)
```

## 🚀 Quick Start

### 1. Prerequisites

```powershell
# Install required packages (if not already installed)
pip install pymupdf spacy nltk gensim matplotlib networkx pyvis tqdm

# Download spaCy language model
python -m spacy download en_core_web_sm
```

### 2. Prepare Your Data

Place all PDF files in the `included/` directory (or update `PDF_FOLDER_PATH` in the script).

### 3. Run the Main Pipeline

```powershell
python refined-topic-model.py
```

**Expected Runtime:** 2-4 hours for 223 documents testing k=2 to k=20

**What it does:**
- Extracts text from all PDFs
- Preprocesses with lemmatization and POS filtering
- Detects meaningful bigrams/trigrams
- Trains 19 LDA models (k=2 to k=20)
- Selects optimal model using coherence scores
- Generates interactive HTML visualizations

**Progress indicators:**
```
Extracting PDF text: 100%|██████████| 223/223 [00:30<00:00]
Preprocessing documents: 100%|██████████| 223/223 [03:30<00:00]
Training LDA models: 47%|████████  | 9/19 [15:23<17:42, 106.2s/model]
```

### 4. Generate Manual Review Document

```powershell
python create_topic_review_doc.py
```

**What it does:**
- Loads the final optimized model
- Extracts top 20 keywords per topic
- Creates a printable text document for manual categorization
- Includes space for notes and recommendations

**Output:** `topics_for_manual_review_YYYYMMDD_HHMMSS.txt`

### 5. Review and Categorize

1. Open the review document in a text editor or Word
2. Print it for manual annotation
3. For each topic:
   - Read the keywords
   - Assign a meaningful category name
   - Note quality, overlaps, or issues
4. Use insights to refine the model (see "Refinement" below)

## 📊 Output Files Explained

### `refined_topics_summary.html`
**Interactive HTML table** showing:
- All topics with their keywords
- Document counts per topic
- Top 10 documents assigned to each topic
- Model statistics and methodology

**How to use:** Open in any web browser, review topic assignments

### `refined_knowledge_graph.html`
**Interactive network visualization** showing:
- Topics (red nodes)
- Keywords (green nodes)
- Documents (blue nodes)
- Relationships and weights

**How to use:** Open in browser, drag nodes, zoom, explore connections

### `coherence_plot.png`
**Chart showing** coherence scores for different numbers of topics (k=2 to k=20)
- Peak indicates optimal number of topics
- Used to validate the automated selection

### `model_checkpoints/`
**Saved models** for each k value tested:
- `lda_model_k2.pkl`, `lda_model_k3.pkl`, ..., `lda_model_k20.pkl`
- `final_best_model_k{N}.pkl` - The optimal model selected

**Use case:** Load any model for further analysis without retraining

### `topics_for_manual_review_*.txt`
**Human-readable document** with:
- All topics and their top 20 keywords
- Relevance scores for each keyword
- Space for manual categorization
- Notes section for observations

**Purpose:** Print and annotate for manual topic validation and refinement

### `topic_modeling_*.log`
**Complete execution log** with timestamps:
- All processing steps
- Model training progress
- Coherence scores
- Errors and warnings

**Use case:** Debugging and tracking what happened during execution

## 🔧 Configuration & Refinement

### Key Parameters (in `refined-topic-model.py`)

```python
# Line 48: PDF folder location
PDF_FOLDER_PATH = r"D:\Github\phd\ML\included"

# Lines 54-60: Vocabulary filtering
MIN_DOC_COUNT = 5          # Word must appear in ≥5 documents
MAX_DOC_FRACTION = 0.85    # Word can't appear in >85% of documents
BIGRAM_MIN_COUNT = 5       # Minimum count for phrase detection
BIGRAM_THRESHOLD = 100     # Threshold for phrase scoring

# Lines 59-61: Topic range to test
TOPIC_RANGE_START = 2      # Start from k=2 topics
TOPIC_RANGE_END = 21       # Test up to k=20 topics
TOPIC_STEP = 1             # Test every k value

# Lines 63-65: LDA training parameters
LDA_PASSES = 10            # Training iterations (↑ = better quality, slower)
LDA_ITERATIONS = 400       # Per-document iterations
LDA_CHUNKSIZE = 100        # Documents per batch
```

### Custom Stopwords (Lines 137-142)

Add domain-specific terms that appear too frequently:

```python
corpus_specific = {
    'microalgae', 'microalga', 'algae', 'algal', 'alga',
    'species', 'strain', 'strains', 
    'model', 'system', 'systems',
    'sample', 'samples', 'sampling',
    # ADD YOUR TERMS HERE based on manual review
}
```

### Performance Tuning

**To speed up (trade quality for time):**
```python
LDA_PASSES = 5              # Reduce from 10
LDA_ITERATIONS = 200        # Reduce from 400
TOPIC_RANGE_START = 5       # Start from k=5
TOPIC_RANGE_END = 16        # End at k=15
TOPIC_STEP = 2              # Test every 2nd value (5, 7, 9...)
```

**To improve quality (slower):**
```python
LDA_PASSES = 15             # Increase from 10
LDA_ITERATIONS = 600        # Increase from 400
```

## 🔄 Refinement Workflow

1. **Run initial model** → Review outputs
2. **Generate review document** → Manual categorization
3. **Identify issues:**
   - Topics too broad → Increase k
   - Topics too narrow → Decrease k
   - Topics overlapping → Add stopwords
   - Poor separation → Adjust MIN_DOC_COUNT
4. **Update parameters** in `refined-topic-model.py`
5. **Re-run** → Compare results
6. **Iterate** until satisfied

## 🐛 Troubleshooting

### Script hangs at "Training LDA models"
**Solution:** It's not hung, just slow. Check progress bars. Each model takes 3-10 minutes.

### "RuntimeError: multiprocessing"
**Solution:** Already fixed with `if __name__ == '__main__':` guard and `processes=1` in CoherenceModel.

### "No PDF files found"
**Solution:** Check `PDF_FOLDER_PATH` points to correct directory with PDF files.

### "Vocabulary is empty"
**Solution:** Reduce `MIN_DOC_COUNT` or increase `MAX_DOC_FRACTION`.

### Knowledge graph fails to generate
**Solution:** Run `regenerate_graph.py` or check that numpy float32 values are converted to float.

## 📝 Files You DON'T Need to Run

- `refined-topic-model.py.backup` - Backup file, ignore
- `rebuild.py`, `fix_*.py`, `create_*.py` - Development scripts, ignore
- `__pycache__/` - Python cache, ignore

## 🔬 Methodology

This pipeline implements a 6-stage framework:

1. **Custom Stop-Word List** - Generic + Academic + Domain-specific (285 terms)
2. **Semantic Normalization** - Lemmatization + POS filtering (NOUN, ADJ, VERB, ADV only)
3. **N-gram Detection** - Bigrams & trigrams (threshold=100)
4. **Vocabulary Pruning** - Document frequency filtering (min_df=5, max_df=0.85)
5. **Coherence-Based Evaluation** - C_v metric across k=2-20
6. **Optimal Model Training** - Auto-selected k with alpha=auto, eta=auto

## 📚 Citation & References

Based on methodological best practices for topic modeling:
- Gensim LDA implementation
- C_v coherence metric for topic evaluation
- Phrase detection via pointwise mutual information
- Document frequency filtering for noise reduction

## 🆘 Support

Check the execution log (`topic_modeling_*.log`) for detailed information about what happened during execution.

For issues with the methodology or parameters, review:
- `CRITICAL_FIXES_SUMMARY.md` - Technical details on fixes applied
- `QUICK_REFERENCE.md` - Quick troubleshooting guide

---

**Last Updated:** 2025-11-16  
**Python Version:** 3.12  
**Corpus Size:** 223 scientific papers

