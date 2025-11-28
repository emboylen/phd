"""
Match BERTopic Results to Bibliometric Data
============================================

Links BERTopic topic assignments with bibliometric metadata (publication year,
citations, funding, authors, etc.) for dynamic topic modeling analysis.

Author: PhD Literature Review Analysis
Date: November 2025
"""

import pandas as pd
import re
from pathlib import Path
from difflib import SequenceMatcher
import warnings
warnings.filterwarnings('ignore')


def normalize_title(title):
    """
    Normalize title for matching by removing special characters,
    converting to lowercase, and standardizing whitespace.
    
    Args:
        title (str): Original title text
        
    Returns:
        str: Normalized title for matching
    """
    if pd.isna(title):
        return ""
    
    # Convert to string and lowercase
    title = str(title).lower()
    
    # Remove .pdf extension if present
    title = title.replace('.pdf', '')
    
    # Remove special characters and extra whitespace
    title = re.sub(r'[^\w\s]', ' ', title)
    title = re.sub(r'\s+', ' ', title)
    
    return title.strip()


def calculate_similarity(title1, title2):
    """
    Calculate similarity ratio between two titles using SequenceMatcher.
    
    Args:
        title1 (str): First title
        title2 (str): Second title
        
    Returns:
        float: Similarity ratio (0.0 to 1.0)
    """
    return SequenceMatcher(None, title1, title2).ratio()


def match_datasets(bertopic_df, biblio_df, similarity_threshold=0.85):
    """
    Match BERTopic results to bibliometric data using title similarity.
    
    Args:
        bertopic_df (pd.DataFrame): BERTopic document topics
        biblio_df (pd.DataFrame): Bibliometric metadata
        similarity_threshold (float): Minimum similarity for match (0.0-1.0)
        
    Returns:
        tuple: (merged_df, match_stats)
    """
    print("=" * 80)
    print("MATCHING BERTopic DOCUMENTS TO BIBLIOMETRIC RECORDS")
    print("=" * 80)
    
    # Normalize titles in both datasets
    print("\n[1/5] Normalizing titles...")
    bertopic_df['normalized_filename'] = bertopic_df['filename'].apply(normalize_title)
    biblio_df['normalized_title'] = biblio_df['TI'].apply(normalize_title)
    
    # Prepare results storage
    matches = []
    unmatched_bertopic = []
    match_quality = []
    
    print(f"[2/5] Matching {len(bertopic_df)} BERTopic documents to {len(biblio_df)} bibliometric records...")
    print(f"      Similarity threshold: {similarity_threshold}")
    
    # Match each BERTopic document
    for idx, bertopic_row in bertopic_df.iterrows():
        normalized_filename = bertopic_row['normalized_filename']
        
        # Calculate similarity with all bibliometric records
        similarities = biblio_df['normalized_title'].apply(
            lambda x: calculate_similarity(normalized_filename, x)
        )
        
        # Find best match
        best_match_idx = similarities.idxmax()
        best_similarity = similarities.max()
        
        if best_similarity >= similarity_threshold:
            # Good match found
            matches.append({
                'bertopic_index': idx,
                'biblio_index': best_match_idx,
                'similarity': best_similarity,
                'bertopic_filename': bertopic_row['filename'],
                'biblio_title': biblio_df.loc[best_match_idx, 'TI']
            })
            match_quality.append(best_similarity)
        else:
            # No good match
            unmatched_bertopic.append({
                'filename': bertopic_row['filename'],
                'best_similarity': best_similarity,
                'closest_match': biblio_df.loc[best_match_idx, 'TI']
            })
    
    print(f"[3/5] Matching complete!")
    print(f"      Matched: {len(matches)} documents ({len(matches)/len(bertopic_df)*100:.1f}%)")
    print(f"      Unmatched: {len(unmatched_bertopic)} documents ({len(unmatched_bertopic)/len(bertopic_df)*100:.1f}%)")
    print(f"      Average match quality: {sum(match_quality)/len(match_quality):.3f}" if match_quality else "      No matches found")
    
    # Create merged dataset
    print("[4/5] Merging datasets...")
    
    matches_df = pd.DataFrame(matches)
    
    # Merge BERTopic data
    merged = bertopic_df.loc[matches_df['bertopic_index']].reset_index(drop=True)
    
    # Merge bibliometric data
    biblio_matched = biblio_df.loc[matches_df['biblio_index']].reset_index(drop=True)
    
    # Combine
    merged = pd.concat([
        merged.drop(columns=['normalized_filename']),
        biblio_matched.drop(columns=['normalized_title']),
        matches_df[['similarity']]
    ], axis=1)
    
    # Generate match statistics
    match_stats = {
        'total_bertopic_documents': len(bertopic_df),
        'total_biblio_records': len(biblio_df),
        'matched_documents': len(matches),
        'unmatched_documents': len(unmatched_bertopic),
        'match_rate': len(matches) / len(bertopic_df),
        'avg_similarity': sum(match_quality) / len(match_quality) if match_quality else 0,
        'min_similarity': min(match_quality) if match_quality else 0,
        'max_similarity': max(match_quality) if match_quality else 0,
        'unmatched_list': unmatched_bertopic
    }
    
    print(f"[5/5] Merged dataset created: {len(merged)} records with {len(merged.columns)} columns")
    
    return merged, match_stats


