# Advanced Analyses Implementation Plan

**Research Question**: Why is algae not being used for biofuel despite its promise?

**Approach**: Three quantitative analyses to elucidate commercialization barriers

---

## Analysis 1: Innovation Gap Analysis (Papers vs. Patents)

### Overview

**Methodology**: Cross-Domain Topic Projection (Science-Technology Linkage Analysis)

**Hypothesis**: "Ghost topics" with high academic activity but low patent activity reveal specific commercialization barriers.

**Data Sources**:
- ✅ Scientific papers: 223 papers (BERTopic trained)
- ✅ Patents: `machine-learning/patent-analysis/bq-results-*.csv`

### Implementation Steps

#### Phase 1: Prepare Patent Data

```python
# File: machine-learning/analyze_innovation_gap.py

import pandas as pd
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load existing scientific paper topics
scientific_model = BERTopic.load("bertopic_outputs/bertopic_model_20251119_130232")
scientific_topics = pd.read_csv("bertopic_outputs/document_topics_20251119_130232.csv")

# 2. Load patent data
patents = pd.read_csv("patent-analysis/bq-results-20251119-051840-1763529534350.csv")

# 3. Preprocess patent abstracts (same pipeline as papers)
def clean_patent_text(text):
    # Apply same cleaning as run_bertopic_analysis.py
    # Remove URLs, DOIs, special chars
    pass

patents['cleaned_abstract'] = patents['abstract'].apply(clean_patent_text)
```

#### Phase 2: Project Patents into Paper Topic Space

```python
# Key technique: Use the SAME embedding model and project into existing topic space
# Do NOT retrain - we want to see where patents fall in the scientific landscape

# 4. Generate embeddings for patents using same model
embedding_model = scientific_model.embedding_model
patent_embeddings = embedding_model.encode(patents['cleaned_abstract'].tolist(), 
                                           show_progress_bar=True)

# 5. Project patents into existing topic space
patent_topics, patent_probs = scientific_model.transform(
    patents['cleaned_abstract'].tolist(),
    embeddings=patent_embeddings
)

# 6. Add to dataframe
patents['topic'] = patent_topics
patents['topic_probability'] = [prob.max() for prob in patent_probs]
```

#### Phase 3: Innovation Gap Calculation

```python
# 7. Compare distributions
scientific_dist = scientific_topics['topic'].value_counts(normalize=True)
patent_dist = patents['topic'].value_counts(normalize=True)

# 8. Calculate Innovation Gap Index for each topic
innovation_gap = pd.DataFrame({
    'topic': scientific_dist.index,
    'paper_proportion': scientific_dist.values,
    'patent_proportion': patent_dist.reindex(scientific_dist.index, fill_value=0).values
})

# Innovation Gap Index = (Papers % - Patents %) / Papers %
# High positive value = "Ghost Topic" (lots of papers, few patents)
innovation_gap['gap_index'] = (
    (innovation_gap['paper_proportion'] - innovation_gap['patent_proportion']) / 
    innovation_gap['paper_proportion']
)

# Absolute density difference
innovation_gap['gap_absolute'] = (
    innovation_gap['paper_proportion'] - innovation_gap['patent_proportion']
)

# Get topic names from model
topic_info = scientific_model.get_topic_info()
innovation_gap = innovation_gap.merge(
    topic_info[['Topic', 'Name']], 
    left_on='topic', 
    right_on='Topic'
)

# Sort by gap index
innovation_gap = innovation_gap.sort_values('gap_index', ascending=False)
```

#### Phase 4: Visualization and Interpretation

