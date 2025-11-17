# Outputs Directory

This directory contains all generated results from the topic modeling pipeline. All outputs are timestamped to track different runs and enable comparison.

## 📁 Subdirectories

### `logs/`
Execution logs with detailed processing information for each run.

### `summaries/`
Human-readable topic summaries, model configurations, and review documents.

### `visualizations/`
Interactive HTML visualizations and plots for exploring topics and relationships.

## 🔍 What's in Each Subdirectory?

### Logs (`logs/`)

**Files:** `topic_modeling_YYYYMMDD_HHMMSS.log`

**Contents:**
- Timestamped execution log for each run
- All processing stages with progress
- Model training details and coherence scores
- Errors, warnings, and debug information
- Final model selection reasoning

**Use cases:**
- Debugging issues
- Tracking what parameters were used
- Comparing coherence scores across runs
- Understanding why a particular k was selected

**Example log entry:**
```
2025-11-16 07:19:45,123 - INFO - Training LDA model with k=8 topics...
2025-11-16 07:21:32,456 - INFO - Coherence score for k=8: 0.4523
2025-11-16 07:21:32,789 - INFO - New best model found! k=8 with coherence 0.4523
```

---

### Summaries (`summaries/`)

**Files:**
- `topic_model_print_summary_YYYYMMDD_HHMMSS.txt` - Comprehensive topic review for printing
- `model_configuration_summary_YYYYMMDD_HHMMSS.txt` - Model statistics and parameters
- `topics_for_manual_review_YYYYMMDD_HHMMSS.txt` - Simple topic keywords list
- `Refinement-topic-model-results.docx` - Word document with analysis

**1. Print Summary (`topic_model_print_summary_*.txt`)**

**Contents:**
- Table of contents with all topics
- Full page per topic:
  - Top 20 keywords with relevance scores
  - Representative documents from corpus
  - Manual categorization form (write-in spaces)
  - Quality assessment checkboxes
  - Refinement suggestion areas
- Overall analysis section
- Merge/split recommendations
- Missing topics section
- Additional stopwords suggestions
- Parameter adjustment recommendations

**Use cases:**
- Print for manual review and annotation
- Team collaboration on topic labeling
- Quality assessment before publication
- Planning next refinement iteration

**Example section:**
```
================================================================================
TOPIC 1 - Manual Label: _________________________________
================================================================================

Top 20 Keywords (Two-Column Layout):
   1. photosynthesis   (0.045)      11. electron        (0.018)
   2. light            (0.042)      12. chlorophyll     (0.017)
   ...

Representative Documents:
   • "Analysis of photosynthetic efficiency in..." (45% match)
   • "Light-dependent reactions in microalgae..." (42% match)
   ...

QUALITY ASSESSMENT:
[ ] Coherent and interpretable
[ ] Mixed/needs refinement
[ ] Low quality/should be merged or removed

SUGGESTED LABEL: _________________________________________________

NOTES:
_____________________________________________________________________
```

**2. Configuration Summary (`model_configuration_summary_*.txt`)**

**Contents:**
- Model metadata (optimal k, vocabulary size, coherence score)
- Complete list of all processing parameters
- Full custom stop word list (285+ words)
- Training configuration details
- System information

**Use cases:**
- Documentation for reproducibility
- Reference when tweaking parameters
- Understanding what stopwords are being filtered
- Tracking configuration across runs

**Example section:**
```
MODEL STATISTICS:
   Optimal Topics (k): 8
   Vocabulary Size: 11,415 terms
   Coherence Score: 0.4523
   Total Documents: 223

VOCABULARY FILTERING:
   Minimum Document Count: 5
   Maximum Document Fraction: 0.85
   Bigram Min Count: 3
   Bigram Threshold: 50
   ...

CUSTOM STOP WORDS (285 total):
   Generic (174): about, above, across, after, ...
   Academic (52): abstract, according, acknowledgment, ...
   Corpus-Specific (59): microalgae, microalga, algae, ...
```

**3. Manual Review (`topics_for_manual_review_*.txt`)**

**Contents:**
- Simple list of all topics
- Top 20 keywords per topic with scores
- Document counts
- Space for manual labels

**Use cases:**
- Quick reference during analysis
- Simplified format for quick labeling
- Easy to share via email or chat

---

### Visualizations (`visualizations/`)

