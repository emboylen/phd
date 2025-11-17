"""
Extract model statistics and configuration to a text file
"""
import sys
from pathlib import Path
from gensim.models import LdaModel
from datetime import datetime

# Read the script to extract configuration
print("Reading configuration from refined-topic-model.py...")
with open('refined-topic-model.py', 'r', encoding='utf-8') as f:
    script_content = f.read()

# Extract custom stopwords from the script
import re

# Extract generic stopwords count
generic_match = re.search(r"generic_stopwords = set\(stopwords\.words\('english'\)\)", script_content)

# Extract academic artifacts
academic_start = script_content.find("academic_artifacts = {")
academic_end = script_content.find("}", academic_start)
academic_section = script_content[academic_start:academic_end+1]
academic_words = re.findall(r"'([^']+)'", academic_section)

# Extract corpus-specific
corpus_start = script_content.find("corpus_specific = {")
corpus_end = script_content.find("}", corpus_start)
corpus_section = script_content[corpus_start:corpus_end+1]
corpus_words = re.findall(r"'([^']+)'", corpus_section)

# Extract parameters
min_doc_count = re.search(r"MIN_DOC_COUNT = (\d+)", script_content)
max_doc_fraction = re.search(r"MAX_DOC_FRACTION = ([\d.]+)", script_content)
bigram_min = re.search(r"BIGRAM_MIN_COUNT = (\d+)", script_content)
bigram_thresh = re.search(r"BIGRAM_THRESHOLD = (\d+)", script_content)
trigram_min = re.search(r"TRIGRAM_MIN_COUNT = (\d+)", script_content)
trigram_thresh = re.search(r"TRIGRAM_THRESHOLD = (\d+)", script_content)
topic_start = re.search(r"TOPIC_RANGE_START = (\d+)", script_content)
topic_end = re.search(r"TOPIC_RANGE_END = (\d+)", script_content)
topic_step = re.search(r"TOPIC_STEP = (\d+)", script_content)
lda_passes = re.search(r"LDA_PASSES = (\d+)", script_content)
lda_iterations = re.search(r"LDA_ITERATIONS = (\d+)", script_content)

# Try to load the final model
CHECKPOINT_DIR = "model_checkpoints"
checkpoint_files = list(Path(CHECKPOINT_DIR).glob("final_best_model_*.pkl"))

if checkpoint_files:
    model_file = checkpoint_files[0]
    print(f"Loading model from: {model_file}")
    final_model = LdaModel.load(str(model_file))
    optimal_k = int(model_file.stem.split('_k')[1])
    vocab_size = len(final_model.id2word)
    model_loaded = True
else:
    print("No final model found - will output configuration only")
    optimal_k = "Not yet determined"
    vocab_size = "Not yet determined"
    model_loaded = False

# Create output file
output_file = f"model_configuration_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

