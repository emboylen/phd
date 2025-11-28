"""
Review and Manually Match Unmatched Documents
==============================================

Provides detailed comparison of unmatched documents with their closest matches
to enable manual review and matching decisions.

Author: PhD Literature Review Analysis
Date: November 2025
"""

import pandas as pd
from pathlib import Path
import re


def normalize_for_comparison(text):
    """Normalize text for easier visual comparison."""
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = text.replace('.pdf', '')
    # Keep more structure for comparison
    text = re.sub(r'[^\w\s-]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def safe_print(text):
    """Print text with safe encoding for Windows console."""
    try:
        print(text)
    except UnicodeEncodeError:
        # Replace problematic characters
        safe_text = text.encode('ascii', 'replace').decode('ascii')
        print(safe_text)


def main():
    """Generate detailed review of unmatched documents."""
    
    project_root = Path(__file__).parent.parent
    
    # Load unmatched documents
    unmatched_path = project_root / 'machine-learning' / 'dynamic-topic-analysis' / 'unmatched_documents.csv'
    unmatched_df = pd.read_csv(unmatched_path)
    
    # Load bibliometric data for additional context
    biblio_path = project_root / 'bibliometric-analysis' / 'reproducible-bibliometric-analysis' / 'data' / 'filtered_data.csv'
    biblio_df = pd.read_csv(biblio_path)
    
    # Load BERTopic data
    bertopic_path = project_root / 'machine-learning' / 'bertopic_outputs' / 'document_topics_20251119_130232.csv'
    bertopic_df = pd.read_csv(bertopic_path)
    
    print("=" * 100)
    print("UNMATCHED DOCUMENTS DETAILED REVIEW")
    print("=" * 100)
    print(f"\nTotal unmatched: {len(unmatched_df)}")
    print(f"Similarity range: {unmatched_df['best_similarity'].min():.2f} - {unmatched_df['best_similarity'].max():.2f}")
    
    # Sort by similarity (highest first)
    unmatched_df = unmatched_df.sort_values('best_similarity', ascending=False)
    
    print("\n" + "=" * 100)
    print("DETAILED COMPARISON (sorted by similarity - highest first)")
    print("=" * 100)
    
    # Prepare manual matching suggestions
    manual_matches = []
    
    for idx, row in unmatched_df.iterrows():
        filename = row['filename']
        closest_match = row['closest_match']
        similarity = row['best_similarity']
        
        # Normalize for comparison
        norm_filename = normalize_for_comparison(filename)
        norm_closest = normalize_for_comparison(closest_match)
        
        # Find the bibliometric record
        biblio_match = biblio_df[biblio_df['TI'].str.upper() == closest_match]
        
        # Find BERTopic record
        bertopic_match = bertopic_df[bertopic_df['filename'] == filename]
        
        safe_print(f"\n{'-' * 100}")
        safe_print(f"MATCH #{len(manual_matches)+1} | Similarity: {similarity:.3f}")
        safe_print(f"{'-' * 100}")
        safe_print(f"\nBERTopic Filename:")
        safe_print(f"  {filename}")
        safe_print(f"\nClosest Bibliometric Title:")
        safe_print(f"  {closest_match}")
        
        if not biblio_match.empty:
            year = biblio_match.iloc[0]['PY']
            tc = biblio_match.iloc[0]['TC']
            safe_print(f"\nBibliometric Metadata:")
            safe_print(f"  Year: {year}")
            safe_print(f"  Citations: {tc}")
            if pd.notna(biblio_match.iloc[0]['AB']):
                abstract = str(biblio_match.iloc[0]['AB'])[:200]
                safe_print(f"  Abstract: {abstract}...")
        
        if not bertopic_match.empty:
            topic = bertopic_match.iloc[0]['topic']
            topic_name = bertopic_match.iloc[0]['topic_name']
            safe_print(f"\nBERTopic Assignment:")
            safe_print(f"  Topic: {topic}")
            safe_print(f"  Topic Name: {topic_name}")
        
        # Normalized comparison
        safe_print(f"\nNormalized Comparison:")
        safe_print(f"  Filename:  {norm_filename[:80]}")
        safe_print(f"  Title:     {norm_closest[:80]}")
        
        # Check for key matching elements
        filename_words = set(norm_filename.split())
        title_words = set(norm_closest.split())
        common_words = filename_words.intersection(title_words)
        unique_to_filename = filename_words - title_words
        unique_to_title = title_words - filename_words
        
        safe_print(f"\nWord Analysis:")
        safe_print(f"  Common words ({len(common_words)}): {' '.join(sorted(list(common_words))[:15])}")
        if len(common_words) > 15:
            safe_print(f"    ... and {len(common_words)-15} more")
        
        # Decision suggestion
        if similarity >= 0.65:
            suggestion = "HIGH CONFIDENCE - Likely same paper (title truncation/variation)"
        elif similarity >= 0.50:
            suggestion = "MEDIUM CONFIDENCE - Could be same paper, review abstracts"
        else:
            suggestion = "LOW CONFIDENCE - Likely different papers"
        
        safe_print(f"\nSuggestion: {suggestion}")
        
        manual_matches.append({
            'filename': filename,
            'closest_match': closest_match,
            'similarity': similarity,
            'suggestion': suggestion,
            'year': biblio_match.iloc[0]['PY'] if not biblio_match.empty else None,
            'biblio_index': biblio_match.index[0] if not biblio_match.empty else None
        })
    
    # Create summary table
    print("\n" + "=" * 100)
    print("SUMMARY TABLE")
    print("=" * 100)
    
    summary_df = pd.DataFrame(manual_matches)
    
    print("\nBy Confidence Level:")
    print(f"  HIGH (>= 0.65):   {len(summary_df[summary_df['similarity'] >= 0.65])} matches")
    print(f"  MEDIUM (>= 0.50): {len(summary_df[(summary_df['similarity'] >= 0.50) & (summary_df['similarity'] < 0.65)])} matches")
    print(f"  LOW (< 0.50):     {len(summary_df[summary_df['similarity'] < 0.50])} matches")
    
    # Save detailed review
    output_path = project_root / 'machine-learning' / 'dynamic-topic-analysis' / 'unmatched_detailed_review.csv'
    summary_df.to_csv(output_path, index=False)
    print(f"\nDetailed review saved: {output_path}")
    
    # Save high confidence matches for potential auto-matching
    high_confidence = summary_df[summary_df['similarity'] >= 0.65]
    if not high_confidence.empty:
        high_conf_path = project_root / 'machine-learning' / 'dynamic-topic-analysis' / 'high_confidence_matches.csv'
        high_confidence.to_csv(high_conf_path, index=False)
        print(f"High confidence matches saved: {high_conf_path}")
        print(f"\n  -> {len(high_confidence)} documents could be auto-matched with lower threshold (0.65)")
    
    print("\n" + "=" * 100)
    print("RECOMMENDATIONS")
    print("=" * 100)
    print(f"\n1. Accept HIGH confidence matches (>= 0.65): {len(high_confidence)} documents")
    print(f"   This would bring total matches to: {205 + len(high_confidence)}/223 ({(205 + len(high_confidence))/223*100:.1f}%)")
    print(f"\n2. Review MEDIUM confidence matches manually")
    print(f"\n3. Skip LOW confidence matches (likely different papers)")
    print(f"\nNext: Run enhanced matching script with tiered thresholds")


if __name__ == '__main__':
    main()

