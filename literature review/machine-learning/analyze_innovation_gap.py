"""
Innovation Gap Analysis: Scientific Papers vs. Patents
Cross-Domain Topic Projection to Identify Commercialization Barriers

This script projects patent data into the scientific paper topic space
to identify "ghost topics" with high academic activity but low commercial translation.

Author: PhD Research
Date: November 2025
"""

import sys
import io

# Fix Unicode encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import pandas as pd
import numpy as np
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import matplotlib.pyplot as plt
import seaborn as sns
import re
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)

print("=" * 80)
print("INNOVATION GAP ANALYSIS")
print("Cross-Domain Topic Projection: Papers vs. Patents")
print("=" * 80)

# =============================================================================
# STEP 1: LOAD TRAINED SCIENTIFIC PAPER MODEL
# =============================================================================

print("\n[1/7] Loading trained BERTopic model from scientific papers...")

# Load the existing model trained on scientific papers
MODEL_PATH = "bertopic_outputs/bertopic_model_20251119_130232"

# Load embedding model explicitly
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
embedding_model = SentenceTransformer(EMBEDDING_MODEL)

# Load BERTopic model with embedding model
scientific_model = BERTopic.load(MODEL_PATH, embedding_model=embedding_model)

# Load scientific paper topic assignments
PAPERS_PATH = "bertopic_outputs/document_topics_20251119_130232.csv"
scientific_topics = pd.read_csv(PAPERS_PATH)

print(f"[OK] Loaded model with {len(scientific_model.get_topic_info())} topics")
print(f"[OK] Scientific papers: {len(scientific_topics)} documents")

# =============================================================================
# STEP 2: LOAD AND PREPROCESS PATENT DATA
# =============================================================================

print("\n[2/7] Loading patent data from BigQuery results...")

PATENT_PATH = "patent-analysis/bq-results-20251119-051840-1763529534350.csv"
patents = pd.read_csv(PATENT_PATH)

print(f"[OK] Loaded {len(patents)} patents")

# Preprocess patent abstracts (same cleaning as papers)
def clean_patent_text(text):
    """
    Clean patent text using same preprocessing as scientific papers
    """
    if not isinstance(text, str):
        return ""
    
    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)
    
    # Remove DOIs
    text = re.sub(r'doi:\S+|DOI:\S+', '', text)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove special characters but preserve domain terms
    text = re.sub(r'[^\w\s\-\.°\+\^\-]', ' ', text)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    
    text = text.strip()
    
    return text

print("\n[3/7] Preprocessing patent abstracts...")
patents['cleaned_abstract'] = patents['abstract'].apply(clean_patent_text)

# Filter out patents with insufficient content
MIN_ABSTRACT_LENGTH = 100
patents = patents[patents['cleaned_abstract'].str.len() >= MIN_ABSTRACT_LENGTH].copy()

print(f"[OK] {len(patents)} patents after filtering (min {MIN_ABSTRACT_LENGTH} chars)")

# =============================================================================
# STEP 3: PROJECT PATENTS INTO SCIENTIFIC TOPIC SPACE
# =============================================================================

print("\n[4/7] Generating embeddings for patents using same model as papers...")

# Generate embeddings for patent abstracts
patent_abstracts = patents['cleaned_abstract'].tolist()
patent_embeddings = embedding_model.encode(
    patent_abstracts,
    show_progress_bar=True,
    batch_size=32
)

print(f"[OK] Generated embeddings: {patent_embeddings.shape}")

print("\n[5/7] Projecting patents into scientific topic space...")

# Transform patents using the scientific paper model
# This assigns each patent to the closest scientific topic
patent_topics, patent_probs = scientific_model.transform(
    patent_abstracts,
    embeddings=patent_embeddings
)

# Add to dataframe
patents['topic'] = patent_topics
patents['topic_probability'] = [prob.max() if len(prob) > 0 else 0 for prob in patent_probs]

