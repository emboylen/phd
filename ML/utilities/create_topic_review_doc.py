"""
Generate a human-readable printable summary of topics for manual categorization
"""
import sys
from pathlib import Path
from gensim.models import LdaModel
from datetime import datetime

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

# Load coherence score if available
try:
    with open('coherence_plot.png.meta.txt', 'r') as f:
        coherence_info = f.read()
except:
    coherence_info = "Not available"

# Get vocabulary size
vocab_size = len(final_model.id2word)

# Create the document
output_file = f"topics_for_manual_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

with open(output_file, 'w', encoding='utf-8') as f:
    # Header
    f.write("=" * 80 + "\n")
    f.write("TOPIC MODEL SUMMARY - FOR MANUAL CATEGORIZATION\n")
    f.write("=" * 80 + "\n\n")
    
    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Number of Topics: {optimal_k}\n")
    f.write(f"Vocabulary Size: {vocab_size}\n")
    f.write(f"Model File: {model_file.name}\n\n")
    
    f.write("=" * 80 + "\n")
    f.write("INSTRUCTIONS FOR MANUAL CATEGORIZATION:\n")
    f.write("=" * 80 + "\n")
    f.write("1. Review each topic's keywords below\n")
    f.write("2. Assign a meaningful category name to each topic\n")
    f.write("3. Note any topics that seem unclear or overlapping\n")
    f.write("4. Suggest keywords to add/remove for refinement\n\n")
    f.write("Format: Write your category after 'CATEGORY:' for each topic\n\n")
    
    # List all topics
    f.write("=" * 80 + "\n")
    f.write("TOPICS AND KEYWORDS\n")
    f.write("=" * 80 + "\n\n")
    
    for topic_id in range(optimal_k):
        # Get top 20 keywords for thorough review
        top_words = final_model.show_topic(topic_id, topn=20)
        
        f.write("-" * 80 + "\n")
        f.write(f"TOPIC {topic_id}\n")
        f.write("-" * 80 + "\n\n")
        
        # Keywords with weights
        f.write("Top Keywords (with relevance scores):\n")
        for i, (word, weight) in enumerate(top_words, 1):
            word_display = word.replace('_', ' ')
            f.write(f"  {i:2d}. {word_display:30s} ({weight:.4f})\n")
        
        f.write("\n")
        f.write("CATEGORY: _________________________________\n")
        f.write("\n")
        f.write("NOTES:\n")
        f.write("  - \n")
        f.write("  - \n")
        f.write("  - \n")
        f.write("\n\n")
    
    # Summary section for overall notes
    f.write("=" * 80 + "\n")
    f.write("OVERALL OBSERVATIONS\n")
    f.write("=" * 80 + "\n\n")
    f.write("Topics that are too broad:\n\n\n")
    f.write("Topics that are too narrow:\n\n\n")
    f.write("Topics that overlap:\n\n\n")
    f.write("Missing topics (gaps in coverage):\n\n\n")
    f.write("Suggested stopwords to add:\n\n\n")
    f.write("Suggested parameter changes:\n\n\n")

print(f"\n[SUCCESS] Document created: {output_file}")
print(f"   Location: {Path(output_file).resolve()}")
print(f"\n[INFO] Open this file to:")
print("   1. Review and categorize each topic")
print("   2. Print it for manual annotation")
print("   3. Use it to refine your model")
print("\n[TIP] You can also open it in Word/Google Docs for easier editing")