```python
# 9. Create Innovation Gap visualization
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Plot 1: Diverging bar chart
topics = innovation_gap['Name'].str[:40]
x = np.arange(len(topics))

axes[0].barh(x, innovation_gap['paper_proportion'], 
            alpha=0.7, label='Scientific Papers', color='steelblue')
axes[0].barh(x, -innovation_gap['patent_proportion'], 
            alpha=0.7, label='Patents', color='coral')
axes[0].set_yticks(x)
axes[0].set_yticklabels(topics, fontsize=9)
axes[0].set_xlabel('Topic Proportion')
axes[0].set_title('Innovation Gap: Scientific Papers vs. Patents by Topic', 
                  fontsize=14, fontweight='bold')
axes[0].legend()
axes[0].axvline(0, color='black', linewidth=0.8)

# Plot 2: Gap Index with annotations
colors = ['red' if gi > 0.5 else 'orange' if gi > 0.2 else 'green' 
          for gi in innovation_gap['gap_index']]
axes[1].barh(x, innovation_gap['gap_index'], color=colors, alpha=0.8)
axes[1].set_yticks(x)
axes[1].set_yticklabels(topics, fontsize=9)
axes[1].set_xlabel('Innovation Gap Index (Higher = More Papers, Fewer Patents)')
axes[1].set_title('Ghost Topics: Academic Research Without Commercial Translation', 
                  fontsize=14, fontweight='bold')
axes[1].axvline(0.5, color='red', linestyle='--', alpha=0.5, 
                label='Critical Gap Threshold')
axes[1].legend()

plt.tight_layout()
plt.savefig('bertopic_outputs/innovation_gap_analysis.png', dpi=300, bbox_inches='tight')
```

#### Phase 5: Barrier Classification

```python
# 10. Classify barriers by topic characteristics
def classify_barrier(row):
    """
    Classify likely commercialization barrier based on gap pattern
    """
    gap_idx = row['gap_index']
    paper_count = row['paper_proportion'] * len(scientific_topics)
    patent_count = row['patent_proportion'] * len(patents)
    
    if gap_idx > 0.7:  # Very high papers, very low patents
        if 'genetic' in row['Name'].lower() or 'strain' in row['Name'].lower():
            return 'REGULATORY (GMO/Biosafety)'
        elif 'sustainability' in row['Name'].lower() or 'policy' in row['Name'].lower():
            return 'POLICY VOID (No Framework)'
        else:
            return 'TECHNICAL INFEASIBILITY'
    elif gap_idx > 0.3:  # Moderate gap
        return 'ECONOMIC (High Cost to Scale)'
    elif gap_idx < 0:  # More patents than papers
        return 'OVER-PATENTED (Patent Thicket)'
    else:
        return 'BALANCED (Normal Translation)'

innovation_gap['barrier_type'] = innovation_gap.apply(classify_barrier, axis=1)

# 11. Export results
innovation_gap.to_csv('bertopic_outputs/innovation_gap_results.csv', index=False)

# 12. Generate summary report
with open('bertopic_outputs/INNOVATION_GAP_REPORT.txt', 'w') as f:
    f.write("INNOVATION GAP ANALYSIS REPORT\n")
    f.write("=" * 80 + "\n\n")
    
    f.write("GHOST TOPICS (High Academic Activity, Low Commercial Activity):\n")
    f.write("-" * 80 + "\n")
    ghost_topics = innovation_gap[innovation_gap['gap_index'] > 0.5]
    for idx, row in ghost_topics.iterrows():
        f.write(f"\nTopic: {row['Name']}\n")
        f.write(f"  Papers: {row['paper_proportion']*100:.1f}%\n")
        f.write(f"  Patents: {row['patent_proportion']*100:.1f}%\n")
        f.write(f"  Gap Index: {row['gap_index']:.2f}\n")
        f.write(f"  Likely Barrier: {row['barrier_type']}\n")
    
    f.write("\n\nBALANCED TOPICS (Healthy Science-Technology Translation):\n")
    f.write("-" * 80 + "\n")
    balanced = innovation_gap[(innovation_gap['gap_index'] >= -0.2) & 
                              (innovation_gap['gap_index'] <= 0.2)]
    for idx, row in balanced.iterrows():
        f.write(f"\nTopic: {row['Name']}\n")
        f.write(f"  Papers: {row['paper_proportion']*100:.1f}%\n")
        f.write(f"  Patents: {row['patent_proportion']*100:.1f}%\n")

print("✓ Innovation Gap Analysis Complete")
```