def save_results(merged_df, match_stats, output_dir):
    """
    Save merged dataset and matching statistics.
    
    Args:
        merged_df (pd.DataFrame): Merged dataset
        match_stats (dict): Matching statistics
        output_dir (Path): Output directory
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    print("\n" + "=" * 80)
    print("SAVING RESULTS")
    print("=" * 80)
    
    # Save merged dataset
    merged_path = output_dir / 'merged_topic_bibliometric_data.csv'
    merged_df.to_csv(merged_path, index=False)
    print(f"[OK] Merged dataset saved: {merged_path}")
    print(f"  - {len(merged_df)} records")
    print(f"  - {len(merged_df.columns)} columns")
    
    # Save Excel version with key columns only (for easier review)
    key_columns = [
        'filename', 'topic', 'topic_probability', 'topic_name',
        'TI', 'PY', 'TC', 'DI', 'AU', 'SO', 'FU', 'AB',
        'similarity'
    ]
    existing_key_columns = [col for col in key_columns if col in merged_df.columns]
    
    excel_path = output_dir / 'merged_topic_bibliometric_data.xlsx'
    merged_df[existing_key_columns].to_excel(excel_path, index=False)
    print(f"[OK] Excel summary saved: {excel_path}")
    
    # Save match statistics
    stats_path = output_dir / 'matching_statistics.txt'
    with open(stats_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("BERTopic to Bibliometric Matching Statistics\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("OVERALL STATISTICS\n")
        f.write("-" * 80 + "\n")
        f.write(f"Total BERTopic documents:     {match_stats['total_bertopic_documents']}\n")
        f.write(f"Total bibliometric records:   {match_stats['total_biblio_records']}\n")
        f.write(f"Successfully matched:         {match_stats['matched_documents']} ({match_stats['match_rate']*100:.1f}%)\n")
        f.write(f"Unmatched:                    {match_stats['unmatched_documents']} ({(1-match_stats['match_rate'])*100:.1f}%)\n\n")
        
        f.write("MATCH QUALITY\n")
        f.write("-" * 80 + "\n")
        f.write(f"Average similarity:           {match_stats['avg_similarity']:.3f}\n")
        f.write(f"Minimum similarity:           {match_stats['min_similarity']:.3f}\n")
        f.write(f"Maximum similarity:           {match_stats['max_similarity']:.3f}\n\n")
        
        if match_stats['unmatched_list']:
            f.write("UNMATCHED DOCUMENTS\n")
            f.write("-" * 80 + "\n")
            for item in match_stats['unmatched_list']:
                f.write(f"\nFilename: {item['filename']}\n")
                f.write(f"  Best similarity: {item['best_similarity']:.3f}\n")
                f.write(f"  Closest match: {item['closest_match'][:100]}...\n")
    
    print(f"[OK] Match statistics saved: {stats_path}")
    
    # Save unmatched list separately
    if match_stats['unmatched_list']:
        unmatched_df = pd.DataFrame(match_stats['unmatched_list'])
        unmatched_path = output_dir / 'unmatched_documents.csv'
        unmatched_df.to_csv(unmatched_path, index=False)
        print(f"[OK] Unmatched documents saved: {unmatched_path}")
    
    print("\n" + "=" * 80)
    print("DATA SUMMARY")
    print("=" * 80)
    print("\nKey columns in merged dataset:")
    print(f"  - filename:          Source PDF filename")
    print(f"  - topic:             BERTopic topic assignment (0-{merged_df['topic'].max()})")
    print(f"  - topic_name:        Human-readable topic label")
    print(f"  - TI:                Paper title")
    print(f"  - PY:                Publication year ({merged_df['PY'].min()}-{merged_df['PY'].max()})")
    print(f"  - TC:                Total citations (mean: {merged_df['TC'].mean():.1f})")
    print(f"  - FU:                Funding information")
    print(f"  - AU:                Authors")
    print(f"  - DI:                DOI")
    print(f"  - AB:                Abstract")
    
    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print("\n1. Review unmatched documents (if any) and adjust threshold if needed")
    print("2. Run dynamic topic analysis: python analyze_topics_over_time.py")
    print("3. Examine temporal trends by publication year")
    print("4. Analyze citation patterns by topic")
    print("5. Investigate funding distribution across topics")


def main():
    """Main execution function."""
    
    # Define paths
    project_root = Path(__file__).parent.parent
    bertopic_path = project_root / 'machine-learning' / 'bertopic_outputs' / 'document_topics_20251119_130232.csv'
    biblio_path = project_root / 'bibliometric-analysis' / 'reproducible-bibliometric-analysis' / 'data' / 'filtered_data.csv'
    output_dir = project_root / 'machine-learning' / 'dynamic-topic-analysis'
    
    print("\n" + "=" * 80)
    print("BERTopic to Bibliometric Data Matching Pipeline")
    print("=" * 80)
    print(f"\nBERTopic data:      {bertopic_path}")
    print(f"Bibliometric data:  {biblio_path}")
    print(f"Output directory:   {output_dir}")
    
    # Load datasets
    print("\n" + "=" * 80)
    print("LOADING DATA")
    print("=" * 80)
    
    print("\nLoading BERTopic results...")
    bertopic_df = pd.read_csv(bertopic_path)
    print(f"[OK] Loaded {len(bertopic_df)} BERTopic documents")
    print(f"  Topics: {bertopic_df['topic'].nunique()} unique topics")
    
    print("\nLoading bibliometric data...")
    biblio_df = pd.read_csv(biblio_path)
    print(f"[OK] Loaded {len(biblio_df)} bibliometric records")
    print(f"  Years: {biblio_df['PY'].min()}-{biblio_df['PY'].max()}")
    print(f"  Total citations: {biblio_df['TC'].sum()}")
    
    # Match datasets
    merged_df, match_stats = match_datasets(
        bertopic_df, 
        biblio_df, 
        similarity_threshold=0.85
    )
    
    # Save results
    save_results(merged_df, match_stats, output_dir)
    
    print("\n" + "=" * 80)
    print("[COMPLETE] MATCHING FINISHED SUCCESSFULLY")
    print("=" * 80)


if __name__ == '__main__':
    main()

