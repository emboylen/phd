"""
BERTopic Pipeline for Microalgae Biofuel Sustainability Research
PhD Research Project - Semantic Topic Modeling with Transformer Embeddings

This script implements a modern BERTopic workflow for analyzing scientific literature
on microalgae biofuel sustainability and policy, replacing the legacy LDA approach.

Author: PhD Candidate
Date: 2025
"""

import re
import pandas as pd
import numpy as np
from typing import List, Optional

# BERTopic and components
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer

# Visualization
import matplotlib.pyplot as plt
import plotly.io as pio

# Set plotly renderer for compatibility
pio.renderers.default = "browser"

print("=" * 80)
print("BERTOPIC SEMANTIC TOPIC MODELING PIPELINE")
print("Microalgae Biofuel Sustainability Research")
print("=" * 80)

# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Embedding Model Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Fast, balanced performance

# UMAP Configuration (Dimensionality Reduction)
UMAP_N_NEIGHBORS = 15      # Balance between local and global structure
UMAP_N_COMPONENTS = 5      # Reduced dimensions before clustering
UMAP_METRIC = 'cosine'     # Appropriate for text embeddings
UMAP_RANDOM_STATE = 42     # Reproducibility

# HDBSCAN Configuration (Clustering)
HDBSCAN_MIN_CLUSTER_SIZE = 15    # Minimum documents per cluster
HDBSCAN_METRIC = 'euclidean'     # Standard for UMAP output
HDBSCAN_PREDICTION_DATA = True   # Enable outlier reduction

# CountVectorizer Configuration (c-TF-IDF)
CV_STOP_WORDS = "english"        # Remove common English stop words
CV_MIN_DF = 2                    # Minimum document frequency
CV_NGRAM_RANGE = (1, 2)          # Unigrams and bigrams

# Output Configuration
OUTPUT_DIR = "bertopic_outputs"
VISUALIZATIONS = {
    'intertopic_distance': 'intertopic_distance_map.html',
    'hierarchy': 'topic_hierarchy.html',
    'barchart': 'topic_barchart.html',
    'topics_over_time': 'topics_over_time.html'  # If temporal data available
}

# ==============================================================================
# 1. PREPROCESSING FUNCTION
# ==============================================================================

def clean_text(text: str) -> str:
    """
    Lightweight text cleaning for BERTopic (preserves natural language structure).
    
    Critical Constraint: Preserves domain-specific chemical symbols and acronyms
    like pH, N, P, Fe, TEA, LCA that are essential for microalgae research.
    
    Args:
        text (str): Raw abstract text
        
    Returns:
        str: Cleaned text with preserved semantic structure
        
    Note:
        Unlike LDA preprocessing, we do NOT apply:
        - Lemmatization (breaks BERT's contextual understanding)
        - Stemming (damages semantic meaning)
        - Aggressive stop-word removal (context is important)
        - Lowercasing (preserves proper nouns and acronyms)
    """
    if not isinstance(text, str):
        return ""
    
    # Remove URLs (http, https, www)
    text = re.sub(r'http\S+|www\.\S+', '', text)
    
    # Remove DOI patterns
    text = re.sub(r'doi:\S+|DOI:\S+', '', text)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove special characters but preserve:
    # - Hyphens in compound words (e.g., "life-cycle")
    # - Periods in abbreviations (e.g., "e.g.", "i.e.")
    # - Chemical formulas (CO2, NO3-, PO4^3-)
    # Strategy: Only remove truly problematic characters
    text = re.sub(r'[^\w\s\-\.°\+\-\^]', ' ', text)
    
    # Normalize whitespace (multiple spaces to single space)
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Critical: Do NOT filter by token length
    # Domain-specific terms like "pH", "N", "P", "Fe", "C", "TEA", "LCA" must be preserved
    
    return text


def preprocess_dataframe(df: pd.DataFrame, text_column: str = 'abstract') -> pd.DataFrame:
    """
    Apply lightweight preprocessing to entire DataFrame.
    
    Args:
        df (pd.DataFrame): Input DataFrame with text column
        text_column (str): Name of column containing text to process
        
    Returns:
        pd.DataFrame: DataFrame with cleaned text column
    """
    print(f"\nPreprocessing {len(df)} documents...")
    
    # Create cleaned text column
    df['cleaned_text'] = df[text_column].apply(clean_text)
    
    # Remove empty documents after cleaning
    original_count = len(df)
    df = df[df['cleaned_text'].str.len() > 50]  # Minimum 50 characters
    removed_count = original_count - len(df)
    
    if removed_count > 0:
        print(f"  ⚠ Removed {removed_count} documents with insufficient content")
    
    print(f"✓ Preprocessing complete: {len(df)} documents ready for embedding")
    
    return df