### Expected Findings

**Ghost Topics (Likely)**:
- Sustainability Assessment & LCA (regulatory void - no framework to certify)
- Policy Frameworks (academic analysis, no practical implementation)
- Third-Generation Innovations (too early-stage, high risk)

**Balanced Topics (Likely)**:
- Biodiesel Production Technology (mature, established patents)
- Wastewater Treatment Integration (practical application)

**Over-Patented (Possible)**:
- Specific lipid extraction methods (patent thickets blocking entry)

### Thesis Integration

**Chapter Section**: "Quantifying the Commercialization Gap"

**Key Figure**: Diverging bar chart showing paper vs. patent distribution

**Key Table**: Innovation Gap Index by topic with barrier classification

**Citation Methodology**: "Cross-domain topic projection (Chen et al., 2023) using BERTopic framework"

---

## Analysis 2: Policy Stance Detection

### Overview

**Methodology**: Stance Detection NLP on Regulatory Documents

**Hypothesis**: Policy documents exhibit neutral or absent stance towards algae biofuels, creating regulatory void.

**Data Sources**:
- ✅ Policy documents: `machine-learning/policy-analysis/downloaded_policies/`
- ✅ Policy metadata: `machine-learning/policy-analysis/policies-export-2025-11-19.csv`

### Implementation Steps

#### Phase 1: Extract Text from Policy Documents

```python
# File: machine-learning/policy-analysis/analyze_policy_stance.py

import pandas as pd
import fitz  # PyMuPDF
from bs4 import BeautifulSoup
import os
from pathlib import Path
from transformers import pipeline
import re

# 1. Extract text from all policy documents
def extract_policy_text(file_path):
    """Extract text from PDF, HTML, or TXT"""
    ext = Path(file_path).suffix.lower()
    
    if ext == '.pdf':
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    
    elif ext == '.html':
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            return soup.get_text()
    
    elif ext == '.txt':
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    
    return ""

# 2. Process all downloaded policies
policy_dir = Path("downloaded_policies")
policies = []

for policy_file in policy_dir.iterdir():
    if policy_file.is_file():
        text = extract_policy_text(policy_file)
        overton_id = policy_file.stem
        
        policies.append({
            'overton_id': overton_id,
            'filename': policy_file.name,
            'text': text,
            'text_length': len(text)
        })

policy_texts = pd.DataFrame(policies)

# 3. Load metadata
metadata = pd.read_csv("policies-export-2025-11-19.csv")
policy_texts = policy_texts.merge(
    metadata, 
    left_on='overton_id', 
    right_on='Overton id',
    how='left'
)
```

#### Phase 2: Stance Detection Using Pre-trained Models

