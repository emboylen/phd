"""
Integrated BERTopic Analysis for Microalgae Biofuel Research
Combines PDF extraction with semantic topic modeling

This script:
1. Extracts text from PDF corpus
2. Applies lightweight preprocessing
3. Runs BERTopic semantic clustering
4. Generates visualizations and exports
"""

import sys
import io
import os
import re
from pathlib import Path
from datetime import datetime

# Fix Unicode encoding on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# PDF and data handling
import fitz  # PyMuPDF
import pandas as pd
import numpy as np
from tqdm import tqdm

# BERTopic components
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer

# Visualization
import matplotlib.pyplot as plt

print("=" * 80)
print("BERTOPIC ANALYSIS - MICROALGAE BIOFUEL SUSTAINABILITY RESEARCH")
print("=" * 80)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Input/Output
PDF_FOLDER = r"D:\Github\phd\ML\included"
OUTPUT_DIR = "bertopic_outputs"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# Embedding Model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# UMAP Parameters
UMAP_N_NEIGHBORS = 15
UMAP_N_COMPONENTS = 5
UMAP_METRIC = 'cosine'
UMAP_RANDOM_STATE = 42

# HDBSCAN Parameters
HDBSCAN_MIN_CLUSTER_SIZE = 15
HDBSCAN_METRIC = 'euclidean'
HDBSCAN_MIN_SAMPLES = 1

# Vectorizer Parameters
CV_STOP_WORDS = "english"
CV_MIN_DF = 2
CV_NGRAM_RANGE = (1, 2)

# Processing
MIN_TEXT_LENGTH = 100  # Minimum characters for valid document

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==============================================================================
# STAGE 1: PDF TEXT EXTRACTION
# ==============================================================================

def extract_text_from_pdfs(pdf_folder: str) -> pd.DataFrame:
    """
    Extract text from all PDFs in the specified folder.
    
    Args:
        pdf_folder (str): Path to folder containing PDFs
        
    Returns:
        pd.DataFrame: DataFrame with columns ['filename', 'text', 'page_count']
    """
    print("\n" + "=" * 80)
    print("STAGE 1: PDF TEXT EXTRACTION")
    print("=" * 80)
    
    pdf_path = Path(pdf_folder)
    
    # Validate folder
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF folder not found: {pdf_folder}")
    
    pdf_files = list(pdf_path.glob("*.pdf"))
    print(f"\nFound {len(pdf_files)} PDF files")
    
    if len(pdf_files) == 0:
        raise ValueError(f"No PDF files found in {pdf_folder}")
    
    # Extract text from each PDF
    data = []
    failed_files = []
    
    for pdf_file in tqdm(pdf_files, desc="Extracting PDFs", unit="file"):
        try:
            doc = fitz.open(pdf_file)
            full_text = ""
            page_count = doc.page_count
            
            for page_num in range(page_count):
                page = doc.load_page(page_num)
                full_text += page.get_text("text")
            
            doc.close()
            
            # Validate content
            if len(full_text.strip()) >= MIN_TEXT_LENGTH:
                data.append({
                    'filename': pdf_file.name,
                    'text': full_text,
                    'page_count': page_count
                })
            else:
                tqdm.write(f"  [SKIP] {pdf_file.name}: insufficient content")
                failed_files.append(pdf_file.name)
                
        except Exception as e:
            tqdm.write(f"  [ERROR] {pdf_file.name}: {e}")
            failed_files.append(pdf_file.name)
    
    df = pd.DataFrame(data)
    
    print(f"\n✓ Successfully extracted {len(df)} documents")
    if failed_files:
        print(f"  ⚠ {len(failed_files)} files failed or skipped")
    
    # Save raw extractions
    raw_csv = os.path.join(OUTPUT_DIR, f"raw_extractions_{TIMESTAMP}.csv")
    df.to_csv(raw_csv, index=False, encoding='utf-8')
    print(f"  ✓ Raw extractions saved: {raw_csv}")
    
    return df


# ==============================================================================
# STAGE 2: LIGHTWEIGHT PREPROCESSING
# ==============================================================================