# ==============================================================================
# 2. BERTOPIC MODEL INITIALIZATION
# ==============================================================================

def initialize_bertopic_model(
    embedding_model: Optional[SentenceTransformer] = None,
    verbose: bool = True
) -> BERTopic:
    """
    Initialize BERTopic with custom sub-models for fine-grained control.
    
    Architecture:
        1. SentenceTransformer: Contextual embeddings (768-dim)
        2. UMAP: Dimensionality reduction (768-dim → 5-dim)
        3. HDBSCAN: Density-based clustering
        4. CountVectorizer: c-TF-IDF representation
    
    Args:
        embedding_model (SentenceTransformer, optional): Pre-loaded embedding model
        verbose (bool): Print configuration details
        
    Returns:
        BERTopic: Initialized (untrained) BERTopic model
    """
    if verbose:
        print("\n" + "=" * 80)
        print("INITIALIZING BERTOPIC MODEL")
        print("=" * 80)
    
    # Step 1: Embedding Model
    if embedding_model is None:
        if verbose:
            print(f"\n[1/4] Loading Sentence Transformer: {EMBEDDING_MODEL}")
        embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        if verbose:
            print(f"      ✓ Embedding dimension: {embedding_model.get_sentence_embedding_dimension()}")
    
    # Step 2: UMAP Dimensionality Reduction
    if verbose:
        print(f"\n[2/4] Initializing UMAP")
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
    
    # Step 3: HDBSCAN Clustering
    if verbose:
        print(f"\n[3/4] Initializing HDBSCAN")
        print(f"      • min_cluster_size: {HDBSCAN_MIN_CLUSTER_SIZE}")
        print(f"      • metric: {HDBSCAN_METRIC}")
        print(f"      • prediction_data: {HDBSCAN_PREDICTION_DATA}")
    
    hdbscan_model = HDBSCAN(
        min_cluster_size=HDBSCAN_MIN_CLUSTER_SIZE,
        metric=HDBSCAN_METRIC,
        prediction_data=HDBSCAN_PREDICTION_DATA,
        min_samples=1  # Allow more flexible cluster formation
    )
    
    # Step 4: CountVectorizer for c-TF-IDF
    if verbose:
        print(f"\n[4/4] Initializing CountVectorizer")
        print(f"      • stop_words: {CV_STOP_WORDS}")
        print(f"      • min_df: {CV_MIN_DF}")
        print(f"      • ngram_range: {CV_NGRAM_RANGE}")
    
    vectorizer_model = CountVectorizer(
        stop_words=CV_STOP_WORDS,
        min_df=CV_MIN_DF,
        ngram_range=CV_NGRAM_RANGE
    )
    
    # Assemble BERTopic Model
    if verbose:
        print(f"\n{'=' * 80}")
        print("Assembling BERTopic Pipeline...")
    
    topic_model = BERTopic(
        embedding_model=embedding_model,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        vectorizer_model=vectorizer_model,
        top_n_words=10,              # Number of keywords per topic
        verbose=verbose,
        calculate_probabilities=True  # Enable probability calculations
    )
    
    if verbose:
        print("✓ BERTopic model initialized successfully")
        print("=" * 80)
    
    return topic_model


# ==============================================================================
# 3. TRAINING AND OUTLIER REDUCTION
# ==============================================================================

