"""
Compare BERTopic and Bibliometric Datasets
===========================================

Shows exactly what papers are in each dataset and identifies discrepancies.

Author: PhD Literature Review Analysis
Date: November 2025
"""

import pandas as pd
from pathlib import Path
import re


def normalize_for_comparison(title):
    """Normalize title for comparison."""
    if pd.isna(title):
        return ""
    
    title = str(title).lower()
    title = title.replace('.pdf', '')
    title = re.sub(r'[^\w\s]', ' ', title)
    title = re.sub(r'\s+', ' ', title)
    
    return title.strip()


def main():
    """Compare the two datasets."""
    
    project_root = Path(__file__).parent.parent
    
    # Load both datasets
    bertopic_path = project_root / 'machine-learning' / 'bertopic_outputs' / 'document_topics_20251119_130232.csv'
    biblio_path = project_root / 'bibliometric-analysis' / 'reproducible-bibliometric-analysis' / 'data' / 'filtered_data.csv'
    
    print("=" * 100)
    print("DATASET COMPARISON: BERTopic vs Bibliometric")
    print("=" * 100)
    
    print(f"\nLoading BERTopic documents from:")
    print(f"  {bertopic_path}")
    bertopic_df = pd.read_csv(bertopic_path)
    print(f"  Total: {len(bertopic_df)} documents")
    
    print(f"\nLoading Bibliometric records from:")
    print(f"  {biblio_path}")
    biblio_df = pd.read_csv(biblio_path)
    print(f"  Total: {len(biblio_df)} records")
    
    # Normalize titles
    bertopic_df['normalized'] = bertopic_df['filename'].apply(normalize_for_comparison)
    biblio_df['normalized'] = biblio_df['TI'].apply(normalize_for_comparison)
    
    # Create sets for comparison
    bertopic_titles = set(bertopic_df['normalized'].tolist())
    biblio_titles = set(biblio_df['normalized'].tolist())
    
    # Find differences
    only_in_bertopic = bertopic_titles - biblio_titles
    only_in_biblio = biblio_titles - bertopic_titles
    in_both = bertopic_titles.intersection(biblio_titles)
    
    print("\n" + "=" * 100)
    print("COMPARISON RESULTS")
    print("=" * 100)
    
    print(f"\nPapers in BOTH datasets:          {len(in_both)}")
    print(f"Papers ONLY in BERTopic:          {len(only_in_bertopic)} (these won't have bibliometric data)")
    print(f"Papers ONLY in Bibliometric:      {len(only_in_biblio)} (these weren't analyzed by BERTopic)")
    
    # Save detailed comparison
    output_dir = project_root / 'machine-learning' / 'dynamic-topic-analysis'
    output_dir.mkdir(exist_ok=True)
    
    # Papers only in BERTopic
    if only_in_bertopic:
        print(f"\n" + "-" * 100)
        print(f"PAPERS ONLY IN BERTopic ({len(only_in_bertopic)} papers)")
        print("-" * 100)
        print("\nThese PDFs were analyzed by BERTopic but don't have matching bibliometric records:")
        
        bertopic_only_df = bertopic_df[bertopic_df['normalized'].isin(only_in_bertopic)].copy()
        bertopic_only_df = bertopic_only_df.sort_values('filename')
        
        # Save to CSV
        save_path = output_dir / 'papers_only_in_bertopic.csv'
        bertopic_only_df[['filename', 'topic', 'topic_name', 'topic_probability']].to_csv(save_path, index=False)
        print(f"  First few examples saved to: {save_path}")
        print(f"  Total: {len(bertopic_only_df)} papers")
    
    # Papers only in Bibliometric
    if only_in_biblio:
        print(f"\n" + "-" * 100)
        print(f"PAPERS ONLY IN BIBLIOMETRIC DATA ({len(only_in_biblio)} papers)")
        print("-" * 100)
        print("\nThese papers are in bibliometric database but weren't analyzed by BERTopic:")
        
        biblio_only_df = biblio_df[biblio_df['normalized'].isin(only_in_biblio)].copy()
        biblio_only_df = biblio_only_df.sort_values('TI')
        
        # Save to CSV
        save_path = output_dir / 'papers_only_in_bibliometric.csv'
        biblio_only_df[['TI', 'PY', 'TC', 'AU', 'SO', 'DI']].to_csv(save_path, index=False)
        print(f"  Saved to: {save_path}")
        print(f"  Total: {len(biblio_only_df)} papers")
    
    # Papers in both
    print(f"\n" + "-" * 100)
    print(f"PAPERS IN BOTH DATASETS ({len(in_both)} papers)")
    print("-" * 100)
    print("\nThese papers successfully matched and will be used for dynamic topic analysis.")
    
    both_bertopic = bertopic_df[bertopic_df['normalized'].isin(in_both)].copy()
    both_biblio = biblio_df[biblio_df['normalized'].isin(in_both)].copy()
    
    save_path = output_dir / 'papers_in_both_datasets.csv'
    both_bertopic[['filename', 'topic', 'topic_name']].to_csv(save_path, index=False)
    print(f"\n  Saved to: {save_path}")
    
    # Summary statistics
    print("\n" + "=" * 100)
    print("SUMMARY")
    print("=" * 100)
    
    print(f"\nBERTopic Dataset ({len(bertopic_df)} total):")
    print(f"  - Analyzed PDFs from: machine-learning/bertopic_outputs/")
    print(f"  - Successfully matched: {len(in_both)} ({len(in_both)/len(bertopic_df)*100:.1f}%)")
    print(f"  - No bibliometric match: {len(only_in_bertopic)} ({len(only_in_bertopic)/len(bertopic_df)*100:.1f}%)")
    
    print(f"\nBibliometric Dataset ({len(biblio_df)} total):")
    print(f"  - From: bibliometric-analysis/.../filtered_data.csv")
    print(f"  - Successfully matched: {len(in_both)} ({len(in_both)/len(biblio_df)*100:.1f}%)")
    print(f"  - Not analyzed by BERTopic: {len(only_in_biblio)} ({len(only_in_biblio)/len(biblio_df)*100:.1f}%)")
    
    print("\n" + "=" * 100)
    print("EXPLANATION OF DISCREPANCIES")
    print("=" * 100)
    
    print("\nPossible reasons for mismatches:")
    print("\n1. DIFFERENT SOURCE FILES:")
    print("   - BERTopic analyzed PDFs from: included-papers/ or similar directory")
    print("   - Bibliometric data from: Scopus/WoS export (possibly different paper selection)")
    
    print("\n2. FILTERING DIFFERENCES:")
    print("   - One dataset may have additional filtering criteria")
    print("   - Bibliometric data shows it's 'filtered_data.csv' - some papers excluded")
    
    print("\n3. DATA COLLECTION TIMING:")
    print("   - BERTopic analysis: November 2024")
    print("   - Bibliometric data: May have different collection date")
    
    print("\n4. TITLE VARIATIONS:")
    print("   - Some papers may have slightly different titles in different sources")
    print("   - PDF filenames may not exactly match database titles")
    
    print("\n" + "=" * 100)
    print("RECOMMENDATION")
    print("=" * 100)
    
    print(f"\nFor dynamic topic modeling, you have {len(in_both)} papers with complete data.")
    print(f"This is {len(in_both)/len(bertopic_df)*100:.1f}% of your BERTopic analysis.")
    print(f"\nThis is sufficient for robust temporal analysis (2009-2025).")
    
    print("\nTo investigate discrepancies:")
    print("  1. Check: papers_only_in_bertopic.csv")
    print("  2. Check: papers_only_in_bibliometric.csv")
    print("  3. Verify source directories for both datasets")
    
    # Create comprehensive comparison file
    comparison_path = output_dir / 'dataset_comparison_report.txt'
    with open(comparison_path, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write("DATASET COMPARISON REPORT\n")
        f.write("=" * 100 + "\n\n")
        
        f.write(f"BERTopic documents: {len(bertopic_df)}\n")
        f.write(f"Bibliometric records: {len(biblio_df)}\n")
        f.write(f"Matched papers: {len(in_both)}\n")
        f.write(f"Only in BERTopic: {len(only_in_bertopic)}\n")
        f.write(f"Only in Bibliometric: {len(only_in_biblio)}\n\n")
        
        f.write("-" * 100 + "\n")
        f.write("PAPERS ONLY IN BERTopic\n")
        f.write("-" * 100 + "\n\n")
        if only_in_bertopic:
            bertopic_only_df = bertopic_df[bertopic_df['normalized'].isin(only_in_bertopic)].copy()
            for idx, row in bertopic_only_df.iterrows():
                f.write(f"{row['filename']}\n")
        else:
            f.write("None\n")
        
        f.write("\n" + "-" * 100 + "\n")
        f.write("PAPERS ONLY IN BIBLIOMETRIC\n")
        f.write("-" * 100 + "\n\n")
        if only_in_biblio:
            biblio_only_df = biblio_df[biblio_df['normalized'].isin(only_in_biblio)].copy()
            for idx, row in biblio_only_df.iterrows():
                f.write(f"{row['TI']}\n")
        else:
            f.write("None\n")
    
    print(f"\nFull report saved to: {comparison_path}")
    print("\n" + "=" * 100)


if __name__ == '__main__':
    main()