```python
# 4. Load stance detection model
# Options:
# - "cardiffnlp/twitter-roberta-base-stance" (general stance)
# - "climatebert/distilroberta-base-climate-stance" (climate-specific)
# - Custom fine-tuned model on biofuel policy corpus

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Using ClimateBERT for environmental policy stance
model_name = "climatebert/distilroberta-base-climate-f"  # Or stance variant
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Alternative: Use zero-shot classification for more flexibility
classifier = pipeline("zero-shot-classification", 
                     model="facebook/bart-large-mnli")

# 5. Define target topics for stance detection
targets = {
    'first_gen': ['first generation biofuels', 'corn ethanol', 'biodiesel from crops'],
    'third_gen_algae': ['algae biofuel', 'microalgae biodiesel', 'third generation biofuel', 
                        'algal biomass', 'phytoplankton fuel'],
    'sustainability': ['sustainable biofuel', 'renewable fuel standard', 'carbon neutral'],
    'commercialization': ['commercial production', 'scale-up', 'industrial biofuel']
}

# 6. Detect stance for each policy document (segment-level analysis)
def segment_document(text, max_length=500):
    """Break document into analyzable segments (paragraphs or chunks)"""
    # Split by paragraphs
    paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 100]
    return paragraphs

def detect_stance_zero_shot(text_segment, target_keywords):
    """
    Use zero-shot classification to detect stance
    Labels: Support, Oppose, Neutral
    """
    hypothesis_template = "This text supports {}"
    
    # Check if text mentions the target at all
    mentions_target = any(kw.lower() in text_segment.lower() for kw in target_keywords)
    
    if not mentions_target:
        return {'stance': 'Not Mentioned', 'confidence': 1.0, 'segment': text_segment[:200]}
    
    # Classify stance
    result = classifier(
        text_segment,
        candidate_labels=['support', 'oppose', 'neutral'],
        hypothesis_template=hypothesis_template
    )
    
    return {
        'stance': result['labels'][0],
        'confidence': result['scores'][0],
        'segment': text_segment[:200]
    }

# 7. Analyze each policy document
results = []

for idx, row in policy_texts.iterrows():
    doc_id = row['overton_id']
    doc_title = row['Title']
    full_text = row['text']
    
    if len(full_text) < 100:
        continue  # Skip empty/corrupted documents
    
    segments = segment_document(full_text)
    
    for target_name, target_keywords in targets.items():
        # Analyze each segment
        segment_stances = []
        
        for segment in segments[:20]:  # Limit to first 20 segments for speed
            stance = detect_stance_zero_shot(segment, target_keywords)
            if stance['stance'] != 'Not Mentioned':
                segment_stances.append(stance)
        
        # Aggregate stance for this document-target pair
        if len(segment_stances) > 0:
            # Majority vote weighted by confidence
            stance_counts = {}
            for s in segment_stances:
                stance_counts[s['stance']] = stance_counts.get(s['stance'], 0) + s['confidence']
            
            dominant_stance = max(stance_counts, key=stance_counts.get)
            avg_confidence = sum(s['confidence'] for s in segment_stances) / len(segment_stances)
            
            results.append({
                'overton_id': doc_id,
                'title': doc_title,
                'target': target_name,
                'stance': dominant_stance,
                'confidence': avg_confidence,
                'mentions': len(segment_stances),
                'sample_segment': segment_stances[0]['segment'] if segment_stances else ''
            })
        else:
            # Target not mentioned in document
            results.append({
                'overton_id': doc_id,
                'title': doc_title,
                'target': target_name,
                'stance': 'Not Mentioned',
                'confidence': 1.0,
                'mentions': 0,
                'sample_segment': ''
            })

stance_results = pd.DataFrame(results)
```

#### Phase 3: Comparative Stance Analysis