def clean_text(text: str) -> str:
    """
    Lightweight cleaning for BERTopic (preserves natural language structure).
    
    Critical: Preserves domain-specific terms like pH, N, P, Fe, TEA, LCA.
    
    Args:
        text (str): Raw text from PDF
        
    Returns:
        str: Cleaned text
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
    
    # Remove special characters but preserve hyphens, periods, chemical symbols
    text = re.sub(r'[^\w\s\-\.°\+\^\-]', ' ', text)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Strip whitespace
    text = text.strip()
    
    return text


def preprocess_documents(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply lightweight preprocessing to all documents.
    
    Args:
        df (pd.DataFrame): DataFrame with 'text' column
        
    Returns:
        pd.DataFrame: DataFrame with added 'cleaned_text' column
    """
    print("\n" + "=" * 80)
    print("STAGE 2: LIGHTWEIGHT PREPROCESSING")
    print("=" * 80)
    
    print(f"\nCleaning {len(df)} documents...")
    
    # Apply cleaning
    df['cleaned_text'] = df['text'].apply(clean_text)
    
    # Filter out documents with insufficient cleaned text
    original_count = len(df)
    df = df[df['cleaned_text'].str.len() >= MIN_TEXT_LENGTH].copy()
    removed_count = original_count - len(df)
    
    if removed_count > 0:
        print(f"  ⚠ Removed {removed_count} documents with insufficient content after cleaning")
    
    print(f"✓ Preprocessing complete: {len(df)} documents ready")
    
    # Calculate statistics
    total_chars = df['cleaned_text'].str.len().sum()
    avg_chars = df['cleaned_text'].str.len().mean()
    
    print(f"  • Total characters: {total_chars:,}")
    print(f"  • Average per document: {avg_chars:,.0f}")
    
    return df


# ==============================================================================
# STAGE 3: BERTOPIC MODEL INITIALIZATION AND TRAINING
# ==============================================================================

def initialize_bertopic() -> BERTopic:
    """
    Initialize BERTopic model with custom sub-models.
    
    Returns:
        BERTopic: Configured but untrained model
    """
    print("\n" + "=" * 80)
    print("STAGE 3: INITIALIZING BERTOPIC MODEL")
    print("=" * 80)
    
    # Step 1: Embedding Model
    print(f"\n[1/4] Loading Sentence Transformer: {EMBEDDING_MODEL}")
    embedding_model = SentenceTransformer(EMBEDDING_MODEL)
    print(f"      ✓ Embedding dimension: {embedding_model.get_sentence_embedding_dimension()}")
    
    # Step 2: UMAP
    print(f"\n[2/4] Configuring UMAP")
    print(f"      • n_neighbors: {UMAP_N_NEIGHBORS}")
    print(f"      • n_components: {UMAP_N_COMPONENTS}")
    print(f"      • metric: {UMAP_METRIC}")
    
    umap_model = UMAP(
        n_neighbors=UMAP_N_NEIGHBORS,
        n_components=UMAP_N_COMPONENTS,
        metric=UMAP_METRIC,
        random_state=UMAP_RANDOM_STATE,
        low_memory=False
    )
    
    # Step 3: HDBSCAN
    print(f"\n[3/4] Configuring HDBSCAN")
    print(f"      • min_cluster_size: {HDBSCAN_MIN_CLUSTER_SIZE}")
    print(f"      • metric: {HDBSCAN_METRIC}")
    
    hdbscan_model = HDBSCAN(
        min_cluster_size=HDBSCAN_MIN_CLUSTER_SIZE,
        metric=HDBSCAN_METRIC,
        prediction_data=True,
        min_samples=HDBSCAN_MIN_SAMPLES
    )
    
    # Step 4: CountVectorizer
    print(f"\n[4/4] Configuring CountVectorizer")
    print(f"      • stop_words: {CV_STOP_WORDS}")
    print(f"      • min_df: {CV_MIN_DF}")
    print(f"      • ngram_range: {CV_NGRAM_RANGE}")
    
    vectorizer_model = CountVectorizer(
        stop_words=CV_STOP_WORDS,
        min_df=CV_MIN_DF,
        ngram_range=CV_NGRAM_RANGE
    )
    
    # Assemble BERTopic
    print(f"\n{'=' * 80}")
    print("Assembling BERTopic pipeline...")
    
    topic_model = BERTopic(
        embedding_model=embedding_model,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        vectorizer_model=vectorizer_model,
        top_n_words=15,
        verbose=True,
        calculate_probabilities=True
    )
    
    print("✓ BERTopic model initialized")
    
    return topic_model


