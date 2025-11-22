"""
Generate Human-Readable Summary of BERTopic Results
"""

import pandas as pd
import os
from datetime import datetime

# Configuration
TIMESTAMP = "20251119_130232"  # Update this if needed
BERTOPIC_DIR = "bertopic_outputs"
OUTPUT_FILE = f"bertopic_outputs/BERTOPIC_SUMMARY_{TIMESTAMP}.txt"

print("=" * 80)
print("BERTOPIC ANALYSIS SUMMARY GENERATOR")
print("=" * 80)

# Load topic info (first row with column names)
topic_csv = os.path.join(BERTOPIC_DIR, f"topic_info_{TIMESTAMP}.csv")

print(f"\nReading: {topic_csv}")

# Read just the essential info
df_topics = pd.read_csv(topic_csv, usecols=['Topic', 'Count', 'Name', 'Representation'])

# Load document assignments
doc_csv = os.path.join(BERTOPIC_DIR, f"document_topics_{TIMESTAMP}.csv")
df_docs = pd.read_csv(doc_csv, usecols=['filename', 'topic', 'topic_probability'])

# Generate summary
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("BERTOPIC ANALYSIS RESULTS - MICROALGAE BIOFUEL SUSTAINABILITY RESEARCH\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Total Documents Analyzed: {len(df_docs)}\n")
    f.write(f"Topics Discovered: {len(df_topics) - 1}\n\n")  # -1 for outlier topic
    
    f.write("=" * 80 + "\n")
    f.write("TOPIC OVERVIEW\n")
    f.write("=" * 80 + "\n\n")
    
    for idx, row in df_topics.iterrows():
        topic_id = row['Topic']
        
        if topic_id == -1:
            continue  # Skip outliers
        
        f.write(f"\n{'─' * 80}\n")
        f.write(f"TOPIC {topic_id}\n")
        f.write(f"{'─' * 80}\n\n")
        f.write(f"Document Count: {row['Count']}\n")
        f.write(f"Topic Label: {row['Name']}\n\n")
        
        # Parse representation (list of keywords)
        repr_str = row['Representation']
        f.write(f"Top Keywords:\n{repr_str}\n\n")
        
        # Get representative documents
        topic_docs = df_docs[df_docs['topic'] == topic_id].sort_values('topic_probability', ascending=False).head(10)
        
        f.write(f"Representative Documents (Top 10 by confidence):\n")
        f.write(f"{'─' * 80}\n")
        for doc_idx, doc in topic_docs.iterrows():
            f.write(f"\n{doc['filename']}\n")
            f.write(f"  Confidence: {doc['topic_probability']:.3f}\n")
        
        f.write("\n")
    
    f.write("\n" + "=" * 80 + "\n")
    f.write("DOCUMENT-TO-TOPIC ASSIGNMENTS\n")
    f.write("=" * 80 + "\n\n")
    
    # Summary statistics
    avg_conf = df_docs['topic_probability'].mean()
    min_conf = df_docs['topic_probability'].min()
    max_conf = df_docs['topic_probability'].max()
    
    f.write(f"Average Confidence: {avg_conf:.3f}\n")
    f.write(f"Minimum Confidence: {min_conf:.3f}\n")
    f.write(f"Maximum Confidence: {max_conf:.3f}\n\n")
    
    # Topic distribution
    f.write("Documents per Topic:\n")
    f.write("─" * 40 + "\n")
    topic_counts = df_docs['topic'].value_counts().sort_index()
    for topic, count in topic_counts.items():
        if topic != -1:
            f.write(f"  Topic {topic}: {count} documents\n")
    
    f.write("\n" + "=" * 80 + "\n")
    f.write("END OF SUMMARY\n")
    f.write("=" * 80 + "\n")

print(f"[SUCCESS] Summary saved: {OUTPUT_FILE}")
print(f"\nYou can now:")
print(f"  1. Review the summary: notepad {OUTPUT_FILE}")
print(f"  2. Open interactive visualizations in your browser")
print(f"  3. Explore the full data in the CSV files")