```python
# 8. Compare stance towards First Gen vs. Third Gen (Algae)
comparison = stance_results.groupby(['target', 'stance']).size().unstack(fill_value=0)
comparison_pct = comparison.div(comparison.sum(axis=1), axis=0) * 100

# 9. Calculate "Regulatory Void Index"
# High index = topic is mentioned infrequently or with neutral stance
void_index = []

for target in targets.keys():
    target_data = stance_results[stance_results['target'] == target]
    
    mention_rate = (target_data['stance'] != 'Not Mentioned').mean()
    support_rate = (target_data['stance'] == 'support').mean()
    neutral_rate = (target_data['stance'] == 'neutral').mean()
    
    # Void Index: Low mention + High neutral = Regulatory Void
    void_score = (1 - mention_rate) * 0.6 + neutral_rate * 0.4
    
    void_index.append({
        'target': target,
        'mention_rate': mention_rate,
        'support_rate': support_rate,
        'oppose_rate': (target_data['stance'] == 'oppose').mean(),
        'neutral_rate': neutral_rate,
        'void_index': void_score
    })

void_df = pd.DataFrame(void_index).sort_values('void_index', ascending=False)

# 10. Visualization
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Plot 1: Stance distribution by target
comparison_pct.plot(kind='bar', stacked=True, ax=axes[0, 0], 
                    color=['green', 'red', 'gray', 'lightgray'])
axes[0, 0].set_title('Policy Stance Distribution by Biofuel Type', fontweight='bold')
axes[0, 0].set_ylabel('Percentage of Documents')
axes[0, 0].legend(title='Stance', bbox_to_anchor=(1.05, 1))

# Plot 2: Regulatory Void Index
axes[0, 1].barh(void_df['target'], void_df['void_index'], 
                color=['red' if v > 0.5 else 'orange' for v in void_df['void_index']])
axes[0, 1].set_xlabel('Regulatory Void Index')
axes[0, 1].set_title('Regulatory Void: Low Mention + Neutral Stance', fontweight='bold')
axes[0, 1].axvline(0.5, color='red', linestyle='--', alpha=0.5)

# Plot 3: Mention rate comparison
mention_data = void_df[['target', 'mention_rate']].set_index('target')
mention_data.plot(kind='barh', ax=axes[1, 0], legend=False, color='steelblue')
axes[1, 0].set_xlabel('Mention Rate in Policy Documents')
axes[1, 0].set_title('Policy Attention by Biofuel Type', fontweight='bold')

# Plot 4: Support vs. Oppose
support_oppose = void_df[['target', 'support_rate', 'oppose_rate']].set_index('target')
support_oppose.plot(kind='barh', ax=axes[1, 1], color=['green', 'red'])
axes[1, 1].set_xlabel('Rate')
axes[1, 1].set_title('Policy Support vs. Opposition', fontweight='bold')
axes[1, 1].legend(['Support', 'Oppose'])

plt.tight_layout()
plt.savefig('policy-analysis/policy_stance_analysis.png', dpi=300, bbox_inches='tight')

# 11. Export results
stance_results.to_csv('policy-analysis/stance_detection_results.csv', index=False)
void_df.to_csv('policy-analysis/regulatory_void_index.csv', index=False)
```

#### Phase 4: Generate Insights Report

```python
# 12. Generate report
with open('policy-analysis/POLICY_STANCE_REPORT.txt', 'w') as f:
    f.write("POLICY STANCE DETECTION ANALYSIS REPORT\n")
    f.write("=" * 80 + "\n\n")
    
    f.write("REGULATORY VOID ANALYSIS:\n")
    f.write("-" * 80 + "\n")
    for idx, row in void_df.iterrows():
        f.write(f"\n{row['target'].upper().replace('_', ' ')}:\n")
        f.write(f"  Mention Rate: {row['mention_rate']*100:.1f}%\n")
        f.write(f"  Support Rate: {row['support_rate']*100:.1f}%\n")
        f.write(f"  Neutral Rate: {row['neutral_rate']*100:.1f}%\n")
        f.write(f"  Void Index: {row['void_index']:.2f}\n")
        
        if row['void_index'] > 0.5:
            f.write(f"  ⚠️  HIGH REGULATORY VOID - Investor Uncertainty\n")
    
    f.write("\n\nKEY FINDINGS:\n")
    f.write("-" * 80 + "\n")
    
    # Compare first gen vs third gen
    first_gen = void_df[void_df['target'] == 'first_gen'].iloc[0]
    third_gen = void_df[void_df['target'] == 'third_gen_algae'].iloc[0]
    
    f.write(f"\nFirst Generation Biofuels:\n")
    f.write(f"  Mentioned in {first_gen['mention_rate']*100:.0f}% of documents\n")
    f.write(f"  Support rate: {first_gen['support_rate']*100:.0f}%\n")
    
    f.write(f"\nThird Generation (Algae) Biofuels:\n")
    f.write(f"  Mentioned in {third_gen['mention_rate']*100:.0f}% of documents\n")
    f.write(f"  Support rate: {third_gen['support_rate']*100:.0f}%\n")
    
    if third_gen['void_index'] > first_gen['void_index']:
        diff = (third_gen['void_index'] - first_gen['void_index']) * 100
        f.write(f"\n⚠️  CRITICAL FINDING:\n")
        f.write(f"  Algae biofuels have {diff:.0f}% higher regulatory void than first gen.\n")
        f.write(f"  This creates INVESTMENT UNCERTAINTY - no clear policy framework.\n")

print("✓ Policy Stance Detection Complete")
```