print(f"[OK] Patents assigned to {len(set(patent_topics))} different topics")

# =============================================================================
# STEP 4: CALCULATE INNOVATION GAP INDEX
# =============================================================================

print("\n[6/7] Calculating Innovation Gap Index...")

# Get topic distributions
scientific_dist = scientific_topics['topic'].value_counts(normalize=True).sort_index()
patent_dist = patents['topic'].value_counts(normalize=True).sort_index()

# Create comparison dataframe
innovation_gap = pd.DataFrame({
    'topic': scientific_dist.index,
    'paper_proportion': scientific_dist.values,
    'patent_proportion': patent_dist.reindex(scientific_dist.index, fill_value=0).values
})

# Calculate gap metrics
innovation_gap['gap_absolute'] = (
    innovation_gap['paper_proportion'] - innovation_gap['patent_proportion']
)

innovation_gap['gap_index'] = (
    innovation_gap['gap_absolute'] / innovation_gap['paper_proportion']
)

innovation_gap['paper_count'] = [
    (scientific_topics['topic'] == t).sum() for t in innovation_gap['topic']
]

innovation_gap['patent_count'] = [
    (patents['topic'] == t).sum() for t in innovation_gap['topic']
]

# Get topic names from model
topic_info = scientific_model.get_topic_info()
innovation_gap = innovation_gap.merge(
    topic_info[['Topic', 'Name']], 
    left_on='topic', 
    right_on='Topic',
    how='left'
)

# Sort by gap index
innovation_gap = innovation_gap.sort_values('gap_index', ascending=False)

print(f"[OK] Innovation gap calculated for {len(innovation_gap)} topics")

# Classify barriers
def classify_barrier(row):
    """
    Classify likely commercialization barrier based on gap pattern
    """
    gap_idx = row['gap_index']
    topic_name = str(row['Name']).lower()
    
    if gap_idx > 0.7:  # Very high gap
        if any(term in topic_name for term in ['genetic', 'strain', 'engineering']):
            return 'REGULATORY (GMO/Biosafety)'
        elif any(term in topic_name for term in ['sustainability', 'policy', 'assessment']):
            return 'POLICY VOID (No Framework)'
        elif any(term in topic_name for term in ['future', 'innovation', 'third generation']):
            return 'EARLY STAGE (Not Ready)'
        else:
            return 'TECHNICAL INFEASIBILITY'
    
    elif gap_idx > 0.3:  # Moderate gap
        if any(term in topic_name for term in ['extraction', 'harvesting', 'processing']):
            return 'ECONOMIC (Cost Barrier)'
        else:
            return 'SCALING CHALLENGE'
    
    elif gap_idx < 0:  # More patents than papers
        return 'OVER-PATENTED (Patent Thicket)'
    
    else:  # Balanced
        return 'HEALTHY TRANSLATION'

innovation_gap['barrier_type'] = innovation_gap.apply(classify_barrier, axis=1)

# =============================================================================
# STEP 5: VISUALIZATION
# =============================================================================

print("\n[7/7] Generating visualizations...")

fig, axes = plt.subplots(3, 1, figsize=(14, 16))

# Plot 1: Diverging bar chart (Papers vs Patents)
topics_labels = innovation_gap['Name'].str[:50]
x = np.arange(len(topics_labels))

axes[0].barh(x, innovation_gap['paper_proportion'], 
            alpha=0.7, label='Scientific Papers', color='steelblue')
axes[0].barh(x, -innovation_gap['patent_proportion'], 
            alpha=0.7, label='Patents', color='coral')
axes[0].set_yticks(x)
axes[0].set_yticklabels(topics_labels, fontsize=9)
axes[0].set_xlabel('Topic Proportion', fontsize=12, fontweight='bold')
axes[0].set_title('Innovation Gap: Scientific Papers vs. Patents by Topic', 
                  fontsize=14, fontweight='bold')