def train_bertopic(topic_model: BERTopic, documents: list) -> tuple:
    """
    Train BERTopic model and reduce outliers.
    
    Args:
        topic_model (BERTopic): Initialized model
        documents (list): List of cleaned documents
        
    Returns:
        tuple: (topics, probabilities)
    """
    print("\n" + "=" * 80)
    print("STAGE 4: TRAINING BERTOPIC MODEL")
    print("=" * 80)
    
    print(f"\nTraining on {len(documents)} documents...")
    print("Note: This will take several minutes (embedding generation + UMAP + clustering)")
    
    # Fit model
    topics, probabilities = topic_model.fit_transform(documents)
    
    initial_topics = len(set(topics)) - (1 if -1 in topics else 0)
    initial_outliers = sum(1 for t in topics if t == -1)
    
    print(f"\n✓ Initial training complete")
    print(f"  • Topics discovered: {initial_topics}")
    print(f"  • Outlier documents: {initial_outliers}")
    
    # Outlier reduction
    if initial_outliers > 0:
        print(f"\n{'=' * 80}")
        print("REDUCING OUTLIERS")
        print("=" * 80)
        
        print("\nApplying embedding-based outlier reduction...")
        
        new_topics = topic_model.reduce_outliers(
            documents,
            topics,
            strategy="embeddings"
        )
        
        # Update model
        topic_model.update_topics(documents, topics=new_topics)
        
        final_outliers = sum(1 for t in new_topics if t == -1)
        outliers_reduced = initial_outliers - final_outliers
        
        print(f"✓ Outlier reduction complete")
        print(f"  • Outliers reassigned: {outliers_reduced}")
        print(f"  • Remaining outliers: {final_outliers}")
        print(f"  • Final topics: {len(set(new_topics)) - (1 if -1 in new_topics else 0)}")
        
        topics = new_topics
    
    return topics, probabilities


# ==============================================================================
# STAGE 4: VISUALIZATION AND EXPORT
# ==============================================================================

def generate_visualizations(topic_model: BERTopic, df: pd.DataFrame):
    """
    Generate and save all visualizations and exports.
    
    Args:
        topic_model (BERTopic): Trained model
        df (pd.DataFrame): DataFrame with topics assigned
    """
    print("\n" + "=" * 80)
    print("STAGE 5: GENERATING VISUALIZATIONS AND EXPORTS")
    print("=" * 80)
    
    # 1. Topic Info DataFrame
    print("\n[1/5] Extracting topic information...")
    topic_info = topic_model.get_topic_info()
    
    topic_info_path = os.path.join(OUTPUT_DIR, f"topic_info_{TIMESTAMP}.csv")
    topic_info.to_csv(topic_info_path, index=False, encoding='utf-8')
    print(f"      ✓ Saved: {topic_info_path}")
    
    # Display summary
    print(f"\n      Topic Summary (Top 10):")
    print(f"      {'─' * 70}")
    for idx, row in topic_info.head(10).iterrows():
        if row['Topic'] != -1:
            topic_name = row['Name'][:55] if 'Name' in row else row['Representation'][:55]
            print(f"      Topic {row['Topic']:2d} ({row['Count']:4d} docs): {topic_name}...")
    
    # 2. Document-Topic Assignments
    print("\n[2/5] Saving document-topic assignments...")
    results_path = os.path.join(OUTPUT_DIR, f"document_topics_{TIMESTAMP}.csv")
    df.to_csv(results_path, index=False, encoding='utf-8')
    print(f"      ✓ Saved: {results_path}")
    
    # 3. Intertopic Distance Map
    print("\n[3/5] Generating intertopic distance map...")
    try:
        fig = topic_model.visualize_topics()
        fig_path = os.path.join(OUTPUT_DIR, f"intertopic_distance_{TIMESTAMP}.html")
        fig.write_html(fig_path)
        print(f"      ✓ Saved: {fig_path}")
    except Exception as e:
        print(f"      ⚠ Failed: {e}")
    
    # 4. Hierarchical Clustering
    print("\n[4/5] Generating hierarchy dendrogram...")
    try:
        fig = topic_model.visualize_hierarchy()
        fig_path = os.path.join(OUTPUT_DIR, f"hierarchy_{TIMESTAMP}.html")
        fig.write_html(fig_path)
        print(f"      ✓ Saved: {fig_path}")
    except Exception as e:
        print(f"      ⚠ Failed: {e}")
    
    # 5. Topic Barchart
    print("\n[5/5] Generating topic barchart...")
    try:
        top_topics = [t for t in topic_info['Topic'].tolist() if t != -1][:10]
        fig = topic_model.visualize_barchart(top_n_topics=min(len(top_topics), 10))
        fig_path = os.path.join(OUTPUT_DIR, f"barchart_{TIMESTAMP}.html")
        fig.write_html(fig_path)
        print(f"      ✓ Saved: {fig_path}")
    except Exception as e:
        print(f"      ⚠ Failed: {e}")
    
    print(f"\n{'=' * 80}")
    print("✓ All visualizations generated")