### Expected Findings

**Hypothesis**: Third-gen algae biofuels will show:
- Low mention rate (<30% of policy documents)
- High neutral stance (>50% when mentioned)
- High void index (>0.6)

**Comparison**: First-gen biofuels will show:
- High mention rate (>70%)
- Clear support/oppose stances
- Low void index (<0.3)

**Thesis Implication**: "Regulatory void" prevents investment - companies need clear rules before committing capital.

### Dependencies

```bash
pip install transformers torch beautifulsoup4 pymupdf
```

---

## Analysis 3: Bibliometric-Enhanced Topic Modeling (BETM)

### Overview

**Two Sub-Analyses**:
1. **Dynamic Topic Modeling (DTM)** - Track topic evolution over time
2. **Funding Overlay** - Map research funding to topics

### 3A: Dynamic Topic Modeling

#### Implementation

```python
# File: machine-learning/analyze_dynamic_topics.py

import pandas as pd
from bertopic import BERTopic
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# 1. Load BERTopic results with timestamps
doc_topics = pd.read_csv("bertopic_outputs/document_topics_20251119_130232.csv")

# 2. Load bibliometric data with years
biblio_data = pd.read_excel("../bibliometric-analysis/reproducible-bibliometric-analysis/data/filtered_data_biblioshiny_ready.xlsx")

# 3. Merge on filename (need to match PDF filenames to biblio records)
# This requires matching DOI or Title
# Assuming you can create a mapping file

# 4. Use BERTopic's built-in Topics Over Time
scientific_model = BERTopic.load("bertopic_outputs/bertopic_model_20251119_130232")

# Prepare timestamps (need to extract from bibliometric data)
timestamps = biblio_data['PY'].astype(str).tolist()  # Publication Year
documents = doc_topics['cleaned_text'].tolist()

# Generate topics over time
topics_over_time = scientific_model.topics_over_time(
    documents, 
    timestamps,
    nr_bins=17  # 2009-2025 = 17 years
)

# 5. Visualize evolution
fig = scientific_model.visualize_topics_over_time(topics_over_time, top_n_topics=6)
fig.write_html("bertopic_outputs/topics_over_time.html")

# 6. Identify "Dead Topics" (peaked then disappeared)
topic_trends = topics_over_time.groupby('Topic')['Frequency'].apply(list)

dead_topics = []
for topic, frequencies in topic_trends.items():
    if len(frequencies) > 5:
        peak_year = frequencies.index(max(frequencies))
        recent_avg = sum(frequencies[-3:]) / 3
        peak_value = max(frequencies)
        
        # Dead if peak was >5 years ago and recent activity < 20% of peak
        if peak_year < len(frequencies) - 5 and recent_avg < 0.2 * peak_value:
            topic_info = scientific_model.get_topic(topic)
            dead_topics.append({
                'topic': topic,
                'topic_keywords': topic_info,
                'peak_year': 2009 + peak_year,
                'decline_rate': (peak_value - recent_avg) / peak_value
            })

dead_topics_df = pd.DataFrame(dead_topics)
dead_topics_df.to_csv("bertopic_outputs/dead_topics_analysis.csv", index=False)

# 7. Identify "Emerging Topics" (growing recently)
emerging_topics = []
for topic, frequencies in topic_trends.items():
    if len(frequencies) > 5:
        recent_growth = (frequencies[-1] - frequencies[-5]) / frequencies[-5]
        
        if recent_growth > 0.5:  # 50% growth in last 5 years
            topic_info = scientific_model.get_topic(topic)
            emerging_topics.append({
                'topic': topic,
                'topic_keywords': topic_info,
                'growth_rate': recent_growth
            })

emerging_df = pd.DataFrame(emerging_topics)
emerging_df.to_csv("bertopic_outputs/emerging_topics_analysis.csv", index=False)
```

