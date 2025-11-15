"""
A Methodological Framework for Enhancing Topic Model Coherence in Scientific Literature Analysis
Implements a 6-Stage Refinement Pipeline for High-Quality Topic Modeling
"""

# Fix Unicode encoding issues on Windows
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import fitz  # PyMuPDF
from pathlib import Path
import re
from pprint import pprint

# NLP and Topic Modeling
import spacy
from nltk.corpus import stopwords
import nltk
from gensim.models import Phrases
from gensim.models.phrases import Phraser
from gensim.corpora import Dictionary
from gensim.models import LdaModel, CoherenceModel
import matplotlib.pyplot as plt

# Visualization
import networkx as nx
from pyvis.network import Network

# Progress bars
from tqdm import tqdm

# Serialization and file handling
import pickle
import os
import logging
from datetime import datetime

print("=" * 80)
print("REFINED TOPIC MODELING PIPELINE - 6-STAGE FRAMEWORK")
print("=" * 80)

# ==============================================================================
# CONFIGURATION
# ==============================================================================
PDF_FOLDER_PATH = r"D:\Github\phd\ML\included"
OUTPUT_GRAPH_FILENAME = "refined_knowledge_graph.html"
OUTPUT_TABLE_FILENAME = "refined_topics_summary.html"
CHECKPOINT_DIR = "model_checkpoints"
LOG_FILE = f"topic_modeling_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Advanced Parameters
MIN_DOC_COUNT = 5          # min_df: word must appear in at least 5 documents
MAX_DOC_FRACTION = 0.85    # max_df: word can't appear in more than 85% of documents
BIGRAM_MIN_COUNT = 5       # Minimum count for bigram formation
BIGRAM_THRESHOLD = 100     # Threshold for bigram scoring
TOPIC_RANGE_START = 2      # Test topics from k=2
TOPIC_RANGE_END = 21       # Test topics up to k=20
TOPIC_STEP = 1

# LDA Training Parameters (optimized for balance between quality and speed)
LDA_PASSES = 10            # Total training passes
LDA_ITERATIONS = 400       # Iterations per document
LDA_CHUNKSIZE = 100        # Documents per training chunk

# Create checkpoint directory
os.makedirs(CHECKPOINT_DIR, exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
logger.info("=" * 80)
logger.info("REFINED TOPIC MODELING PIPELINE STARTED")
logger.info("=" * 80)

# Download required NLTK data (run once)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    print("Downloading NLTK stopwords...")
    nltk.download('stopwords', quiet=True)

# Load spaCy model (run once: python -m spacy download en_core_web_sm)
print("\nLoading spaCy model...")
try:
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    # Set max_length to prevent memory issues with very long documents
    nlp.max_length = 2000000  # 2 million characters
    print("✓ spaCy model loaded")
    logger.info("spaCy model loaded successfully")
except OSError:
    error_msg = "ERROR: spaCy model not found. Please run: python -m spacy download en_core_web_sm"
    print(error_msg)
    logger.error(error_msg)
    sys.exit(1)

# ==============================================================================
# STAGE 1: FOUNDATIONAL TEXT REFINEMENT - CUSTOM STOP-WORD LIST
# ==============================================================================
print("\n" + "=" * 80)
print("STAGE 1: Building Comprehensive Stop-Word List")
print("=" * 80)

# Layer 1: Generic English stop words
generic_stopwords = set(stopwords.words('english'))

# Layer 2: Academic & Web Artifacts
academic_artifacts = {
    # Citation artifacts
    'et', 'al', 'e.g', 'i.e', 'etc', 'cf', 'ibid', 'op', 'cit',
    # Figure and table references
    'fig', 'figure', 'figs', 'table', 'tab', 'ref', 'refs', 'equation', 'eq',
    # Web and DOI
    'http', 'https', 'www', 'doi', 'com', 'org', 'pdf', 'html', 'htm', 'url',
    # Document structure
    'introduction', 'methods', 'methodology', 'methodologies', 'result', 'results',
    'discussion', 'conclusion', 'conclusions', 'abstract', 'summary',
    # Publishing metadata
    'copyright', 'author', 'authors', 'journal', 'publisher', 'pubmed', 'elsevier',
    'page', 'pages', 'vol', 'volume', 'no', 'issue', 'supplement',
    # Common academic phrases
    'study', 'research', 'paper', 'article', 'review', 'present', 'presented',
    'investigate', 'investigated', 'demonstrate', 'demonstrated', 'shown',
    'approach', 'method', 'technique', 'analysis', 'analyses', 'experiment',
    'experimental', 'data', 'datum'
}

# Layer 3: Corpus-Specific Stop Words (microalgae domain)
corpus_specific = {
    'microalgae', 'microalga', 'algae', 'algal', 'alga',
    'species', 'strain', 'strains', 
    'model', 'system', 'systems',
    'sample', 'samples', 'sampling'
}

# Layer 4: Noise patterns (numbers, single characters)
# These will be handled by regex and POS filtering

# Combine all layers
custom_stop_words = generic_stopwords.union(academic_artifacts).union(corpus_specific)

print(f"✓ Generic stop words: {len(generic_stopwords)}")
print(f"✓ Academic artifacts: {len(academic_artifacts)}")
print(f"✓ Corpus-specific: {len(corpus_specific)}")
print(f"✓ Total custom stop words: {len(custom_stop_words)}")

# ==============================================================================
# STAGE 2: SEMANTIC NORMALIZATION - LEMMATIZATION + POS FILTERING
# ==============================================================================
print("\n" + "=" * 80)
print("STAGE 2: Defining Advanced Text Processing Function")
print("=" * 80)

# Define allowed POS tags (only keep meaningful content words)
ALLOWED_POSTAGS = {'NOUN', 'ADJ', 'VERB', 'ADV'}

def preprocess_text_spacy(doc_text: str, custom_stops: set) -> list:
    """
    Applies lemmatization, POS filtering, and custom stop-word removal.
    
    Args:
        doc_text: Raw text from document
        custom_stops: Set of custom stop words
    
    Returns:
        List of cleaned, lemmatized tokens
    """
    # Remove URLs and DOIs with regex
    doc_text = re.sub(r'http\S+|www\.\S+|doi:\S+', '', doc_text)
    
    # Remove email addresses
    doc_text = re.sub(r'\S+@\S+', '', doc_text)
    
    # Remove standalone numbers and years
    doc_text = re.sub(r'\b\d+\b', '', doc_text)
    
    # Process with spaCy
    doc = nlp(doc_text.lower())
    
    tokens = []
    for token in doc:
        # Check conditions:
        # 1. Token is alphabetic
        # 2. Not a generic spaCy stop word
        # 3. Has an allowed POS tag
        # 4. Length > 2 (avoid 'al', 'et', etc.)
        if (token.is_alpha and
            not token.is_stop and
            token.pos_ in ALLOWED_POSTAGS and
            len(token.lemma_) > 2):
            
            lemma = token.lemma_.lower()
            
            # Final check against comprehensive custom stop list
            if lemma not in custom_stops:
                tokens.append(lemma)
    
    return tokens

print("✓ Text processing function defined")
print(f"✓ Allowed POS tags: {ALLOWED_POSTAGS}")


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
if __name__ == '__main__':
    from multiprocessing import freeze_support
    freeze_support()

    # Rest of execution code goes here - to be added manually
    # TODO: Copy lines 211-end from CRITICAL_FIXES_SUMMARY.md attached file