axes[0].legend(loc='upper right')
axes[0].axvline(0, color='black', linewidth=0.8)
axes[0].grid(axis='x', alpha=0.3)

# Plot 2: Gap Index with color coding
colors = ['darkred' if gi > 0.7 else 'red' if gi > 0.5 else 'orange' if gi > 0.2 else 'green' 
          for gi in innovation_gap['gap_index']]

axes[1].barh(x, innovation_gap['gap_index'], color=colors, alpha=0.8)
axes[1].set_yticks(x)
axes[1].set_yticklabels(topics_labels, fontsize=9)
axes[1].set_xlabel('Innovation Gap Index (Higher = More Papers, Fewer Patents)', 
                   fontsize=12, fontweight='bold')
axes[1].set_title('Ghost Topics: Academic Research Without Commercial Translation', 
                  fontsize=14, fontweight='bold')
axes[1].axvline(0.7, color='darkred', linestyle='--', alpha=0.5, linewidth=1, 
                label='Critical Gap')
axes[1].axvline(0.3, color='orange', linestyle='--', alpha=0.5, linewidth=1, 
                label='Moderate Gap')
axes[1].legend(loc='upper right')
axes[1].grid(axis='x', alpha=0.3)

# Plot 3: Absolute counts
width = 0.4
axes[2].barh(x - width/2, innovation_gap['paper_count'], width, 
            label='Papers', color='steelblue', alpha=0.7)
axes[2].barh(x + width/2, innovation_gap['patent_count'], width, 
            label='Patents', color='coral', alpha=0.7)
axes[2].set_yticks(x)
axes[2].set_yticklabels(topics_labels, fontsize=9)
axes[2].set_xlabel('Document Count', fontsize=12, fontweight='bold')
axes[2].set_title('Absolute Document Counts by Topic', fontsize=14, fontweight='bold')
axes[2].legend(loc='upper right')
axes[2].grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('bertopic_outputs/innovation_gap_analysis.png', dpi=300, bbox_inches='tight')
print("[OK] Saved: bertopic_outputs/innovation_gap_analysis.png")

# =============================================================================
# STEP 6: EXPORT RESULTS
# =============================================================================

# Save detailed results
innovation_gap.to_csv('bertopic_outputs/innovation_gap_results.csv', index=False)
print("[OK] Saved: bertopic_outputs/innovation_gap_results.csv")

# Save patent topic assignments
patents[['publication_number', 'title', 'topic', 'topic_probability', 'country_code', 
         'publication_date']].to_csv('bertopic_outputs/patent_topic_assignments.csv', index=False)
print("[OK] Saved: bertopic_outputs/patent_topic_assignments.csv")

# =============================================================================
# STEP 7: GENERATE SUMMARY REPORT
# =============================================================================