### 3B: Funding Overlay Analysis

#### Implementation

```python
# File: machine-learning/analyze_funding_overlay.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# 1. Load bibliometric data with funding information
biblio_data = pd.read_excel(
    "../bibliometric-analysis/reproducible-bibliometric-analysis/data/filtered_data_biblioshiny_ready.xlsx"
)

# 2. Extract funding sources from FU (Funding Agency) field
def categorize_funding(funding_string):
    """Categorize funding as Government, Private, Academic, etc."""
    if pd.isna(funding_string):
        return 'Unknown'
    
    funding_upper = str(funding_string).upper()
    
    # Government agencies
    if any(term in funding_upper for term in ['NSF', 'DOE', 'USDA', 'NIH', 'EPA', 
                                                'DEPARTMENT', 'MINISTRY', 'NATIONAL']):
        return 'Government'
    
    # Industry/Private
    elif any(term in funding_upper for term in ['COMPANY', 'CORP', 'INC', 'LTD',
                                                  'FOUNDATION', 'PRIVATE']):
        return 'Industry'
    
    # Academic
    elif any(term in funding_upper for term in ['UNIVERSITY', 'COLLEGE', 'INSTITUTE']):
        return 'Academic'
    
    else:
        return 'Other'

biblio_data['funding_category'] = biblio_data['FU'].apply(categorize_funding)

# 3. Merge with BERTopic results (requires matching)
# Assume we can match on DOI or Title
doc_topics = pd.read_csv("bertopic_outputs/document_topics_20251119_130232.csv")

# Match biblio to topics (simplified - you'll need actual matching logic)
# This would require creating a lookup table between PDF filenames and DOI/Titles

# 4. Analyze funding distribution by topic
funding_by_topic = biblio_data.groupby(['topic', 'funding_category']).size().unstack(fill_value=0)

# 5. Calculate "Funding Mismatch Index"
# Topics with high papers but low industry funding = basic science trap
# Topics with high industry funding but low impact = wasted investment

funding_mismatch = []

for topic in funding_by_topic.index:
    gov_funding = funding_by_topic.loc[topic, 'Government']
    industry_funding = funding_by_topic.loc[topic, 'Industry']
    
    total_papers = funding_by_topic.loc[topic].sum()
    
    # Mismatch: High government (basic science) but low industry (commercialization)
    mismatch_score = gov_funding / (industry_funding + 1)  # Avoid division by zero
    
    funding_mismatch.append({
        'topic': topic,
        'government': gov_funding,
        'industry': industry_funding,
        'academic': funding_by_topic.loc[topic, 'Academic'],
        'mismatch_score': mismatch_score,
        'total_papers': total_papers
    })

mismatch_df = pd.DataFrame(funding_mismatch).sort_values('mismatch_score', ascending=False)

# 6. Visualization
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Plot 1: Funding by topic (stacked bar)
funding_by_topic_pct = funding_by_topic.div(funding_by_topic.sum(axis=1), axis=0) * 100
funding_by_topic_pct.plot(kind='barh', stacked=True, ax=axes[0, 0])
axes[0, 0].set_title('Funding Sources by Topic', fontweight='bold')
axes[0, 0].set_xlabel('Percentage of Papers')

# Plot 2: Mismatch score
axes[0, 1].barh(mismatch_df['topic'], mismatch_df['mismatch_score'],
                color=['red' if m > 5 else 'orange' if m > 2 else 'green' 
                       for m in mismatch_df['mismatch_score']])
axes[0, 1].set_title('Funding Mismatch: Gov/Industry Ratio', fontweight='bold')
axes[0, 1].set_xlabel('Mismatch Score (Higher = More Basic Science)')
axes[0, 1].axvline(2, color='red', linestyle='--', alpha=0.5)

# Plot 3: Industry funding vs citation impact
# (requires merging citation data)

# Plot 4: Temporal funding trends
# (requires temporal data)

plt.tight_layout()
plt.savefig('bertopic_outputs/funding_overlay_analysis.png', dpi=300, bbox_inches='tight')

# 7. Export
mismatch_df.to_csv('bertopic_outputs/funding_mismatch_results.csv', index=False)
```