def save_model(topic_model: BERTopic):
    """Save trained model."""
    print("\n" + "=" * 80)
    print("STAGE 6: SAVING MODEL")
    print("=" * 80)
    
    model_path = os.path.join(OUTPUT_DIR, f"bertopic_model_{TIMESTAMP}")
    
    print(f"\nSaving model to: {model_path}")
    topic_model.save(model_path, serialization="pytorch", save_ctfidf=True)
    print(f"✓ Model saved successfully")


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main():
    """Main execution pipeline."""
    try:
        # Stage 1: Extract PDFs
        df = extract_text_from_pdfs(PDF_FOLDER)
        
        # Stage 2: Preprocess
        df = preprocess_documents(df)
        
        documents = df['cleaned_text'].tolist()
        
        # Stage 3: Initialize and train
        topic_model = initialize_bertopic()
        topics, probabilities = train_bertopic(topic_model, documents)
        
        # Add results to DataFrame
        df['topic'] = topics
        df['topic_probability'] = [prob.max() if len(prob) > 0 else 0 for prob in probabilities]
        
        # Get topic names
        topic_info = topic_model.get_topic_info()
        topic_names = dict(zip(topic_info['Topic'], topic_info['Name'] if 'Name' in topic_info.columns else topic_info['Representation']))
        df['topic_name'] = df['topic'].map(topic_names)
        
        # Stage 4: Visualizations
        generate_visualizations(topic_model, df)
        
        # Stage 5: Save model
        save_model(topic_model)
        
        # Final Summary
        print("\n" + "=" * 80)
        print("✓ BERTOPIC ANALYSIS COMPLETE")
        print("=" * 80)
        
        print(f"\nResults Summary:")
        print(f"  • Documents processed: {len(df)}")
        print(f"  • Topics discovered: {len(set(topics)) - (1 if -1 in topics else 0)}")
        print(f"  • Average confidence: {df['topic_probability'].mean():.3f}")
        print(f"  • Outliers remaining: {sum(1 for t in topics if t == -1)}")
        
        print(f"\nOutput Directory: {os.path.abspath(OUTPUT_DIR)}")
        print(f"\nKey Files:")
        print(f"  • topic_info_{TIMESTAMP}.csv - Topic keywords and counts")
        print(f"  • document_topics_{TIMESTAMP}.csv - Document assignments")
        print(f"  • intertopic_distance_{TIMESTAMP}.html - Interactive map")
        print(f"  • hierarchy_{TIMESTAMP}.html - Topic hierarchy")
        
        print(f"\n{'=' * 80}")
        print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        return df, topic_model
        
    except Exception as e:
        print(f"\n{'=' * 80}")
        print(f"ERROR: {e}")
        print("=" * 80)
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    df_results, model = main()

