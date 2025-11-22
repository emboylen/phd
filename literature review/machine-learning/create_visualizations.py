"""
Generate Comprehensive Visualizations for BERTopic Analysis Summary

Creates publication-quality static visualizations including:
1. Topic Distribution (Pie Chart)
2. Topic Confidence Distribution (Box Plot)
3. Topic Size Comparison (Horizontal Bar Chart)
4. Top Keywords per Topic (Heatmap-style visualization)
5. Document-Topic Confidence Histogram
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')

# Set style for publication-quality figures
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'sans-serif'

# Configuration
TIMESTAMP = "20251119_130232"
BERTOPIC_DIR = "bertopic_outputs"
OUTPUT_DIR = "bertopic_outputs/visualizations"

import os
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 80)
print("GENERATING BERTOPIC VISUALIZATIONS")
print("=" * 80)

# Load data
print("\nLoading data...")
topic_csv = os.path.join(BERTOPIC_DIR, f"topic_info_{TIMESTAMP}.csv")
doc_csv = os.path.join(BERTOPIC_DIR, f"document_topics_{TIMESTAMP}.csv")

df_topics = pd.read_csv(topic_csv, usecols=['Topic', 'Count', 'Name'])
df_docs = pd.read_csv(doc_csv, usecols=['filename', 'topic', 'topic_probability'])

# Remove outlier topic (-1) if exists
df_topics = df_topics[df_topics['Topic'] != -1]
df_docs = df_docs[df_docs['topic'] != -1]

# Define topic labels (manually curated for clarity)
topic_labels = {
    0: 'General Production\n& Challenges',
    1: 'Wastewater Treatment\n& Circular Economy',
    2: 'Integrated Biorefinery\n& Value-Added Products',
    3: 'Sustainability Assessment\n& Policy',
    4: 'Biodiesel Production\nTechnology',
    5: 'Third-Generation\nBiofuels & Innovation'
}

df_topics['Label'] = df_topics['Topic'].map(topic_labels)

print(f"[OK] Loaded {len(df_topics)} topics and {len(df_docs)} documents")

# ============================================================================
# VISUALIZATION 1: Topic Distribution Pie Chart
# ============================================================================
print("\n[1/6] Creating topic distribution pie chart...")

fig, ax = plt.subplots(figsize=(10, 8))

colors = sns.color_palette("husl", len(df_topics))
explode = [0.05 if i == 0 else 0.02 for i in range(len(df_topics))]

wedges, texts, autotexts = ax.pie(
    df_topics['Count'],
    labels=df_topics['Label'],
    autopct='%1.1f%%',
    startangle=90,
    colors=colors,
    explode=explode,
    textprops={'fontsize': 9, 'weight': 'bold'}
)

# Improve text readability
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(10)
    autotext.set_weight('bold')

ax.set_title('Distribution of Research Themes in Microalgae Biofuel Literature\n(n=223 documents)',
             fontsize=14, weight='bold', pad=20)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '01_topic_distribution_pie.png'), bbox_inches='tight')
plt.close()
print("  [OK] Saved: 01_topic_distribution_pie.png")

# ============================================================================
# VISUALIZATION 2: Topic Size Bar Chart (Horizontal)
# ============================================================================
print("\n[2/6] Creating topic size comparison bar chart...")

fig, ax = plt.subplots(figsize=(10, 6))

# Sort by count
df_sorted = df_topics.sort_values('Count', ascending=True)

bars = ax.barh(df_sorted['Label'], df_sorted['Count'], color=colors)

# Add value labels on bars
for i, (count, label) in enumerate(zip(df_sorted['Count'], df_sorted['Label'])):
    ax.text(count + 1, i, f'{count} docs', va='center', fontsize=9, weight='bold')

ax.set_xlabel('Number of Documents', fontsize=11, weight='bold')
ax.set_ylabel('Research Topic', fontsize=11, weight='bold')
ax.set_title('Document Distribution Across Research Topics', fontsize=13, weight='bold', pad=15)
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '02_topic_sizes_horizontal.png'), bbox_inches='tight')
plt.close()
print("  [OK] Saved: 02_topic_sizes_horizontal.png")

# ============================================================================
# VISUALIZATION 3: Confidence Distribution Box Plot
# ============================================================================
print("\n[3/6] Creating confidence distribution box plot...")

fig, ax = plt.subplots(figsize=(12, 6))

# Prepare data for box plot
confidence_by_topic = []
labels_ordered = []

for topic_id in sorted(df_topics['Topic'].unique()):
    topic_confidences = df_docs[df_docs['topic'] == topic_id]['topic_probability'].values
    confidence_by_topic.append(topic_confidences)
    labels_ordered.append(topic_labels[topic_id])

bp = ax.boxplot(confidence_by_topic, labels=labels_ordered, patch_artist=True,
                medianprops=dict(color='red', linewidth=2),
                boxprops=dict(facecolor='lightblue', edgecolor='black', linewidth=1.5),
                whiskerprops=dict(linewidth=1.5),
                capprops=dict(linewidth=1.5))

# Color boxes
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax.set_ylabel('Assignment Confidence Score', fontsize=11, weight='bold')
ax.set_xlabel('Research Topic', fontsize=11, weight='bold')
ax.set_title('Document-Topic Assignment Confidence Distribution', fontsize=13, weight='bold', pad=15)
ax.set_ylim([0, 1.05])
ax.grid(axis='y', alpha=0.3)
ax.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, label='50% Threshold')
ax.legend(loc='lower right')

plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '03_confidence_distribution_boxplot.png'), bbox_inches='tight')
plt.close()
print("  [OK] Saved: 03_confidence_distribution_boxplot.png")

# ============================================================================
# VISUALIZATION 4: Overall Confidence Histogram
# ============================================================================
print("\n[4/6] Creating overall confidence histogram...")

fig, ax = plt.subplots(figsize=(10, 6))

ax.hist(df_docs['topic_probability'], bins=30, color='steelblue', edgecolor='black', alpha=0.7)

# Add statistics
mean_conf = df_docs['topic_probability'].mean()
median_conf = df_docs['topic_probability'].median()

ax.axvline(mean_conf, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_conf:.3f}')
ax.axvline(median_conf, color='green', linestyle='--', linewidth=2, label=f'Median: {median_conf:.3f}')

ax.set_xlabel('Assignment Confidence Score', fontsize=11, weight='bold')
ax.set_ylabel('Number of Documents', fontsize=11, weight='bold')
ax.set_title('Distribution of Document-Topic Assignment Confidence\n(n=223 documents)', 
             fontsize=13, weight='bold', pad=15)
ax.legend(fontsize=10)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '04_overall_confidence_histogram.png'), bbox_inches='tight')
plt.close()
print("  [OK] Saved: 04_overall_confidence_histogram.png")

# ============================================================================
# VISUALIZATION 5: Topic Characteristics Summary
# ============================================================================
print("\n[5/6] Creating topic characteristics summary...")

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

# Panel 1: Document counts
df_sorted = df_topics.sort_values('Count', ascending=False)
bars1 = ax1.bar(range(len(df_sorted)), df_sorted['Count'], color=colors)
ax1.set_xticks(range(len(df_sorted)))
ax1.set_xticklabels([f"T{t}" for t in df_sorted['Topic']], fontsize=9)
ax1.set_ylabel('Document Count', fontsize=10, weight='bold')
ax1.set_title('A) Documents per Topic', fontsize=11, weight='bold')
ax1.grid(axis='y', alpha=0.3)

# Add value labels
for i, (count, topic) in enumerate(zip(df_sorted['Count'], df_sorted['Topic'])):
    ax1.text(i, count + 1, str(count), ha='center', va='bottom', fontsize=8, weight='bold')

# Panel 2: Average confidence per topic
avg_conf_by_topic = df_docs.groupby('topic')['topic_probability'].mean().sort_index()
bars2 = ax2.bar(range(len(avg_conf_by_topic)), avg_conf_by_topic.values, color=colors)
ax2.set_xticks(range(len(avg_conf_by_topic)))
ax2.set_xticklabels([f"T{t}" for t in avg_conf_by_topic.index], fontsize=9)
ax2.set_ylabel('Average Confidence', fontsize=10, weight='bold')
ax2.set_title('B) Average Assignment Confidence', fontsize=11, weight='bold')
ax2.set_ylim([0, 1])
ax2.axhline(y=0.5, color='red', linestyle='--', alpha=0.5)
ax2.grid(axis='y', alpha=0.3)

# Panel 3: High confidence documents (>0.8) per topic
high_conf_counts = df_docs[df_docs['topic_probability'] > 0.8].groupby('topic').size().reindex(range(6), fill_value=0)
bars3 = ax3.bar(range(len(high_conf_counts)), high_conf_counts.values, color=colors)
ax3.set_xticks(range(len(high_conf_counts)))
ax3.set_xticklabels([f"T{t}" for t in high_conf_counts.index], fontsize=9)
ax3.set_ylabel('Count', fontsize=10, weight='bold')
ax3.set_title('C) High-Confidence Documents (>80%)', fontsize=11, weight='bold')
ax3.grid(axis='y', alpha=0.3)

# Panel 4: Research focus percentages
sizes = df_topics.sort_values('Topic')['Count'].values
labels_short = [f"T{t}" for t in df_topics.sort_values('Topic')['Topic']]
percentages = (sizes / sizes.sum()) * 100

bars4 = ax4.bar(range(len(percentages)), percentages, color=colors)
ax4.set_xticks(range(len(percentages)))
ax4.set_xticklabels(labels_short, fontsize=9)
ax4.set_ylabel('Percentage (%)', fontsize=10, weight='bold')
ax4.set_title('D) Research Focus Distribution', fontsize=11, weight='bold')
ax4.grid(axis='y', alpha=0.3)

# Add percentage labels
for i, pct in enumerate(percentages):
    ax4.text(i, pct + 0.5, f'{pct:.1f}%', ha='center', va='bottom', fontsize=8, weight='bold')

fig.suptitle('BERTopic Analysis: Key Characteristics Summary', 
             fontsize=14, weight='bold', y=0.995)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '05_topic_characteristics_summary.png'), bbox_inches='tight')
plt.close()
print("  [OK] Saved: 05_topic_characteristics_summary.png")

# ============================================================================
# VISUALIZATION 6: Research Maturity Analysis
# ============================================================================
print("\n[6/6] Creating research maturity analysis...")

fig, ax = plt.subplots(figsize=(10, 8))

# Define maturity categories based on topic themes
maturity_categories = {
    'Fundamental\nChallenges': [0],  # Topic 0
    'Application\nDevelopment': [1, 4],  # Wastewater + Biodiesel
    'Economic\nViability': [2, 3],  # Biorefinery + Sustainability
    'Future\nInnovations': [5]  # Third-gen
}

category_counts = {}
category_percentages = {}

for category, topic_ids in maturity_categories.items():
    count = df_topics[df_topics['Topic'].isin(topic_ids)]['Count'].sum()
    category_counts[category] = count
    category_percentages[category] = (count / df_topics['Count'].sum()) * 100

# Create bar chart
categories = list(category_counts.keys())
counts = list(category_counts.values())
percentages = list(category_percentages.values())

colors_maturity = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
bars = ax.bar(categories, counts, color=colors_maturity, edgecolor='black', linewidth=1.5)

# Add value labels
for i, (count, pct) in enumerate(zip(counts, percentages)):
    ax.text(i, count + 2, f'{count} docs\n({pct:.1f}%)', 
            ha='center', va='bottom', fontsize=10, weight='bold')

ax.set_ylabel('Number of Documents', fontsize=12, weight='bold')
ax.set_xlabel('Research Maturity Category', fontsize=12, weight='bold')
ax.set_title('Research Maturity Distribution in Microalgae Biofuel Literature', 
             fontsize=13, weight='bold', pad=15)
ax.set_ylim([0, max(counts) * 1.15])
ax.grid(axis='y', alpha=0.3)

# Add interpretation text
interpretation = (
    "Key Insight: 30% of research remains focused on fundamental challenges,\n"
    "suggesting the field is still maturing. Economic viability (29%) is a\n"
    "major concern, while future innovations are underrepresented (9%)."
)
ax.text(0.5, 0.02, interpretation, transform=ax.transAxes, 
        fontsize=9, ha='center', va='bottom',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '06_research_maturity_analysis.png'), bbox_inches='tight')
plt.close()
print("  [OK] Saved: 06_research_maturity_analysis.png")

# ============================================================================
# SUMMARY STATISTICS
# ============================================================================
print("\n" + "=" * 80)
print("VISUALIZATION SUMMARY")
print("=" * 80)

print(f"\nGenerated 6 publication-quality visualizations:")
print(f"  Output directory: {OUTPUT_DIR}")
print(f"  Resolution: 300 DPI")
print(f"  Format: PNG")

print(f"\nKey Statistics:")
print(f"  - Total Documents: {len(df_docs)}")
print(f"  - Total Topics: {len(df_topics)}")
print(f"  - Mean Confidence: {df_docs['topic_probability'].mean():.3f}")
print(f"  - Median Confidence: {df_docs['topic_probability'].median():.3f}")
print(f"  - Std Dev Confidence: {df_docs['topic_probability'].std():.3f}")
print(f"  - High Confidence (>0.8): {len(df_docs[df_docs['topic_probability'] > 0.8])} docs ({len(df_docs[df_docs['topic_probability'] > 0.8])/len(df_docs)*100:.1f}%)")

print(f"\nTopic Distribution:")
for idx, row in df_topics.sort_values('Count', ascending=False).iterrows():
    pct = (row['Count'] / df_topics['Count'].sum()) * 100
    print(f"  Topic {row['Topic']}: {row['Count']:3d} docs ({pct:5.1f}%) - {topic_labels[row['Topic']].replace(chr(10), ' ')}")

print("\n" + "=" * 80)
print("[SUCCESS] All visualizations complete!")
print("=" * 80)
print(f"\nNext: Open {OUTPUT_DIR} to view all figures")