**Files:**
- `refined_topics_summary.html` - Interactive topic table
- `refined_knowledge_graph.html` - Network visualization
- `pdf_knowledge_graph.html` - Alternative graph view
- `topics_summary.html` - Earlier version of summary
- `coherence_plot.png` - Coherence vs. k chart

**1. Topic Summary (`refined_topics_summary.html`)**

**Contents:**
- Interactive HTML table (sortable, filterable)
- All topics with top keywords
- Document counts per topic
- Top 10 documents per topic with titles
- Model methodology and statistics
- Professional styling for presentations

**How to use:**
- Open in any web browser
- Click column headers to sort
- Use browser search (Ctrl+F) to find specific terms
- Right-click images to save
- Share with collaborators

**2. Knowledge Graph (`refined_knowledge_graph.html`)**

**Contents:**
- Interactive network visualization using pyvis
- Node types:
  - **Red nodes** = Topics (sized by document count)
  - **Green nodes** = Keywords (sized by relevance)
  - **Blue nodes** = Documents (sized by topic probability)
- Edges show relationships and strengths
- Zoom, drag, and explore

**How to use:**
- Open in web browser (Chrome/Firefox recommended)
- Drag nodes to reposition
- Scroll to zoom in/out
- Click nodes to see labels
- Hover to see connection weights
- Use physics simulation controls (if available)

**Physics controls:**
- Can pause/resume node movement
- Adjust spring length and repulsion
- Stabilize graph layout

**3. Coherence Plot (`coherence_plot.png`)**

**Contents:**
- Line chart showing coherence scores (y-axis) vs. number of topics (x-axis)
- Peak indicates optimal k value
- Visual validation of automated selection

**How to use:**
- Open in image viewer
- Look for peak/highest point (optimal k)
- Check if selection makes sense
- Compare with coherence scores in logs
- Include in papers/presentations

**Interpretation:**
- **Sharp peak** = Clear optimal k
- **Plateau** = Multiple good k values (choose based on interpretability)
- **No clear peak** = May need to adjust parameters or extend range

---

## 📊 Typical Output Set (After One Run)

After running `refined-topic-model.py`, you'll get:

```
outputs/
├── logs/
│   └── topic_modeling_20251116_071945.log
├── summaries/
│   └── (initially empty - run utility scripts to generate)
└── visualizations/
    ├── refined_topics_summary.html
    ├── refined_knowledge_graph.html
    └── coherence_plot.png
```

After running utility scripts:

```
outputs/
├── logs/
│   └── topic_modeling_20251116_071945.log
├── summaries/
│   ├── model_configuration_summary_20251116_171218.txt
│   └── topic_model_print_summary_20251116_171620.txt
└── visualizations/
    ├── refined_topics_summary.html
    ├── refined_knowledge_graph.html
    └── coherence_plot.png
```

## 🔄 Comparing Multiple Runs

When refining the model, you'll accumulate multiple outputs:

```
outputs/
├── logs/
│   ├── topic_modeling_20251115_201606.log  (first run, k=2-20)
│   ├── topic_modeling_20251116_071945.log  (second run, k=2-50)
│   └── topic_modeling_20251117_143022.log  (third run, adjusted stopwords)
├── summaries/
│   ├── topic_model_print_summary_20251116_171620.txt  (k=8 model)
│   └── model_configuration_summary_20251116_171218.txt
└── visualizations/
    └── (updated each run, only latest kept unless renamed)
```

**Tip:** Rename important files before re-running to preserve comparisons:
```powershell
# Preserve current results before re-running
Rename-Item "outputs\visualizations\refined_topics_summary.html" "refined_topics_summary_k8.html"
```

## 🗑️ Cleanup

Old log files and summaries can be deleted after you've documented key findings. The models themselves are stored in `model_checkpoints/` and can be reloaded anytime.

**Safe to delete:**
- Old log files (after noting important details)
- Old summaries (after incorporating feedback)
- Intermediate visualizations (can be regenerated)

**Keep:**
- Latest log file (for current run documentation)
- Print summaries with manual annotations
- Configuration summaries for reproducibility

---

**Last Updated:** 2025-11-17  
**Total Output Types:** 3 categories (logs, summaries, visualizations)  
**Average Size per Run:** ~5-15 MB (mostly HTML graphs)