### Expected Findings

**Dead Topics (Hypothesis)**:
- "Open Pond Systems" peaked 2010-2015, declined after
- Replaced by "Photobioreactors" (expensive tech)
- Industry didn't scale because cost increased

**Funding Mismatch (Hypothesis)**:
- "Genetic Engineering" - 90% government, 10% industry (regulatory barrier)
- "Lipid Extraction" - 80% government, 20% industry (technical challenge)
- "LCA/Sustainability" - 95% government, 5% industry (policy void)

**Commercialization Insight**: Money goes to basic science, not engineering bottlenecks like dewatering, harvesting, or process optimization.

---

## Implementation Roadmap

### Week 1: Innovation Gap Analysis
- [ ] Create `analyze_innovation_gap.py`
- [ ] Run patent projection
- [ ] Generate visualizations
- [ ] Draft findings section

### Week 2: Policy Stance Detection
- [ ] Extract text from policy documents
- [ ] Set up stance detection model
- [ ] Run analysis
- [ ] Generate comparative report

### Week 3: BETM - Dynamic Topics
- [ ] Match bibliometric data with topics
- [ ] Generate topics over time
- [ ] Identify dead/emerging topics
- [ ] Create temporal visualizations

### Week 4: BETM - Funding Overlay
- [ ] Parse funding sources
- [ ] Calculate mismatch indices
- [ ] Create funding visualizations
- [ ] Synthesize all findings

### Week 5: Integration & Writing
- [ ] Combine all three analyses
- [ ] Create master visualization dashboard
- [ ] Write methodology sections
- [ ] Draft results and discussion

---

## Dependencies

```bash
# Install all required packages
pip install transformers torch bertopic sentence-transformers
pip install pymupdf beautifulsoup4 pandas numpy
pip install matplotlib seaborn plotly
pip install scikit-learn umap-learn hdbscan
```

---

## Citation Framework

### Innovation Gap Analysis
**Citation**: "Cross-domain topic projection methodology adapted from Chen et al. (2023) using BERTopic semantic modeling"

### Policy Stance Detection
**Citation**: "Stance detection using transformer-based models (RoBERTa/ClimateBERT) following methods of Küçük & Can (2020)"

### Dynamic Topic Modeling
**Citation**: "Temporal topic evolution analysis using BERTopic's Topics Over Time functionality (Grootendorst, 2022)"

### Funding Overlay
**Citation**: "Bibliometric-enhanced topic modeling integrating funding metadata with semantic topics"

---

## Expected Thesis Contributions

1. **Quantitative Evidence** of commercialization failure
2. **Specific Barrier Identification** (regulatory vs. economic vs. technical)
3. **Policy Gaps** documented through stance analysis
4. **Funding Misallocation** proven through overlay analysis
5. **Temporal Dynamics** showing technology shifts and their consequences

**Result**: A data-driven answer to "Why isn't algae being used for biofuel?"


