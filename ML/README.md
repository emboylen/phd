# Topic Modeling Pipeline for Scientific Literature Analysis

A comprehensive 6-stage framework for topic modeling with enhanced coherence optimization, designed for analyzing scientific literature (specifically microalgae/biofuel research).

## 📁 Directory Structure

```
ML/
├── refined-topic-model.py          # Main topic modeling pipeline (RUN THIS)
├── README.md                        # This file
├── run-analysis.ps1                 # Legacy PowerShell runner
├── run-refined-analysis.ps1         # Current PowerShell runner
│
├── included/                        # Your PDF files (223 documents)
│   └── README.md                    # Data directory documentation
│
├── model_checkpoints/               # Saved trained models (auto-created)
│   └── README.md                    # Model storage documentation
│
├── outputs/                         # All generated results
│   ├── README.md                    # Outputs overview
│   ├── logs/                        # Execution logs
│   ├── summaries/                   # Topic reviews & configs
│   └── visualizations/              # HTML graphs & plots
│
├── utilities/                       # Helper scripts
│   └── README.md                    # Utility scripts documentation
│
├── archive/                         # Old versions & development files
│   └── README.md                    # Archive documentation
│
└── venv312/                         # Python virtual environment
```

## 🚀 Quick Start

### 1. Prerequisites

```powershell
# Activate virtual environment
.\venv312\Scripts\Activate.ps1

# Verify packages (should already be installed)
python -m spacy download en_core_web_sm
```

### 2. Prepare Your Data

Place all PDF files in the `included/` directory (or update `PDF_FOLDER_PATH` in the script).

### 3. Run the Main Pipeline

```powershell
python refined-topic-model.py
```

**Expected Runtime:** 2-4 hours for 223 documents testing k=2 to k=50

**What it does:**
- Extracts text from all PDFs
- Preprocesses with lemmatization and POS filtering
- Detects meaningful bigrams/trigrams (enhanced detection)
- Trains multiple LDA models (k=2 to k=50 by steps of 2)
- Selects optimal model using coherence scores
- Generates interactive HTML visualizations

**Progress indicators:**
```
Extracting PDF text: 100%|██████████| 223/223 [00:30<00:00]
Preprocessing documents: 100%|██████████| 223/223 [03:30<00:00]
Training LDA models: 47%|████████  | 12/25 [15:23<17:42, 106.2s/model]
```

### 4. Generate Outputs for Review

```powershell
# Export model configuration and statistics
python utilities/export_model_config.py

# Generate comprehensive print summary
python utilities/export_print_summary.py
```

### 5. Review and Categorize

1. Open the print summary in `outputs/summaries/`
2. Print for manual annotation
3. For each topic:
   - Read the keywords
   - Assign a meaningful category name
   - Note quality, overlaps, or issues
4. Use insights to refine the model (see "Refinement" below)

## 📊 Output Files Explained

### Visualizations (`outputs/visualizations/`)

**`refined_topics_summary.html`**
- Interactive HTML table with all topics and keywords
- Document counts per topic
- Top 10 documents assigned to each topic
- Model statistics and methodology

**`refined_knowledge_graph.html`**
- Interactive network visualization
- Topics (red nodes), Keywords (green), Documents (blue)
- Drag nodes, zoom, explore relationships

**`coherence_plot.png`**
- Chart showing coherence scores vs. number of topics
- Peak indicates optimal k value

### Summaries (`outputs/summaries/`)

**`topic_model_print_summary_*.txt`**
- Comprehensive print-friendly topic summary
- Top 20 keywords per topic
- Representative documents
- Manual categorization forms
- Quality assessment checklists

**`model_configuration_summary_*.txt`**
- Complete model statistics
- All processing parameters
- Custom stop word lists
- Training configuration

### Logs (`outputs/logs/`)

**`topic_modeling_*.log`**
- Complete execution log with timestamps
- All processing steps and progress
- Coherence scores for each k
- Errors and warnings

### Models (`model_checkpoints/`)

**`lda_model_k{N}.pkl`** (and associated files)
- Saved models for each k value tested
- Can be loaded for further analysis without retraining
- Optimal model automatically identified

## 🔧 Configuration & Refinement

### Key Parameters (in `refined-topic-model.py`)

