"""
Create Aligned Datasets for Dynamic Topic Modeling
===================================================

Ensures BERTopic and Bibliometric datasets contain the EXACT same papers
for consistent dynamic topic modeling analysis.

Author: PhD Literature Review Analysis
Date: November 2025
"""

import pandas as pd
from pathlib import Path
import shutil


def main():
    """Create aligned datasets with only matched papers."""
    
    project_root = Path(__file__).parent.parent
    
    print("=" * 100)
    print("CREATING ALIGNED DATASETS - SAME PAPERS IN BOTH ANALYSES")
    print("=" * 100)
    
    # Load the enhanced merged dataset (this already has only matched papers)
    merged_path = project_root / 'machine-learning' / 'dynamic-topic-analysis' / 'merged_topic_bibliometric_data_enhanced.csv'
    merged_df = pd.read_csv(merged_path)
    
    print(f"\nLoaded enhanced merged dataset: {len(merged_df)} papers")
    print(f"These are the papers that exist in BOTH BERTopic and Bibliometric datasets")
    
    # Get the list of matched filenames
    matched_filenames = set(merged_df['filename'].tolist())
    matched_titles = set(merged_df['TI'].tolist())
    
    # Load original datasets
    bertopic_path = project_root / 'machine-learning' / 'bertopic_outputs' / 'document_topics_20251119_130232.csv'
    biblio_path = project_root / 'bibliometric-analysis' / 'reproducible-bibliometric-analysis' / 'data' / 'filtered_data.csv'
    
    bertopic_df = pd.read_csv(bertopic_path)
    biblio_df = pd.read_csv(biblio_path)
    
    print(f"\nOriginal datasets:")
    print(f"  BERTopic:     {len(bertopic_df)} papers")
    print(f"  Bibliometric: {len(biblio_df)} papers")
    
    # Create filtered BERTopic dataset (only matched papers)
    bertopic_aligned = bertopic_df[bertopic_df['filename'].isin(matched_filenames)].copy()
    bertopic_aligned = bertopic_aligned.sort_values('filename').reset_index(drop=True)
    
    # Create filtered Bibliometric dataset (only matched papers)
    biblio_aligned = biblio_df[biblio_df['TI'].isin(matched_titles)].copy()
    biblio_aligned = biblio_aligned.sort_values('TI').reset_index(drop=True)
    
    print(f"\nAligned datasets (same papers only):")
    print(f"  BERTopic aligned:     {len(bertopic_aligned)} papers")
    print(f"  Bibliometric aligned: {len(biblio_aligned)} papers")
    
    # Verify alignment
    if len(bertopic_aligned) != len(biblio_aligned):
        print("\n[WARNING] Counts don't match - checking for duplicates...")
        
        # Check for duplicates in merged dataset
        filename_counts = merged_df['filename'].value_counts()
        duplicates = filename_counts[filename_counts > 1]
        
        if not duplicates.empty:
            print(f"  Found {len(duplicates)} duplicate filenames in merged dataset")
            print(f"  Removing duplicates...")
            
            # Remove duplicates from merged dataset (keep first occurrence)
            merged_df = merged_df.drop_duplicates(subset='filename', keep='first')
            matched_filenames = set(merged_df['filename'].tolist())
            matched_titles = set(merged_df['TI'].tolist())
            
            # Recreate aligned datasets
            bertopic_aligned = bertopic_df[bertopic_df['filename'].isin(matched_filenames)].copy()
            bertopic_aligned = bertopic_aligned.sort_values('filename').reset_index(drop=True)
            
            biblio_aligned = biblio_df[biblio_df['TI'].isin(matched_titles)].copy()
            biblio_aligned = biblio_aligned.sort_values('TI').reset_index(drop=True)
            
            print(f"\nAfter removing duplicates:")
            print(f"  BERTopic aligned:     {len(bertopic_aligned)} papers")
            print(f"  Bibliometric aligned: {len(biblio_aligned)} papers")
    
    # Save aligned datasets
    output_dir = project_root / 'machine-learning' / 'dynamic-topic-analysis'
    output_dir.mkdir(exist_ok=True)
    
    print("\n" + "=" * 100)
    print("SAVING ALIGNED DATASETS")
    print("=" * 100)
    
    # Save aligned BERTopic dataset
    bertopic_aligned_path = output_dir / 'bertopic_aligned_207_papers.csv'
    bertopic_aligned.to_csv(bertopic_aligned_path, index=False)
    print(f"\n[OK] BERTopic aligned dataset: {bertopic_aligned_path}")
    print(f"     Papers: {len(bertopic_aligned)}")
    print(f"     Columns: {list(bertopic_aligned.columns)}")
    
    # Save aligned Bibliometric dataset
    biblio_aligned_path = output_dir / 'bibliometric_aligned_207_papers.csv'
    biblio_aligned.to_csv(biblio_aligned_path, index=False)
    print(f"\n[OK] Bibliometric aligned dataset: {biblio_aligned_path}")
    print(f"     Papers: {len(biblio_aligned)}")
    print(f"     Key columns: TI, PY, TC, AU, SO, FU, DI")
    
    # Save the cleaned merged dataset (no duplicates)
    merged_cleaned_path = output_dir / 'merged_topic_bibliometric_ALIGNED.csv'
    merged_df.to_csv(merged_cleaned_path, index=False)
    print(f"\n[OK] Merged aligned dataset: {merged_cleaned_path}")
    print(f"     Papers: {len(merged_df)}")
    print(f"     Contains ALL data from both datasets for matched papers")
    
    # Create Excel summary
    key_columns = [
        'filename', 'topic', 'topic_probability', 'topic_name',
        'TI', 'PY', 'TC', 'AU', 'SO', 'FU', 'DI', 'AB',
        'similarity', 'strategy'
    ]
    existing_cols = [col for col in key_columns if col in merged_df.columns]
    
    excel_path = output_dir / 'merged_topic_bibliometric_ALIGNED.xlsx'
    merged_df[existing_cols].to_excel(excel_path, index=False)
    print(f"\n[OK] Excel summary: {excel_path}")
    
    # Generate summary statistics
    print("\n" + "=" * 100)
    print("ALIGNMENT SUMMARY")
    print("=" * 100)
    
    print(f"\nDataset alignment completed successfully!")
    print(f"\nPapers in aligned datasets: {len(merged_df)}")
    print(f"\nYear range: {merged_df['PY'].min():.0f} - {merged_df['PY'].max():.0f}")
    print(f"Topics: {merged_df['topic'].nunique()} unique topics")
    print(f"Total citations: {merged_df['TC'].sum():.0f}")
    print(f"Average citations per paper: {merged_df['TC'].mean():.1f}")
    
    # Topic distribution
    print(f"\nTopic distribution in aligned dataset:")
    topic_dist = merged_df['topic'].value_counts().sort_index()
    for topic, count in topic_dist.items():
        topic_name = merged_df[merged_df['topic'] == topic]['topic_name'].iloc[0]
        print(f"  Topic {topic} ({topic_name}): {count} papers ({count/len(merged_df)*100:.1f}%)")
    
    # Temporal distribution
    print(f"\nPapers by year:")
    year_dist = merged_df['PY'].value_counts().sort_index()
    for year in sorted(year_dist.index)[:5]:  # Show first 5 years
        print(f"  {year:.0f}: {year_dist[year]} papers")
    print(f"  ...")
    for year in sorted(year_dist.index)[-5:]:  # Show last 5 years
        print(f"  {year:.0f}: {year_dist[year]} papers")
    
    # Papers excluded
    print("\n" + "=" * 100)
    print("PAPERS EXCLUDED FROM ALIGNED DATASET")
    print("=" * 100)
    
    excluded_bertopic = len(bertopic_df) - len(bertopic_aligned)
    excluded_biblio = len(biblio_df) - len(biblio_aligned)
    
    print(f"\nExcluded from BERTopic dataset: {excluded_bertopic} papers ({excluded_bertopic/len(bertopic_df)*100:.1f}%)")
    print(f"  Reason: No matching bibliometric record")
    
    print(f"\nExcluded from Bibliometric dataset: {excluded_biblio} papers ({excluded_biblio/len(biblio_df)*100:.1f}%)")
    print(f"  Reason: PDF not analyzed by BERTopic")
    
    # Save excluded papers lists
    excluded_bertopic_df = bertopic_df[~bertopic_df['filename'].isin(matched_filenames)].copy()
    excluded_biblio_df = biblio_df[~biblio_df['TI'].isin(matched_titles)].copy()
    
    if not excluded_bertopic_df.empty:
        excl_bert_path = output_dir / 'EXCLUDED_from_bertopic_16_papers.csv'
        excluded_bertopic_df[['filename', 'topic', 'topic_name']].to_csv(excl_bert_path, index=False)
        print(f"\n  List saved: {excl_bert_path}")
    
    if not excluded_biblio_df.empty:
        excl_biblio_path = output_dir / 'EXCLUDED_from_bibliometric_papers.csv'
        excluded_biblio_df[['TI', 'PY', 'TC', 'AU', 'DI']].to_csv(excl_biblio_path, index=False)
        print(f"  List saved: {excl_biblio_path}")
    
    print("\n" + "=" * 100)
    print("READY FOR DYNAMIC TOPIC MODELING")
    print("=" * 100)
    
    print(f"\n✓ All datasets now contain the SAME {len(merged_df)} papers")
    print(f"\n✓ Use this file for dynamic topic analysis:")
    print(f"  {merged_cleaned_path}")
    
    print(f"\n✓ This dataset includes:")
    print(f"  - BERTopic topic assignments for all {len(merged_df)} papers")
    print(f"  - Bibliometric data (year, citations, funding, authors) for all {len(merged_df)} papers")
    print(f"  - Ready for temporal analysis (2009-2025)")
    
    print(f"\nNext step: Run dynamic topic modeling analysis")
    print(f"  python analyze_dynamic_topics.py")


if __name__ == '__main__':
    main()

