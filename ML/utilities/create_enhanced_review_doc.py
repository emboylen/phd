"""
Generate an enhanced human-readable summary with document statistics
"""
import sys
import re
from pathlib import Path
from gensim.models import LdaModel
from datetime import datetime
from bs4 import BeautifulSoup

# Load the final model
CHECKPOINT_DIR = "model_checkpoints"
checkpoint_files = list(Path(CHECKPOINT_DIR).glob("final_best_model_*.pkl"))

if not checkpoint_files:
    print("ERROR: No final model found. Please run the main script first.")
    sys.exit(1)

model_file = checkpoint_files[0]
print(f"Loading model from: {model_file}")
final_model = LdaModel.load(str(model_file))

# Extract k from filename
optimal_k = int(model_file.stem.split('_k')[1])
print(f"Model has {optimal_k} topics")

# Try to extract document counts from HTML
doc_counts = {}
try:
    with open('refined_topics_summary.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all rows in the table
        rows = soup.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 3:
                # First cell is topic ID, third cell is document count
                topic_text = cells[0].get_text()
                if 'Topic' in topic_text:
                    topic_num = int(topic_text.replace('Topic', '').strip())
                    doc_count = cells[2].get_text().strip()
                    doc_counts[topic_num] = int(doc_count)
    print(f"✓ Loaded document counts for {len(doc_counts)} topics")
except Exception as e:
    print(f"⚠ Could not load document counts: {e}")

# Get vocabulary size
vocab_size = len(final_model.id2word)

# Create the enhanced document
output_file = f"topics_manual_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

with open(output_file, 'w', encoding='utf-8') as f:
    # Header
    f.write("╔" + "═" * 78 + "╗\n")
    f.write("║" + " " * 15 + "TOPIC MODEL - MANUAL CATEGORIZATION WORKSHEET" + " " * 17 + "║\n")
    f.write("╚" + "═" * 78 + "╝\n\n")
    
    f.write(f"Generated:        {datetime.now().strftime('%Y-%m-%d at %H:%M')}\n")
    f.write(f"Number of Topics: {optimal_k}\n")
    f.write(f"Vocabulary Size:  {vocab_size:,} terms\n")
    f.write(f"Model File:       {model_file.name}\n\n")
    
    # Quick reference
    f.write("┌" + "─" * 78 + "┐\n")
    f.write("│ QUICK TOPIC REFERENCE                                                       │\n")
    f.write("├" + "─" * 78 + "┤\n")
    
    for topic_id in range(optimal_k):
        top_3_words = [word for word, _ in final_model.show_topic(topic_id, topn=3)]
        top_words_str = ", ".join(top_3_words)[:50]
        doc_count_str = f"({doc_counts.get(topic_id, '?')} docs)" if doc_counts else ""
        line = f"│ Topic {topic_id:2d}: {top_words_str:50s} {doc_count_str:14s} │\n"
        f.write(line)
    
    f.write("└" + "─" * 78 + "┘\n\n")
    
    # Detailed topics
    f.write("\n" + "═" * 80 + "\n")
    f.write("DETAILED TOPIC ANALYSIS\n")
    f.write("═" * 80 + "\n\n")
    
    for topic_id in range(optimal_k):
        # Get top 15 keywords for review
        top_words = final_model.show_topic(topic_id, topn=15)
        
        f.write("\n┌" + "─" * 78 + "┐\n")
        f.write(f"│ TOPIC {topic_id:2d}" + " " * 71 + "│\n")
        f.write("├" + "─" * 78 + "┤\n")
        
        if doc_counts and topic_id in doc_counts:
            f.write(f"│ Documents: {doc_counts[topic_id]:3d}" + " " * 66 + "│\n")
            f.write("├" + "─" * 78 + "┤\n")
        
        # Top 5 keywords prominently
        f.write("│ TOP KEYWORDS:                                                               │\n")
        for i, (word, weight) in enumerate(top_words[:5], 1):
            word_display = word.replace('_', ' ')
            line = f"│   {i}. {word_display:40s} [{weight:.3f}]" + " " * (35 - len(word_display) - len(f"{weight:.3f}")) + "│\n"
            f.write(line)
        
        # Additional keywords (6-15)
        f.write("│                                                                              │\n")
        f.write("│ Additional keywords:                                                         │\n")
        additional = ", ".join([word.replace('_', ' ') for word, _ in top_words[5:15]])
        # Wrap text to fit
        while additional:
            if len(additional) <= 74:
                f.write(f"│   {additional:74s}│\n")
                break
            else:
                # Find last comma before 74 chars
                cutoff = additional[:74].rfind(',')
                if cutoff == -1:
                    cutoff = 74
                f.write(f"│   {additional[:cutoff+1]:74s}│\n")
                additional = additional[cutoff+1:].strip()
        
        f.write("├" + "─" * 78 + "┤\n")
        f.write("│ ASSIGNED CATEGORY:                                                          │\n")
        f.write("│                                                                              │\n")
        f.write("│ [ ] ____________________________________________                             │\n")
        f.write("│                                                                              │\n")
        f.write("├" + "─" * 78 + "┤\n")
        f.write("│ QUALITY RATING:  [ ] Excellent  [ ] Good  [ ] Fair  [ ] Poor                │\n")
        f.write("│                                                                              │\n")
        f.write("│ NOTES:                                                                       │\n")
        f.write("│                                                                              │\n")
        f.write("│                                                                              │\n")
        f.write("│                                                                              │\n")
        f.write("└" + "─" * 78 + "┘\n")
    
    # Summary section
    f.write("\n\n" + "═" * 80 + "\n")
    f.write("REFINEMENT RECOMMENDATIONS\n")
    f.write("═" * 80 + "\n\n")
    
    f.write("1. TOPICS TO MERGE (too similar):\n")
    f.write("   Topic ___ + Topic ___ → New category: ________________\n")
    f.write("   Topic ___ + Topic ___ → New category: ________________\n\n")
    
    f.write("2. TOPICS TO SPLIT (too broad):\n")
    f.write("   Topic ___ → Split into: ________________ and ________________\n")
    f.write("   Topic ___ → Split into: ________________ and ________________\n\n")
    
    f.write("3. STOPWORDS TO ADD (appeared in multiple topics):\n")
    f.write("   - ________________\n")
    f.write("   - ________________\n")
    f.write("   - ________________\n\n")
    
    f.write("4. PARAMETER ADJUSTMENTS FOR NEXT RUN:\n")
    f.write("   Number of topics (current: {}):\n".format(optimal_k))
    f.write("   [ ] Increase to: ___\n")
    f.write("   [ ] Decrease to: ___\n")
    f.write("   [ ] Keep as is\n\n")
    
    f.write("   Other parameters to adjust:\n")
    f.write("   - MIN_DOC_COUNT (current: 5): ___\n")
    f.write("   - MAX_DOC_FRACTION (current: 0.85): ___\n\n")
    
    f.write("5. OVERALL ASSESSMENT:\n")
    f.write("   Quality of topic separation:  [ ] Excellent [ ] Good [ ] Fair [ ] Poor\n")
    f.write("   Coverage of domain:           [ ] Complete  [ ] Good [ ] Fair [ ] Poor\n")
    f.write("   Actionability for analysis:   [ ] High      [ ] Medium [ ] Low\n\n")

print(f"\n✅ Enhanced review document created: {output_file}")
print(f"   Location: {Path(output_file).resolve()}")
print(f"\n📋 This document includes:")
print("   ✓ Quick reference of all topics")
print("   ✓ Detailed keywords for each topic")
print("   ✓ Document counts per topic")
print("   ✓ Checkboxes for categorization")
print("   ✓ Quality rating system")
print("   ✓ Refinement recommendations section")
print(f"\n💡 Ready to print and annotate!")