```python
# Line ~48: PDF folder location
PDF_FOLDER_PATH = r"D:\Github\phd\ML\included"

# Lines ~54-62: Vocabulary filtering & N-grams
MIN_DOC_COUNT = 5          # Word must appear in ≥5 documents
MAX_DOC_FRACTION = 0.85    # Word can't appear in >85% of documents
BIGRAM_MIN_COUNT = 3       # Bigram detection threshold (lowered for better detection)
BIGRAM_THRESHOLD = 50      # Bigram scoring threshold (lowered)
TRIGRAM_MIN_COUNT = 3      # Trigram detection threshold
TRIGRAM_THRESHOLD = 50     # Trigram scoring threshold

# Lines ~64-67: Topic range to test
TOPIC_RANGE_START = 2      # Start from k=2 topics
TOPIC_RANGE_END = 51       # Test up to k=50 topics
TOPIC_STEP = 2             # Test every 2nd value (2, 4, 6, 8...)

# Lines ~69-71: LDA training parameters
LDA_PASSES = 10            # Training iterations (↑ = better quality, slower)
LDA_ITERATIONS = 400       # Per-document iterations
LDA_CHUNKSIZE = 100        # Documents per batch
```

### Custom Stopwords (Lines ~137-180)

Add domain-specific terms that appear too frequently:

```python
corpus_specific = {
    'microalgae', 'microalga', 'algae', 'algal', 'alga',
    'species', 'strain', 'strains', 
    'model', 'system', 'systems',
    'sample', 'samples', 'sampling',
    # ADD YOUR TERMS based on manual review
}
```

### Performance Tuning

**To speed up (trade quality for time):**
```python
LDA_PASSES = 5              # Reduce from 10
LDA_ITERATIONS = 200        # Reduce from 400
TOPIC_RANGE_START = 5       # Start from k=5
TOPIC_RANGE_END = 26        # End at k=25
TOPIC_STEP = 5              # Test every 5th value (5, 10, 15, 20, 25)
```

**To improve quality (slower):**
```python
LDA_PASSES = 15             # Increase from 10
LDA_ITERATIONS = 600        # Increase from 400
TOPIC_STEP = 1              # Test every k value
```

## 🔄 Refinement Workflow

1. **Run initial model** → Review outputs in `outputs/`
2. **Generate summaries** → Use utility scripts
3. **Identify issues:**
   - Topics too broad → Increase k range
   - Topics too narrow → Decrease k range
   - Topics overlapping → Add stopwords
   - Poor separation → Adjust MIN_DOC_COUNT or n-gram thresholds
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
**Solution:** Already fixed - numpy float32 values are converted to Python float/int.

### UnicodeEncodeError when printing
**Solution:** Files are saved correctly - console display issue only (Windows encoding).

## 🔬 Methodology

This pipeline implements a 6-stage framework:

1. **Custom Stop-Word List** - Generic + Academic + Domain-specific (285+ terms)
2. **Semantic Normalization** - Lemmatization + POS filtering (NOUN, ADJ, VERB, ADV only)
3. **N-gram Detection** - Enhanced bigrams & trigrams (lower thresholds for better detection)
4. **Vocabulary Pruning** - Document frequency filtering (min_df=5, max_df=0.85)
5. **Coherence-Based Evaluation** - C_v metric across k=2-50
6. **Optimal Model Training** - Auto-selected k with alpha=auto, eta=auto

## 📚 Technical Details

**Python Version:** 3.12  
**Key Dependencies:** gensim, spacy, nltk, networkx, pyvis, tqdm  
**Corpus Size:** 223 scientific papers  
**LDA Implementation:** Gensim with multicore support (disabled on Windows)  
**Coherence Metric:** C_v (best for interpretability)

## 🆘 Support

- Check execution logs in `outputs/logs/` for detailed information
- Review README files in each subdirectory for specific documentation
- See `archive/` for historical fixes and documentation

## 📝 Recent Updates

**2025-11-16:**
- Extended topic range to k=50 for better optimization
- Enhanced n-gram detection (lowered thresholds)
- Fixed JSON serialization issue in knowledge graph
- Reorganized directory structure for clarity
- Added comprehensive utility scripts and documentation
- Fixed Windows multiprocessing compatibility

---

**Last Updated:** 2025-11-17  
**Status:** Production Ready  
**Current Optimal Model:** k=8 (from previous run)
