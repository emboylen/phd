# Utilities Directory

Helper scripts for post-processing, analysis, and regeneration of outputs. These scripts operate on saved models and don't require re-running the full pipeline.

## 📜 Available Scripts

### `export_model_config.py`
**Purpose:** Export comprehensive model configuration and statistics to a text file.

**What it does:**
- Loads the optimal model from checkpoints
- Extracts all model statistics (k, vocabulary size, coherence)
- Documents all processing parameters
- Lists complete custom stop word set (285+ words)
- Saves to timestamped text file

**When to use:**
- After running the main pipeline
- For documentation and reproducibility
- When sharing model configuration with collaborators
- Before making parameter changes (to track what was used)

**Usage:**
```powershell
python utilities/export_model_config.py
```

**Output:**
- `outputs/summaries/model_configuration_summary_YYYYMMDD_HHMMSS.txt`

**Requirements:**
- Trained model must exist in `model_checkpoints/`
- No additional inputs needed

---

### `export_print_summary.py`
**Purpose:** Generate comprehensive, print-friendly topic summary with detailed information for manual review.

**What it does:**
- Loads the k=8 model (optimal from previous run)
- Extracts top 20 keywords per topic with relevance scores
- Identifies representative documents per topic
- Creates formatted pages for each topic with:
  - Two-column keyword layout
  - Manual categorization forms
  - Quality assessment checkboxes
  - Space for refinement notes
- Adds overall analysis section
- Includes merge/split recommendations

**When to use:**
- After model training completes
- Before manual topic labeling and categorization
- When printing for team review sessions
- For quality assessment and refinement planning

**Usage:**
```powershell
python utilities/export_print_summary.py
```

**Output:**
- `outputs/summaries/topic_model_print_summary_YYYYMMDD_HHMMSS.txt`
- Estimated 10-15 pages for k=8 model
- Formatted for letter size (8.5x11) paper

**Configuration:**
- Currently hardcoded to load k=8 model (line 14)
- Modify `optimal_k = 8` to load different models

**Requirements:**
- Trained model must exist: `model_checkpoints/lda_model_k8.pkl`
- HTML summary file: `refined_topics_summary.html` (for document assignments)

---

### `create_topic_review_doc.py`
**Purpose:** Generate simplified topic review document with keywords only (legacy).

**What it does:**
- Loads the final best model from checkpoints
- Extracts top 20 keywords per topic
- Creates simple text document with:
  - Topic numbers
  - Keywords with relevance scores
  - Document counts
  - Space for manual labels

**When to use:**
- Quick keyword reference
- Simplified review format
- Email-friendly plain text

**Usage:**
```powershell
python utilities/create_topic_review_doc.py
```

**Output:**
- `outputs/summaries/topics_for_manual_review_YYYYMMDD_HHMMSS.txt`

**Note:** `export_print_summary.py` is more comprehensive and recommended for detailed review.

---

### `regenerate_graph.py`
**Purpose:** Regenerate knowledge graph visualization from saved model without re-training.

**What it does:**
- Loads existing model and dictionary
- Rebuilds network graph with topics, keywords, and documents
- Generates interactive HTML visualization
- Useful for testing graph fixes or styling changes

**When to use:**
- After fixing graph generation bugs
- To update graph styling
- To regenerate after manual model adjustments
- Testing without full pipeline re-run

**Usage:**
```powershell
python utilities/regenerate_graph.py
```

**Output:**
- `outputs/visualizations/pdf_knowledge_graph.html` (or similar)

**Requirements:**
- Trained model in `model_checkpoints/`
- Document data (BoW corpus)

**Note:** Currently may need path adjustments depending on model location.

---

### `create_enhanced_review_doc.py`
**Purpose:** Generate enhanced review document by parsing HTML summary (experimental).

**Status:** ⚠️ **Incomplete/Deprecated**

**Issues:**
- Requires BeautifulSoup (`bs4`) which may not be installed
- HTML parsing approach was more complex than needed
- Replaced by `export_print_summary.py`

**Recommendation:** Use `export_print_summary.py` instead.

---

## 🔧 How to Use These Scripts

### Basic Workflow

1. **Run main pipeline first:**
```powershell
python refined-topic-model.py
```