def train_bertopic_model(
    topic_model: BERTopic,
    documents: List[str],
    reduce_outliers: bool = True,
    embeddings: Optional[np.ndarray] = None
) -> tuple:
    """
    Train BERTopic model and optionally reduce outliers.
    
    Args:
        topic_model (BERTopic): Initialized BERTopic model
        documents (List[str]): List of cleaned documents
        reduce_outliers (bool): Whether to apply outlier reduction
        embeddings (np.ndarray, optional): Pre-computed embeddings
        
    Returns:
        tuple: (topics, probabilities, embeddings)
    """
    print("\n" + "=" * 80)
    print("TRAINING BERTOPIC MODEL")
    print("=" * 80)
    
    print(f"\nTraining on {len(documents)} documents...")
    print("Note: This may take several minutes depending on corpus size.")
    
    # Fit the model
    topics, probabilities = topic_model.fit_transform(documents, embeddings)
    
    # Get embeddings if not provided
    if embeddings is None:
        embeddings = topic_model._extract_embeddings(documents)
    
    print(f"\n✓ Initial training complete")
    print(f"  • Discovered topics: {len(set(topics)) - 1}")  # Excluding -1 (outliers)
    print(f"  • Outlier documents: {sum(1 for t in topics if t == -1)}")
    
    # Outlier Reduction
    if reduce_outliers and sum(1 for t in topics if t == -1) > 0:
        print(f"\n{'=' * 80}")
        print("REDUCING OUTLIERS")
        print("=" * 80)
        
        print("\nApplying embedding-based outlier reduction...")
        
        # Strategy: Reassign outliers to nearest topic using embeddings
        new_topics = topic_model.reduce_outliers(
            documents,
            topics,
            strategy="embeddings"
        )
        
        # Update model with reduced outliers
        topic_model.update_topics(documents, topics=new_topics)
        
        outliers_after = sum(1 for t in new_topics if t == -1)
        outliers_reduced = sum(1 for t in topics if t == -1) - outliers_after
        
        print(f"✓ Outlier reduction complete")
        print(f"  • Outliers reassigned: {outliers_reduced}")
        print(f"  • Remaining outliers: {outliers_after}")
        print(f"  • Final topics: {len(set(new_topics)) - 1}")
        
        topics = new_topics
    
    print(f"\n{'=' * 80}")
    print("✓ MODEL TRAINING COMPLETE")
    print("=" * 80)
    
    return topics, probabilities, embeddings


# ==============================================================================
# 4. VISUALIZATION & EXPORT
# ==============================================================================

def visualize_and_export(
    topic_model: BERTopic,
    topics: List[int],
    documents: List[str],
    output_dir: str = OUTPUT_DIR
):
    """
    Generate visualizations and export topic information.
    
    Args:
        topic_model (BERTopic): Trained BERTopic model
        topics (List[int]): Topic assignments for each document
        documents (List[str]): Original documents
        output_dir (str): Directory for outputs
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n" + "=" * 80)
    print("GENERATING VISUALIZATIONS AND EXPORTS")
    print("=" * 80)
    
    # 1. Topic Info DataFrame
    print("\n[1/4] Extracting topic information...")
    topic_info = topic_model.get_topic_info()
    
    # Save to CSV
    topic_info_path = os.path.join(output_dir, "topic_info.csv")
    topic_info.to_csv(topic_info_path, index=False)
    print(f"      ✓ Topic info saved: {topic_info_path}")
    
    # Display summary
    print(f"\n      Topic Summary:")
    print(f"      {'─' * 60}")
    for idx, row in topic_info.head(10).iterrows():
        if row['Topic'] != -1:  # Skip outlier topic
            print(f"      Topic {row['Topic']:2d} ({row['Count']:4d} docs): {row['Name'][:50]}...")
    
    # 2. Intertopic Distance Map
    print("\n[2/4] Generating intertopic distance map...")
    try:
        fig_distance = topic_model.visualize_topics()
        distance_path = os.path.join(output_dir, VISUALIZATIONS['intertopic_distance'])
        fig_distance.write_html(distance_path)
        print(f"      ✓ Intertopic distance map saved: {distance_path}")
    except Exception as e:
        print(f"      ⚠ Failed to generate intertopic distance map: {e}")
    
    # 3. Hierarchical Clustering
    print("\n[3/4] Generating hierarchical clustering dendrogram...")
    try:
        fig_hierarchy = topic_model.visualize_hierarchy()
        hierarchy_path = os.path.join(output_dir, VISUALIZATIONS['hierarchy'])
        fig_hierarchy.write_html(hierarchy_path)
        print(f"      ✓ Hierarchy dendrogram saved: {hierarchy_path}")
    except Exception as e:
        print(f"      ⚠ Failed to generate hierarchy: {e}")
    
    # 4. Topic Barchart
    print("\n[4/4] Generating topic barchart...")
    try:
        # Get top 8 topics (excluding outliers)
        top_topics = [t for t in topic_info['Topic'].tolist() if t != -1][:8]
        fig_barchart = topic_model.visualize_barchart(top_n_topics=len(top_topics))
        barchart_path = os.path.join(output_dir, VISUALIZATIONS['barchart'])
        fig_barchart.write_html(barchart_path)
        print(f"      ✓ Topic barchart saved: {barchart_path}")
    except Exception as e:
        print(f"      ⚠ Failed to generate barchart: {e}")
    
    print(f"\n{'=' * 80}")
    print("✓ VISUALIZATION COMPLETE")
    print("=" * 80)
    print(f"\nAll outputs saved to: {os.path.abspath(output_dir)}")


def save_model(topic_model: BERTopic, output_dir: str = OUTPUT_DIR):
    """
    Save trained BERTopic model for future use.
    
    Args:
        topic_model (BERTopic): Trained model
        output_dir (str): Output directory
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    model_path = os.path.join(output_dir, "bertopic_model")
    
    print(f"\nSaving model to: {model_path}")
    topic_model.save(model_path, serialization="pytorch", save_ctfidf=True)
    print(f"✓ Model saved successfully")


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main(df: pd.DataFrame, text_column: str = 'abstract'):
    """
    Main execution pipeline for BERTopic analysis.
    
    Args:
        df (pd.DataFrame): Input DataFrame with text data
        text_column (str): Column name containing text to analyze
    """
    print("\n" + "=" * 80)
    print("STARTING BERTOPIC PIPELINE")
    print("=" * 80)
    print(f"\nInput: {len(df)} documents")
    print(f"Text column: '{text_column}'")
    
    # Step 1: Preprocessing
    df_clean = preprocess_dataframe(df, text_column)
    documents = df_clean['cleaned_text'].tolist()
    
    # Step 2: Initialize Model
    topic_model = initialize_bertopic_model()
    
    # Step 3: Train Model
    topics, probabilities, embeddings = train_bertopic_model(
        topic_model,
        documents,
        reduce_outliers=True
    )
    
    # Add topics back to DataFrame
    df_clean['topic'] = topics
    df_clean['topic_probability'] = [prob.max() if len(prob) > 0 else 0 for prob in probabilities]
    
    # Step 4: Visualizations and Export
    visualize_and_export(topic_model, topics, documents)
    
    # Step 5: Save Model
    save_model(topic_model)
    
    # Final Summary
    print("\n" + "=" * 80)
    print("✓ PIPELINE COMPLETE")
    print("=" * 80)
    print(f"\nResults Summary:")
    print(f"  • Documents processed: {len(df_clean)}")
    print(f"  • Topics discovered: {len(set(topics)) - 1}")
    print(f"  • Average topic probability: {df_clean['topic_probability'].mean():.3f}")
    print(f"\nNext Steps:")
    print(f"  1. Review topic_info.csv for topic keywords")
    print(f"  2. Open intertopic_distance_map.html to explore topic relationships")
    print(f"  3. Examine topic_hierarchy.html for hierarchical structure")
    print(f"  4. Refine HDBSCAN min_cluster_size if needed")
    
    return df_clean, topic_model