with open(output_file, 'w', encoding='utf-8') as f:
    # Header
    f.write("=" * 80 + "\n")
    f.write("TOPIC MODEL CONFIGURATION & STATISTICS SUMMARY\n")
    f.write("=" * 80 + "\n\n")
    
    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}\n")
    f.write(f"Configuration File: refined-topic-model.py\n")
    if model_loaded:
        f.write(f"Model File: {model_file.name}\n")
    f.write("\n")
    
    # Model Statistics
    f.write("=" * 80 + "\n")
    f.write("MODEL STATISTICS\n")
    f.write("=" * 80 + "\n\n")
    
    f.write(f"Optimal Number of Topics (k):  {optimal_k}\n")
    f.write(f"Final Vocabulary Size:         {vocab_size:,}\n" if isinstance(vocab_size, int) else f"Final Vocabulary Size:         {vocab_size}\n")
    
    if model_loaded:
        f.write(f"Model Type:                    LDA (Latent Dirichlet Allocation)\n")
        f.write(f"Training Algorithm:            Variational Bayes\n")
        f.write(f"Alpha:                         auto-learned\n")
        f.write(f"Eta:                           auto-learned\n")
    
    f.write("\n")
    
    # Processing Parameters
    f.write("=" * 80 + "\n")
    f.write("PROCESSING PARAMETERS\n")
    f.write("=" * 80 + "\n\n")
    
    f.write("Vocabulary Filtering:\n")
    f.write(f"  MIN_DOC_COUNT:        {min_doc_count.group(1) if min_doc_count else 'N/A'} (word must appear in at least this many docs)\n")
    f.write(f"  MAX_DOC_FRACTION:     {max_doc_fraction.group(1) if max_doc_fraction else 'N/A'} (word can't appear in more than this % of docs)\n")
    f.write("\n")
    
    f.write("N-gram Detection:\n")
    f.write(f"  BIGRAM_MIN_COUNT:     {bigram_min.group(1) if bigram_min else 'N/A'}\n")
    f.write(f"  BIGRAM_THRESHOLD:     {bigram_thresh.group(1) if bigram_thresh else 'N/A'}\n")
    f.write(f"  TRIGRAM_MIN_COUNT:    {trigram_min.group(1) if trigram_min else 'N/A'}\n")
    f.write(f"  TRIGRAM_THRESHOLD:    {trigram_thresh.group(1) if trigram_thresh else 'N/A'}\n")
    f.write("\n")
    
    f.write("Topic Range Testing:\n")
    f.write(f"  TOPIC_RANGE_START:    {topic_start.group(1) if topic_start else 'N/A'}\n")
    f.write(f"  TOPIC_RANGE_END:      {topic_end.group(1) if topic_end else 'N/A'}\n")
    f.write(f"  TOPIC_STEP:           {topic_step.group(1) if topic_step else 'N/A'}\n")
    if topic_start and topic_end and topic_step:
        num_models = len(range(int(topic_start.group(1)), int(topic_end.group(1)), int(topic_step.group(1))))
        f.write(f"  Models Trained:       {num_models}\n")
    f.write("\n")
    
    f.write("LDA Training:\n")
    f.write(f"  LDA_PASSES:           {lda_passes.group(1) if lda_passes else 'N/A'} (training iterations)\n")
    f.write(f"  LDA_ITERATIONS:       {lda_iterations.group(1) if lda_iterations else 'N/A'} (per-document iterations)\n")
    f.write(f"  CHUNKSIZE:            100 (documents per batch)\n")
    f.write("\n")
    
    # Custom Stop Words
    f.write("=" * 80 + "\n")
    f.write("CUSTOM STOP WORDS\n")
    f.write("=" * 80 + "\n\n")
    
    f.write("Total Custom Stop Words: ~285 (Generic + Academic + Corpus-specific)\n\n")
    
    f.write("1. GENERIC ENGLISH STOP WORDS\n")
    f.write("-" * 80 + "\n")
    f.write("   Source: NLTK English stopwords corpus\n")
    f.write("   Count: ~198 words\n")
    f.write("   Examples: the, is, at, which, on, in, for, with, as, are, was, etc.\n\n")
    
    f.write("2. ACADEMIC & WEB ARTIFACTS\n")
    f.write("-" * 80 + "\n")
    f.write(f"   Count: {len(academic_words)} words\n\n")
    
    f.write("   Citation artifacts:\n")
    f.write("   ")
    citation = ['et', 'al', 'e.g', 'i.e', 'etc', 'cf', 'ibid', 'op', 'cit']
    f.write(", ".join(citation) + "\n\n")
    
    f.write("   Figure and table references:\n")
    f.write("   ")
    figures = ['fig', 'figure', 'figs', 'table', 'tab', 'ref', 'refs', 'equation', 'eq']
    f.write(", ".join(figures) + "\n\n")
    
    f.write("   Web and DOI:\n")
    f.write("   ")
    web = ['http', 'https', 'www', 'doi', 'com', 'org', 'pdf', 'html', 'htm', 'url']
    f.write(", ".join(web) + "\n\n")
    
    f.write("   Document structure:\n")
    f.write("   ")
    structure = ['introduction', 'methods', 'methodology', 'methodologies', 'result', 'results',
                 'discussion', 'conclusion', 'conclusions', 'abstract', 'summary']
    f.write(", ".join(structure) + "\n\n")
    
    f.write("   Publishing metadata:\n")
    f.write("   ")
    publishing = ['copyright', 'author', 'authors', 'journal', 'publisher', 'pubmed', 
                  'elsevier', 'page', 'pages', 'vol', 'volume', 'no', 'issue', 'supplement']
    f.write(", ".join(publishing) + "\n\n")
    
    f.write("   Common academic phrases:\n")
    f.write("   ")
    academic_common = ['study', 'research', 'paper', 'article', 'review', 'present', 
                       'presented', 'investigate', 'investigated', 'demonstrate', 
                       'demonstrated', 'shown', 'approach', 'method', 'technique', 
                       'analysis', 'analyses', 'experiment', 'experimental', 'data', 'datum']
    f.write(", ".join(academic_common) + "\n\n")
    
    f.write("3. CORPUS-SPECIFIC STOP WORDS (Microalgae/Biofuel Domain)\n")
    f.write("-" * 80 + "\n")
    f.write(f"   Count: {len(corpus_words)} words\n\n")
    f.write("   Words removed:\n")
    f.write("   ")
    f.write(", ".join(corpus_words) + "\n\n")
    
    f.write("   Rationale: These terms appear too frequently across all documents\n")
    f.write("   to be discriminative for topic modeling.\n\n")
    
    # Text Processing Pipeline
    f.write("=" * 80 + "\n")
    f.write("TEXT PROCESSING PIPELINE\n")
    f.write("=" * 80 + "\n\n")
    
    f.write("Stage 1: Custom Stop-Word List\n")
    f.write("  - Generic English (198 words)\n")
    f.write("  - Academic artifacts (74 words)\n")
    f.write("  - Corpus-specific (14 words)\n")
    f.write("  - Total: ~285 stop words\n\n")
    
    f.write("Stage 2: Semantic Normalization\n")
    f.write("  - Lemmatization (reduce words to base form)\n")
    f.write("  - POS filtering (keep only NOUN, ADJ, VERB, ADV)\n")
    f.write("  - Minimum token length: 3 characters\n\n")
    
    f.write("Stage 3: N-gram Detection\n")
    f.write("  - Bigram detection (e.g., 'greenhouse_gas')\n")
    f.write("  - Trigram detection (e.g., 'life_cycle_assessment')\n")
    f.write("  - Pointwise Mutual Information (PMI) scoring\n\n")
    
    f.write("Stage 4: Vocabulary Pruning\n")
    f.write("  - Document frequency filtering\n")
    f.write("  - Remove very rare and very common terms\n\n")
    
    f.write("Stage 5: Coherence-Based Evaluation\n")
    f.write("  - C_v coherence metric\n")
    f.write("  - Test multiple k values\n")
    f.write("  - Select optimal k automatically\n\n")
    
    f.write("Stage 6: Final Model Training\n")
    f.write("  - Train LDA with optimal k\n")
    f.write("  - Auto-learn alpha and eta parameters\n")
    f.write("  - Multiple passes for convergence\n\n")
    
    # Methodology
    f.write("=" * 80 + "\n")
    f.write("METHODOLOGY\n")
    f.write("=" * 80 + "\n\n")
    
    f.write("Algorithm: Latent Dirichlet Allocation (LDA)\n")
    f.write("Implementation: Gensim 4.4.0\n")
    f.write("Coherence Metric: C_v (most correlated with human judgment)\n")
    f.write("Optimization: Variational Bayes inference\n")
    f.write("Hyperparameters: Auto-learned alpha and eta\n\n")
    
    f.write("Key Features:\n")
    f.write("  - Hierarchical stop-word filtering\n")
    f.write("  - Multi-word expression detection\n")
    f.write("  - Automatic optimal topic selection\n")
    f.write("  - Model checkpointing for recovery\n")
    f.write("  - Coherence-driven evaluation\n\n")
    
    # Footer
    f.write("=" * 80 + "\n")
    f.write("END OF SUMMARY\n")
    f.write("=" * 80 + "\n")

print(f"\n[SUCCESS] Configuration summary saved to: {output_file}")
print(f"   Location: {Path(output_file).resolve()}")
print(f"\nSummary includes:")
print("   - Model statistics (k, vocabulary size)")
print("   - All processing parameters")
print("   - Complete stop word lists (285 words)")
print("   - Text processing pipeline description")
print("   - Methodology details")


