"""
Generate a comprehensive, print-friendly topic model summary for review
"""
import sys
from pathlib import Path
from gensim.models import LdaModel
from datetime import datetime
import re

# Load the final model
CHECKPOINT_DIR = "model_checkpoints"

# Try to load k=8 model specifically
optimal_k = 8
model_file = Path(CHECKPOINT_DIR) / f"lda_model_k{optimal_k}.pkl"

if not model_file.exists():
    print(f"ERROR: Model file not found: {model_file}")
    print("Looking for alternative models...")
    checkpoint_files = list(Path(CHECKPOINT_DIR).glob("lda_model_k*.pkl"))
    if checkpoint_files:
        print("Available models:")
        for f in sorted(checkpoint_files):
            print(f"  - {f.name}")
    sys.exit(1)

print(f"Loading model from: {model_file}")
final_model = LdaModel.load(str(model_file))
vocab_size = len(final_model.id2word)
print(f"Model has {optimal_k} topics with vocabulary of {vocab_size:,} terms")

# Try to extract document counts from HTML
doc_counts = {}
doc_assignments = {}
try:
    with open('refined_topics_summary.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
        
        # Extract document counts and names
        for topic_id in range(optimal_k):
            # Find the section for this topic
            topic_pattern = f'Topic {topic_id}</td>'
            if topic_pattern in html_content:
                # Look for doc count (in the third column)
                topic_pos = html_content.find(topic_pattern)
                doc_count_pattern = r'doc-count">(\d+)</td>'
                match = re.search(doc_count_pattern, html_content[topic_pos:topic_pos+500])
                if match:
                    doc_counts[topic_id] = int(match.group(1))
                
                # Extract top document names
                doc_names_pattern = r'class="doc-name">([^<]+)</span>'
                doc_matches = re.findall(doc_names_pattern, html_content[topic_pos:topic_pos+2000])
                doc_assignments[topic_id] = doc_matches[:5]  # Top 5 docs
    
    print(f"Loaded document assignments for {len(doc_counts)} topics")
except Exception as e:
    print(f"Could not load document assignments: {e}")

# Create the comprehensive summary
output_file = f"topic_model_print_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

with open(output_file, 'w', encoding='utf-8') as f:
    # Title Page
    f.write("\n\n")
    f.write(" " * 20 + "=" * 40 + "\n")
    f.write(" " * 20 + "TOPIC MODEL ANALYSIS SUMMARY\n")
    f.write(" " * 20 + "For Manual Review and Categorization\n")
    f.write(" " * 20 + "=" * 40 + "\n\n")
    
    f.write(" " * 25 + f"Generated: {datetime.now().strftime('%B %d, %Y')}\n")
    f.write(" " * 25 + f"Model: {model_file.name}\n")
    f.write(" " * 25 + f"Topics: {optimal_k}\n")
    f.write(" " * 25 + f"Vocabulary: {vocab_size:,} terms\n\n")
    
    f.write("\n" + "=" * 80 + "\n")
    f.write("TABLE OF CONTENTS\n")
    f.write("=" * 80 + "\n\n")
    
    # Build table of contents with top 3 words per topic
    f.write("Topic  Top Keywords                              Doc Count  Page\n")
    f.write("-" * 80 + "\n")
    for topic_id in range(optimal_k):
        top_3 = [word for word, _ in final_model.show_topic(topic_id, topn=3)]
        keywords_str = ", ".join(top_3)[:40]
        doc_count = doc_counts.get(topic_id, '?')
        page_num = topic_id + 1
        f.write(f"  {topic_id:2d}   {keywords_str:40s}    {str(doc_count):>4s}      {page_num:2d}\n")
    
    f.write("\n\n")
    
    # Detailed topic pages
    for topic_id in range(optimal_k):
        # Page break
        f.write("\n" + "=" * 80 + "\n")
        f.write("=" * 80 + "\n")
        f.write(f"TOPIC {topic_id}\n")
        f.write("=" * 80 + "\n")
        f.write("=" * 80 + "\n\n")
        
        # Document count
        if topic_id in doc_counts:
            f.write(f"Documents assigned to this topic: {doc_counts[topic_id]}\n")
            percentage = (doc_counts[topic_id] / sum(doc_counts.values()) * 100) if doc_counts else 0
            f.write(f"Percentage of corpus: {percentage:.1f}%\n\n")
        
        # Top 20 keywords with scores
        f.write("-" * 80 + "\n")
        f.write("TOP 20 KEYWORDS (with relevance scores)\n")
        f.write("-" * 80 + "\n\n")
        
        top_words = final_model.show_topic(topic_id, topn=20)
        
        # Display in two columns for better use of space
        left_col = top_words[:10]
        right_col = top_words[10:20]
        
        for i in range(10):
            # Left column
            if i < len(left_col):
                word_l, score_l = left_col[i]
                word_display_l = word_l.replace('_', ' ')
                left_str = f"{i+1:2d}. {word_display_l:20s} ({score_l:.4f})"
            else:
                left_str = " " * 38
            
            # Right column
            if i < len(right_col):
                word_r, score_r = right_col[i]
                word_display_r = word_r.replace('_', ' ')
                right_str = f"{i+11:2d}. {word_display_r:20s} ({score_r:.4f})"
            else:
                right_str = ""
            
            f.write(f"{left_str}  |  {right_str}\n")
        
        f.write("\n")
        
        # Representative documents
        if topic_id in doc_assignments and doc_assignments[topic_id]:
            f.write("-" * 80 + "\n")
            f.write("REPRESENTATIVE DOCUMENTS (Top 5)\n")
            f.write("-" * 80 + "\n\n")
            for i, doc_name in enumerate(doc_assignments[topic_id], 1):
                f.write(f"  {i}. {doc_name}\n")
            f.write("\n")
        
        # Manual categorization section
        f.write("-" * 80 + "\n")
        f.write("MANUAL CATEGORIZATION\n")
        f.write("-" * 80 + "\n\n")
        
        f.write("Category/Label: ________________________________________________\n\n")
        
        f.write("Alternative labels:\n")
        f.write("  1. ___________________________________________________________\n")
        f.write("  2. ___________________________________________________________\n\n")
        
        f.write("Topic Quality:  [ ] Excellent  [ ] Good  [ ] Fair  [ ] Poor\n\n")
        
        f.write("Coherence:      [ ] Very Clear  [ ] Clear  [ ] Unclear  [ ] Confused\n\n")
        
        f.write("Issues identified:\n")
        f.write("  [ ] Too broad (covers multiple distinct concepts)\n")
        f.write("  [ ] Too narrow (very specific, few documents)\n")
        f.write("  [ ] Overlaps with topic(s): _________________________________\n")
        f.write("  [ ] Contains noise words\n")
        f.write("  [ ] Missing key terms\n")
        f.write("  [ ] Other: __________________________________________________\n\n")
        
        f.write("Notes / Observations:\n")
        f.write("_____________________________________________________________________\n\n")
        f.write("_____________________________________________________________________\n\n")
        f.write("_____________________________________________________________________\n\n")
        f.write("_____________________________________________________________________\n\n")
        
        # Refinement suggestions
        f.write("-" * 80 + "\n")
        f.write("REFINEMENT SUGGESTIONS\n")
        f.write("-" * 80 + "\n\n")
        
        f.write("Keywords to add: ________________________________________________\n\n")
        f.write("Keywords to remove: _____________________________________________\n\n")
        f.write("Suggested stopwords: ____________________________________________\n\n")
        f.write("Merge with topic: _______________________________________________\n\n")
        f.write("Split into: _____________________________________________________\n\n")
        
        f.write("\n")  # Extra space before next topic
    
    # Summary pages
    f.write("\n" + "=" * 80 + "\n")
    f.write("=" * 80 + "\n")
    f.write("OVERALL ANALYSIS & RECOMMENDATIONS\n")
    f.write("=" * 80 + "\n")
    f.write("=" * 80 + "\n\n")
    
    f.write("TOPIC DISTRIBUTION ASSESSMENT\n")
    f.write("-" * 80 + "\n\n")
    f.write("Overall balance:  [ ] Good  [ ] Some topics too large  [ ] Uneven\n\n")
    f.write("Coverage:         [ ] Complete  [ ] Missing themes  [ ] Gaps identified\n\n")
    
    if doc_counts:
        f.write("Document distribution across topics:\n")
        sorted_topics = sorted(doc_counts.items(), key=lambda x: x[1], reverse=True)
        f.write("\nLargest topics:\n")
        for i, (tid, count) in enumerate(sorted_topics[:5], 1):
            pct = (count / sum(doc_counts.values()) * 100)
            f.write(f"  {i}. Topic {tid:2d}: {count:3d} docs ({pct:.1f}%)\n")
        
        f.write("\nSmallest topics:\n")
        for i, (tid, count) in enumerate(sorted_topics[-5:], 1):
            pct = (count / sum(doc_counts.values()) * 100)
            f.write(f"  {i}. Topic {tid:2d}: {count:3d} docs ({pct:.1f}%)\n")
        f.write("\n")
    
    f.write("_____________________________________________________________________\n\n")
    f.write("_____________________________________________________________________\n\n\n")
    
    f.write("TOPICS TO MERGE (too similar or overlapping)\n")
    f.write("-" * 80 + "\n\n")
    f.write("1. Topic ___ + Topic ___ => Merged category: ____________________\n\n")
    f.write("2. Topic ___ + Topic ___ => Merged category: ____________________\n\n")
    f.write("3. Topic ___ + Topic ___ => Merged category: ____________________\n\n")
    f.write("4. Topic ___ + Topic ___ => Merged category: ____________________\n\n\n")
    
    f.write("TOPICS TO SPLIT (too broad)\n")
    f.write("-" * 80 + "\n\n")
    f.write("1. Topic ___ => Split into: _____________ and _____________\n\n")
    f.write("2. Topic ___ => Split into: _____________ and _____________\n\n")
    f.write("3. Topic ___ => Split into: _____________ and _____________\n\n\n")
    
    f.write("MISSING TOPICS (themes not captured)\n")
    f.write("-" * 80 + "\n\n")
    f.write("1. _______________________________________________________________\n\n")
    f.write("2. _______________________________________________________________\n\n")
    f.write("3. _______________________________________________________________\n\n\n")
    
    f.write("ADDITIONAL STOPWORDS TO ADD\n")
    f.write("-" * 80 + "\n")
    f.write("(Terms that appear frequently but don't help distinguish topics)\n\n")
    f.write("1. _________________________  11. _________________________\n\n")
    f.write("2. _________________________  12. _________________________\n\n")
    f.write("3. _________________________  13. _________________________\n\n")
    f.write("4. _________________________  14. _________________________\n\n")
    f.write("5. _________________________  15. _________________________\n\n")
    f.write("6. _________________________  16. _________________________\n\n")
    f.write("7. _________________________  17. _________________________\n\n")
    f.write("8. _________________________  18. _________________________\n\n")
    f.write("9. _________________________  19. _________________________\n\n")
    f.write("10. ________________________  20. _________________________\n\n\n")
    
    f.write("PARAMETER RECOMMENDATIONS FOR NEXT RUN\n")
    f.write("-" * 80 + "\n\n")
    f.write(f"Current optimal k: {optimal_k}\n\n")
    f.write("Recommended k for next run:\n")
    f.write("  [ ] Increase to: _____ (if topics too broad)\n")
    f.write("  [ ] Decrease to: _____ (if topics too narrow/overlapping)\n")
    f.write("  [ ] Keep at: {}\n\n".format(optimal_k))
    
    f.write("Other parameter adjustments:\n")
    f.write("  MIN_DOC_COUNT (current: 5):     Change to: _____\n")
    f.write("  MAX_DOC_FRACTION (current: 0.85): Change to: _____\n")
    f.write("  BIGRAM_THRESHOLD (current: 50):  Change to: _____\n\n\n")
    
    f.write("FINAL ASSESSMENT\n")
    f.write("-" * 80 + "\n\n")
    f.write("Overall model quality:\n")
    f.write("  [ ] Excellent - Ready for use\n")
    f.write("  [ ] Good - Minor refinements needed\n")
    f.write("  [ ] Fair - Significant refinement needed\n")
    f.write("  [ ] Poor - Major rework required\n\n")
    
    f.write("Recommended next steps:\n")
    f.write("  [ ] Use current model as-is\n")
    f.write("  [ ] Refine and re-run with adjusted parameters\n")
    f.write("  [ ] Significant changes needed (see notes above)\n\n")
    
    f.write("Additional comments:\n")
    f.write("_____________________________________________________________________\n\n")
    f.write("_____________________________________________________________________\n\n")
    f.write("_____________________________________________________________________\n\n")
    f.write("_____________________________________________________________________\n\n")
    
    f.write("\n" + "=" * 80 + "\n")
    f.write("END OF REPORT\n")
    f.write("=" * 80 + "\n")
    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Total pages: ~{optimal_k + 3}\n")

print(f"\n[SUCCESS] Comprehensive print summary created: {output_file}")
print(f"   Location: {Path(output_file).resolve()}")
print(f"\nSummary includes:")
print(f"   - Table of contents with all {optimal_k} topics")
print(f"   - Full page for each topic with:")
print("     * Top 20 keywords (two-column layout)")
print("     * Representative documents")
print("     * Manual categorization forms")
print("     * Quality assessment checkboxes")
print("     * Refinement suggestion areas")
print(f"   - Overall analysis section")
print("   - Merge/split recommendations")
print("   - Parameter adjustment suggestions")
print("\n[READY TO PRINT]")
print(f"   Estimated pages: ~{optimal_k + 3}")
print("   Format: Letter size (8.5x11)")
print("   Recommended: Print double-sided for review")

