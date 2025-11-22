# Configuration Update Summary

## Changes Made for Extended Topic Range and Enhanced N-grams

### 1. Extended Topic Range (k=2 to k=50)

**Previous:**
```python
TOPIC_RANGE_START = 2
TOPIC_RANGE_END = 21      # Tested up to k=20
TOPIC_STEP = 1
```

**Updated:**
```python
TOPIC_RANGE_START = 2
TOPIC_RANGE_END = 51      # Now tests up to k=50
TOPIC_STEP = 2            # Tests every 2nd value for efficiency
```

**Why:** Since k=20 had the highest coherence in your first run, testing higher values (up to k=50) will help find the true optimal number of topics.

**Impact on Runtime:**
- Previous: 19 models (k=2 to k=20)
- Current: 25 models (k=2,4,6,8...48,50)
- **Estimated time:** ~3-5 hours (vs 2-4 hours before)

**To test every value (k=2,3,4...50):**
- Change `TOPIC_STEP = 1` (will test 49 models, ~6-8 hours)

---

### 2. Enhanced N-gram Detection

**What Changed:**

```python
# BEFORE:
BIGRAM_MIN_COUNT = 5       # Required 5 occurrences
BIGRAM_THRESHOLD = 100     # High threshold = fewer phrases

# AFTER:
BIGRAM_MIN_COUNT = 3       # Lowered to catch more phrases
BIGRAM_THRESHOLD = 50      # Lowered threshold = more phrases
TRIGRAM_MIN_COUNT = 3      # New parameter for trigrams
TRIGRAM_THRESHOLD = 50     # New parameter for trigrams
```

**Why These Changes:**

1. **Lower min_count (5→3):** Captures meaningful phrases that appear less frequently
   - Example: "carbon_dioxide_emission" might only appear 4 times but is important

2. **Lower threshold (100→50):** More aggressive phrase detection
   - Captures more domain-specific multi-word terms
   - Better semantic coherence in topics

3. **Separate trigram parameters:** Fine-tuned control over 3-word phrases
   - Example: "life_cycle_assessment", "greenhouse_gas_emission"

**Expected Results:**
- ✅ More meaningful multi-word concepts in topics
- ✅ Better semantic coherence (technical terms kept together)
- ✅ More readable topic keywords
- ⚠️ Slightly larger vocabulary (more n-grams included)

---

## How N-grams Improve Coherence

### Before N-grams:
```
Topic 5: emission, greenhouse, gas, carbon, dioxide, assessment, cycle, life
```
Problems: Words are separated, meaning unclear

### After N-grams:
```
Topic 5: greenhouse_gas_emission, carbon_dioxide, life_cycle_assessment, emission_reduction
```
Benefits: Concepts kept together, clearer meaning, better coherence

---

## What to Expect in Your Next Run

### 1. More Detected Phrases
You'll see output like:
```
Sample detected phrases:
  • greenhouse_gas
  • life_cycle_assessment
  • carbon_dioxide_emission
  • biofuel_production
  • renewable_energy
  • climate_change
  • fossil_fuel
  • microalgae_biomass
  ... and many more
```

### 2. Longer Training Time
```
Testing topic counts from k=2 to k=50...
Total models to train: 25

Training LDA models:  20%|████      | 5/25 [45:00<2:30:00, 450s/model]
  → Training LDA with k=10 topics...
  ✓ k=10 complete. Coherence: 0.4892
```

### 3. Better Coherence Scores
- Previous best: k=20 with coherence ~0.48-0.50
- Expected: Higher scores with better k value (likely k=25-35)
- N-grams typically improve coherence by 5-15%

### 4. More Interpretable Topics
Keywords will be more meaningful:
- Instead of: "climate, change, warming, global"
- You'll get: "climate_change, global_warming, temperature_rise"

---

## Monitoring Progress

### During Execution:
```
STAGE 3: Detecting Bigrams and Trigrams
Training bigram model...
✓ N-gram detection complete

Sample detected phrases:  <-- Check this section!
  • biofuel_production
  • renewable_energy
  • carbon_footprint
  [Should see MANY more phrases than before]
```

### After Execution:
Check the coherence plot (`coherence_plot.png`):
- Look for peak between k=20 and k=50
- Coherence should plateau or peak in the k=25-40 range
- If it keeps increasing, may need to test k=60+

---

## Fine-Tuning Options

### If you get TOO MANY n-grams (overly fragmented):
```python
BIGRAM_MIN_COUNT = 5       # Increase back
BIGRAM_THRESHOLD = 75      # Increase threshold
```

### If you get TOO FEW n-grams (not enough phrases):
```python
BIGRAM_MIN_COUNT = 2       # Lower further
BIGRAM_THRESHOLD = 30      # Lower threshold
```

### If coherence peaks early (say k=15):
```python
TOPIC_RANGE_START = 5      # Start higher
TOPIC_RANGE_END = 31       # Test k=5 to k=30
TOPIC_STEP = 1             # Test every value in that range
```

---

## Quick Start for Your Next Run

```powershell
cd D:\Github\phd\ML
python refined-topic-model.py
```

**The script will:**
1. ✅ Test k=2,4,6,8...48,50 (25 models)
2. ✅ Detect more bigrams and trigrams with lower thresholds
3. ✅ Save all checkpoints as before
4. ✅ Generate updated visualizations with new optimal k

**Estimated time:** 3-5 hours

---

## Comparing Results

### After the run completes:

1. **Check coherence plot:**
   - Compare peak in new run vs old run (k=20)
   - Note the new optimal k value

2. **Compare topic quality:**
   ```powershell
   python create_topic_review_doc.py
   ```
   - Compare keywords: More meaningful phrases?
   - Better topic separation?

3. **Check n-gram examples:**
   - Look in the console output during STAGE 3
   - Should see 50-200+ detected phrases (vs ~20-50 before)

---

## Notes

- **First run:** k=20, coherence ~0.48-0.50, testing k=2-20
- **This run:** Testing k=2-50, enhanced n-grams, expecting higher coherence
- **Hypothesis:** Optimal k likely in 25-40 range with improved coherence due to n-grams

**Date configured:** 2025-11-16  
**Ready to run!**

