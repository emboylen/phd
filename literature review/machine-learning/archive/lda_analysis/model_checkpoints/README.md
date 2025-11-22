# Model Checkpoints Directory

This directory stores all trained LDA models from the topic modeling pipeline. Each model is saved during training to enable analysis without re-training and to track coherence across different k values.

## 📁 Contents

After running `refined-topic-model.py`, this directory will contain:

```
model_checkpoints/
├── lda_model_k2.pkl           # Model with 2 topics
├── lda_model_k2.pkl.expElogbeta.npy
├── lda_model_k2.pkl.id2word
├── lda_model_k2.pkl.state
│
├── lda_model_k4.pkl           # Model with 4 topics
├── lda_model_k4.pkl.expElogbeta.npy
├── lda_model_k4.pkl.id2word
├── lda_model_k4.pkl.state
│
├── ...                        # Models for k=6, 8, 10, 12, ...
│
└── lda_model_k50.pkl          # Model with 50 topics
    lda_model_k50.pkl.expElogbeta.npy
    lda_model_k50.pkl.id2word
    lda_model_k50.pkl.state
```

## 📊 File Types

Each model `k{N}` has 4 associated files:

### 1. `lda_model_k{N}.pkl` (Main Model File)
- **Size:** ~5-20 MB depending on k and vocabulary
- **Contents:** Core LDA model with all parameters
- **Usage:** Load with `LdaModel.load()`

### 2. `lda_model_k{N}.pkl.expElogbeta.npy` (Topic-Word Matrix)
- **Size:** Largest file (~10-50 MB)
- **Contents:** Exponential of expected log beta (topic-word distributions)
- **Format:** NumPy binary array
- **Usage:** Automatically loaded with main model

### 3. `lda_model_k{N}.pkl.id2word` (Dictionary)
- **Size:** ~1-5 MB
- **Contents:** Vocabulary mapping (word IDs ↔ words)
- **Format:** Gensim Dictionary object
- **Usage:** Required for interpreting topics

### 4. `lda_model_k{N}.pkl.state` (Training State)
- **Size:** ~10-30 MB
- **Contents:** Model training state (sufficient statistics)
- **Format:** Gensim LdaState object
- **Usage:** Allows resuming training or updating model

## 🔍 Model Selection

The main pipeline (`refined-topic-model.py`) trains models for all k values in the range (default: k=2, 4, 6, ..., 50) and selects the optimal one based on **coherence score (C_v metric)**.

### Example Selection Process:
```
k=2  → Coherence: 0.3421
k=4  → Coherence: 0.4012
k=6  → Coherence: 0.4332
k=8  → Coherence: 0.4523  ← OPTIMAL (highest coherence)
k=10 → Coherence: 0.4487
k=12 → Coherence: 0.4398
...
k=50 → Coherence: 0.3201
```

The model with k=8 would be selected and used for final outputs, but **all models are preserved** for comparison and analysis.

## 💾 Loading Models

### Load a specific model:

```python
from gensim.models import LdaModel

# Load k=8 model
model = LdaModel.load("model_checkpoints/lda_model_k8.pkl")

# Get model info
print(f"Topics: {model.num_topics}")
print(f"Vocabulary: {len(model.id2word)}")

# Show topics
for idx, topic in model.print_topics(-1):
    print(f"Topic {idx}: {topic}")
```

### Load the optimal model (from logs):

```python
import re
from pathlib import Path

# Read log to find optimal k
log_file = "outputs/logs/topic_modeling_20251116_071945.log"
with open(log_file, 'r') as f:
    log_content = f.read()

# Extract optimal k
match = re.search(r'Optimal k=(\d+)', log_content)
optimal_k = int(match.group(1))

# Load that model
model = LdaModel.load(f"model_checkpoints/lda_model_k{optimal_k}.pkl")
```

### Load all models for comparison:

```python
from pathlib import Path
from gensim.models import LdaModel

checkpoint_dir = Path("model_checkpoints")
models = {}

for model_file in sorted(checkpoint_dir.glob("lda_model_k*.pkl")):
    k = int(model_file.stem.split('_k')[1])
    models[k] = LdaModel.load(str(model_file))
    print(f"Loaded k={k} model: {models[k].num_topics} topics")

# Compare topics across different k values
print("\nTopic 0 in different models:")
for k in sorted(models.keys()):
    print(f"k={k}: {models[k].print_topic(0, topn=5)}")
```

## 🔬 Analyzing Models

### Compare coherence scores:

The coherence scores are in the execution log (`outputs/logs/`), but you can recalculate:

```python
from gensim.models import LdaModel, CoherenceModel

# Load model and data
model = LdaModel.load("model_checkpoints/lda_model_k8.pkl")
# ... load corpus and texts (from main pipeline) ...

# Calculate coherence
coherence_model = CoherenceModel(
    model=model,
    texts=texts,
    dictionary=model.id2word,
    coherence='c_v',
    processes=1
)
coherence_score = coherence_model.get_coherence()
print(f"Coherence: {coherence_score:.4f}")
```