# ==============================================================================
# EXAMPLE USAGE
# ==============================================================================

if __name__ == "__main__":
    """
    Example usage with sample data.
    
    To use with your own data:
        df = pd.read_csv("your_abstracts.csv")
        df_results, model = main(df, text_column='abstract')
    """
    
    # Sample data for demonstration
    # Replace this with your actual data loading
    sample_abstracts = [
        "Microalgae cultivation for biofuel production requires optimization of pH levels and nutrient concentrations including N and P.",
        "Life cycle assessment (LCA) of algal biodiesel shows greenhouse gas emissions comparable to fossil fuels.",
        "Techno-economic analysis (TEA) indicates high capital costs for photobioreactor systems in commercial algae production.",
        "Lipid productivity in Chlorella vulgaris can be enhanced through nitrogen starvation and CO2 supplementation.",
        "Policy frameworks for renewable biofuels must consider sustainability metrics and carbon footprint analysis.",
    ]
    
    # Create sample DataFrame
    df = pd.DataFrame({'abstract': sample_abstracts})
    
    print("\n" + "=" * 80)
    print("RUNNING WITH SAMPLE DATA")
    print("Replace this section with your actual data loading code")
    print("=" * 80)
    
    # Uncomment to run with sample data:
    # df_results, model = main(df, text_column='abstract')
    
    print("\n" + "=" * 80)
    print("TO RUN WITH YOUR DATA:")
    print("=" * 80)
    print("""
    # Load your data
    df = pd.read_csv("your_data.csv")  # or pd.read_excel(), etc.
    
    # Run pipeline
    df_results, model = main(df, text_column='abstract')
    
    # Access results
    print(df_results[['abstract', 'topic', 'topic_probability']].head())
    """)