with open('bertopic_outputs/INNOVATION_GAP_REPORT.txt', 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("INNOVATION GAP ANALYSIS REPORT\n")
    f.write("Cross-Domain Topic Projection: Scientific Papers vs. Patents\n")
    f.write("=" * 80 + "\n\n")
    
    f.write("SUMMARY STATISTICS:\n")
    f.write("-" * 80 + "\n")
    f.write(f"Scientific Papers Analyzed: {len(scientific_topics)}\n")
    f.write(f"Patents Analyzed: {len(patents)}\n")
    f.write(f"Topics Identified: {len(innovation_gap)}\n")
    f.write(f"Average Gap Index: {innovation_gap['gap_index'].mean():.2f}\n\n")
    
    f.write("GHOST TOPICS (High Academic Activity, Low Commercial Activity):\n")
    f.write("=" * 80 + "\n")
    ghost_topics = innovation_gap[innovation_gap['gap_index'] > 0.5]
    
    for idx, row in ghost_topics.iterrows():
        f.write(f"\n{row['Name']}\n")
        f.write("-" * 80 + "\n")
        f.write(f"  Gap Index: {row['gap_index']:.2f}\n")
        f.write(f"  Scientific Papers: {row['paper_count']} ({row['paper_proportion']*100:.1f}%)\n")
        f.write(f"  Patents: {row['patent_count']} ({row['patent_proportion']*100:.1f}%)\n")
        f.write(f"  Likely Barrier: {row['barrier_type']}\n")
        
        # Get top keywords for this topic
        topic_keywords = scientific_model.get_topic(int(row['topic']))
        if topic_keywords:
            keywords = ', '.join([kw[0] for kw in topic_keywords[:5]])
            f.write(f"  Key Terms: {keywords}\n")
    
    f.write("\n\nBALANCED TOPICS (Healthy Science-Technology Translation):\n")
    f.write("=" * 80 + "\n")
    balanced = innovation_gap[(innovation_gap['gap_index'] >= -0.2) & 
                              (innovation_gap['gap_index'] <= 0.2)]
    
    for idx, row in balanced.iterrows():
        f.write(f"\n{row['Name']}\n")
        f.write(f"  Papers: {row['paper_count']}, Patents: {row['patent_count']}\n")
        f.write(f"  Status: {row['barrier_type']}\n")
    
    if len(balanced) == 0:
        f.write("\n⚠️  NO BALANCED TOPICS FOUND\n")
        f.write("This suggests systematic commercialization failure across all areas.\n")
    
    f.write("\n\nKEY FINDINGS:\n")
    f.write("=" * 80 + "\n")
    
    # Calculate overall gap
    total_gap = innovation_gap['gap_index'].mean()
    critical_gaps = len(innovation_gap[innovation_gap['gap_index'] > 0.7])
    
    f.write(f"\n1. Overall Innovation Gap: {total_gap:.2f}\n")
    f.write(f"   - {critical_gaps} topics with CRITICAL gaps (>0.7)\n")
    f.write(f"   - {len(ghost_topics)} topics with HIGH gaps (>0.5)\n\n")
    
    f.write("2. Barrier Classification:\n")
    barrier_counts = innovation_gap['barrier_type'].value_counts()
    for barrier, count in barrier_counts.items():
        f.write(f"   - {barrier}: {count} topics\n")
    
    f.write("\n3. Implications for Commercialization:\n")
    if total_gap > 0.5:
        f.write("   ⚠️  CRITICAL: Systematic failure to translate research to technology\n")
        f.write("   - High academic output NOT matched by commercial activity\n")
        f.write("   - Suggests fundamental barriers preventing scale-up\n")
    
    f.write("\n" + "=" * 80 + "\n")
    f.write("END OF REPORT\n")
    f.write("=" * 80 + "\n")

print("✓ Saved: bertopic_outputs/INNOVATION_GAP_REPORT.txt")

# =============================================================================
# FINAL SUMMARY
# =============================================================================

print("\n" + "=" * 80)
print("✓ INNOVATION GAP ANALYSIS COMPLETE")
print("=" * 80)

print(f"\nKey Outputs:")
print(f"  • Visualization: bertopic_outputs/innovation_gap_analysis.png")
print(f"  • Detailed Results: bertopic_outputs/innovation_gap_results.csv")
print(f"  • Patent Assignments: bertopic_outputs/patent_topic_assignments.csv")
print(f"  • Summary Report: bertopic_outputs/INNOVATION_GAP_REPORT.txt")

print(f"\nKey Findings:")
print(f"  • Ghost Topics (gap > 0.5): {len(ghost_topics)}")
print(f"  • Balanced Topics: {len(balanced)}")
print(f"  • Average Gap Index: {innovation_gap['gap_index'].mean():.2f}")

print(f"\nTop 3 Ghost Topics:")
for idx, row in ghost_topics.head(3).iterrows():
    print(f"  • {row['Name'][:60]}")
    print(f"    Gap: {row['gap_index']:.2f}, Barrier: {row['barrier_type']}")

print("\n" + "=" * 80)