### Extract topic-word distributions:

```python
model = LdaModel.load("model_checkpoints/lda_model_k8.pkl")

# Get top words for all topics
for topic_id in range(model.num_topics):
    words = model.show_topic(topic_id, topn=20)
    print(f"\nTopic {topic_id}:")
    for word, prob in words:
        print(f"  {word}: {prob:.4f}")
```

### Predict document topics:

```python
from gensim import corpora

model = LdaModel.load("model_checkpoints/lda_model_k8.pkl")
dictionary = model.id2word

# New document
new_doc = ["photosynthesis", "light", "chlorophyll", "electron", "reaction"]
bow = dictionary.doc2bow(new_doc)

# Get topic distribution
topic_dist = model.get_document_topics(bow)
print("Topic distribution:")
for topic_id, prob in sorted(topic_dist, key=lambda x: x[1], reverse=True):
    print(f"  Topic {topic_id}: {prob:.4f}")
```

## 📊 Storage Information

### Typical Sizes (for 223 documents, ~11k vocabulary):

| k Value | Total Size | Number of Files |
|---------|------------|-----------------|
| k=2     | ~15 MB     | 4 files         |
| k=8     | ~25 MB     | 4 files         |
| k=20    | ~45 MB     | 4 files         |
| k=50    | ~90 MB     | 4 files         |

**Full directory (k=2 to k=50, step=2):** ~800 MB - 1.2 GB

### Space Management:

If disk space is limited:

```powershell
# Keep only models near the optimal k
# Example: Keep k=6, k=8, k=10 if optimal is k=8
Remove-Item model_checkpoints/lda_model_k2*
Remove-Item model_checkpoints/lda_model_k4*
Remove-Item model_checkpoints/lda_model_k12* -Recurse
# ... etc
```

Or keep only the optimal model:

```powershell
# Archive all models first (optional)
Compress-Archive -Path model_checkpoints -DestinationPath archive/all_models_20251117.zip

# Keep only k=8
Get-ChildItem model_checkpoints | Where-Object { $_.Name -notlike "*_k8*" } | Remove-Item
```

## 🔄 Model Updates

### Continuing Training:

Models can be updated with new data:

```python
model = LdaModel.load("model_checkpoints/lda_model_k8.pkl")

# Add more training passes with new/same corpus
model.update(corpus, passes=5)

# Save updated model
model.save("model_checkpoints/lda_model_k8_updated.pkl")
```

### Merging Models (Advanced):

Not directly supported, but you can:
1. Extract topics from multiple models
2. Combine vocabularies
3. Train new model with combined parameters

## 🗑️ Cleanup

### Safe to Delete:
- Models far from optimal k (e.g., if k=8 is optimal, delete k=2, k=4, k=40, k=50)
- `.state` files if you won't resume training (saves ~30% space)
- Old models from previous runs (if you've confirmed new results are better)

### Keep:
- Optimal model and 2-3 neighbors (e.g., k=6, k=8, k=10)
- Models you might want to compare or present
- `.id2word` files (needed for loading models)
- `.expElogbeta.npy` files (needed for topic inference)

### DO NOT Delete:
- All 4 files for any model you want to keep (model won't load properly)
- The entire directory before confirming you have outputs you need

## 🐛 Troubleshooting

### "Model file not found"
**Problem:** Script can't find model.

**Solution:**
```powershell
# List available models
ls model_checkpoints/*.pkl

# Check if training completed
cat outputs/logs/topic_modeling_*.log | Select-String "Saved model"
```

### "Model loading error"
**Problem:** Model is corrupted or incomplete.

**Solution:**
- Re-run main pipeline to regenerate models
- Check all 4 files exist for that k value
- Verify files aren't 0 bytes

### "Out of memory when loading"
**Problem:** Large model (high k) doesn't fit in RAM.

**Solution:**
- Load on machine with more RAM
- Or load only specific components:
```python
# Load just the dictionary
from gensim.corpora import Dictionary
dictionary = Dictionary.load("model_checkpoints/lda_model_k50.pkl.id2word")
```

---

## 📚 Technical Details

**Model Format:** Gensim LdaModel (pickle-based)  
**Training Algorithm:** Variational Bayes (online LDA)  
**Hyperparameters:** 
- `alpha='auto'` (document-topic density, learned)
- `eta='auto'` (topic-word density, learned)
- `passes=10` (number of training passes)
- `iterations=400` (per-document inference iterations)

**Coherence Metric:** C_v (combination of indirect cosine similarity, NPMI, and boolean sliding window)

---

**Last Updated:** 2025-11-17  
**Storage Used:** ~800 MB - 1.2 GB (25 models)  
**Current Optimal:** k=8 (from previous run)