2. **Generate configuration summary:**
```powershell
python utilities/export_model_config.py
```

3. **Generate print summary for review:**
```powershell
python utilities/export_print_summary.py
```

4. **If graph needs regeneration:**
```powershell
python utilities/regenerate_graph.py
```

### Common Scenarios

**Scenario 1: Full Documentation**
```powershell
# After training completes
python utilities/export_model_config.py
python utilities/export_print_summary.py
```
Result: Complete model documentation + printable topic review

**Scenario 2: Quick Review**
```powershell
# Just need topic keywords
python utilities/create_topic_review_doc.py
```
Result: Simple keyword list for each topic

**Scenario 3: Graph Fix**
```powershell
# Graph generation failed but model is good
python utilities/regenerate_graph.py
```
Result: Regenerated graph without re-training model

---

## 📝 Modifying Scripts

### Change which model to load

**In `export_print_summary.py` (line 14):**
```python
# Load k=8 model
optimal_k = 8

# Change to k=12 model
optimal_k = 12
```

### Adjust number of keywords displayed

**In any export script:**
```python
# Change from top 20 to top 30 keywords
num_words = 30  # originally 20
top_words = model.show_topic(topic_id, topn=num_words)
```

### Change output location

**In any export script:**
```python
# Original
output_file = f"outputs/summaries/topic_model_print_summary_{timestamp}.txt"

# Custom location
output_file = f"my_custom_folder/topics_{timestamp}.txt"
```

---

## 🐛 Troubleshooting

### "No model file found"
**Problem:** Script can't find trained model.

**Solution:**
```powershell
# Check if models exist
ls model_checkpoints/*.pkl

# If empty, run main pipeline first
python refined-topic-model.py
```

### "Module not found" errors
**Problem:** Missing dependencies.

**Solution:**
```powershell
# Activate virtual environment
.\venv312\Scripts\Activate.ps1

# Install missing package (if needed)
pip install beautifulsoup4  # for create_enhanced_review_doc.py
```

### UnicodeEncodeError (Windows)
**Problem:** Console can't display certain characters.

**Solution:**
- Ignore console warnings - file is saved correctly
- Open output file in Notepad or VS Code
- Or redirect output: `python script.py > output.log 2>&1`

### Script loads wrong model
**Problem:** Script finds a model but it's not the one you want.

**Solution:**
- Check `model_checkpoints/` for available models
- Edit script to specify correct k value
- Or move unwanted models to `archive/`

---

## 🔄 Script Dependencies

```
refined-topic-model.py (main)
        ↓
   model_checkpoints/
        ↓
   ┌────┴────┬──────────────┬────────────────┐
   ↓         ↓              ↓                ↓
export_   export_     create_        regenerate_
model_    print_      topic_         graph.py
config    summary     review
.py       .py         _doc.py
```

**All utility scripts require:**
1. Completed run of `refined-topic-model.py`
2. Model files in `model_checkpoints/`
3. Virtual environment activated

---

## 📦 Adding New Utility Scripts

When creating new utility scripts:

1. **Follow naming convention:** `action_object.py` (e.g., `export_topics.py`)
2. **Import from main:** Use same imports as main pipeline
3. **Load from checkpoints:** Point to `model_checkpoints/` directory
4. **Output to outputs/:** Save to appropriate `outputs/` subdirectory
5. **Add to this README:** Document what it does and how to use it

**Template:**
```python
#!/usr/bin/env python3
"""
Utility: Brief description
Purpose: What problem does this solve?
Usage: python utilities/script_name.py
"""

from pathlib import Path
from gensim.models import LdaModel

# Load model
CHECKPOINT_DIR = "model_checkpoints"
model_file = Path(CHECKPOINT_DIR) / "lda_model_k8.pkl"
model = LdaModel.load(str(model_file))

# Do something useful
# ...

# Save output
output_file = f"outputs/summaries/output_{timestamp}.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(results)

print(f"[SUCCESS] Output saved: {output_file}")
```

---

**Last Updated:** 2025-11-17  
**Active Scripts:** 5 (2 recommended, 2 legacy, 1 experimental)  
**Purpose:** Post-processing and documentation without re-training

