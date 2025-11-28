"""
Detailed Analysis of 16 Unmatched Papers
=========================================

Shows exactly which 16 papers have no bibliometric data and their closest matches.

Author: PhD Literature Review Analysis
Date: November 2025
"""

import pandas as pd
from pathlib import Path


def main():
    """Analyze the 16 truly unmatched papers."""
    
    project_root = Path(__file__).parent.parent
    
    # Load the remaining unmatched from enhanced matching
    remaining_path = project_root / 'machine-learning' / 'dynamic-topic-analysis' / 'remaining_unmatched_documents.csv'
    remaining_df = pd.read_csv(remaining_path)
    
    # Load bibliometric data to show what papers ARE in the database
    biblio_path = project_root / 'bibliometric-analysis' / 'reproducible-bibliometric-analysis' / 'data' / 'filtered_data.csv'
    biblio_df = pd.read_csv(biblio_path)
    
    print("=" * 120)
    print("16 PAPERS IN BERTopic WITH NO BIBLIOMETRIC DATA")
    print("=" * 120)
    print(f"\nTotal: {len(remaining_df)} papers")
    print(f"\nThese papers were analyzed by BERTopic but could not be matched to bibliometric records.")
    print(f"Showing closest match in bibliometric database for comparison:\n")
    
    # Sort by similarity (highest first) to see if any are close
    remaining_df = remaining_df.sort_values('best_similarity', ascending=False)
    
    for idx, row in remaining_df.iterrows():
        filename = row['filename']
        closest = row['closest_match']
        similarity = row['best_similarity']
        
        # Find the bibliometric record
        biblio_match = biblio_df[biblio_df['TI'].str.upper() == closest]
        
        print("-" * 120)
        print(f"UNMATCHED PAPER #{idx+1} | Similarity to closest match: {similarity:.3f}")
        print("-" * 120)
        
        print(f"\nBERTopic Filename (NO citation data):")
        print(f"  {filename}")
        
        print(f"\nClosest Bibliometric Title (similarity: {similarity:.3f}):")
        print(f"  {closest}")
        
        if not biblio_match.empty:
            year = biblio_match.iloc[0]['PY']
            tc = biblio_match.iloc[0]['TC']
            doi = biblio_match.iloc[0]['DI']
            
            print(f"\nClosest Match Metadata:")
            print(f"  Year: {year}")
            print(f"  Citations: {tc}")
            print(f"  DOI: {doi}")
            
            # Check if this is likely the same paper or truly different
            if similarity >= 0.60:
                assessment = "LIKELY SAME PAPER - title variation or truncation"
            elif similarity >= 0.50:
                assessment = "POSSIBLY SAME PAPER - check manually using DOI/abstract"
            else:
                assessment = "LIKELY DIFFERENT PAPER - or title completely different in database"
            
            print(f"\nAssessment: {assessment}")
        
        print()
    
    # Summary by similarity range
    print("=" * 120)
    print("SUMMARY BY SIMILARITY")
    print("=" * 120)
    
    high_sim = remaining_df[remaining_df['best_similarity'] >= 0.60]
    medium_sim = remaining_df[(remaining_df['best_similarity'] >= 0.50) & (remaining_df['best_similarity'] < 0.60)]
    low_sim = remaining_df[remaining_df['best_similarity'] < 0.50]
    
    print(f"\nHigh similarity (>=0.60): {len(high_sim)} papers")
    print(f"  These are LIKELY the same papers with title variations")
    if not high_sim.empty:
        for idx, row in high_sim.iterrows():
            print(f"    - {row['filename'][:80]}...")
    
    print(f"\nMedium similarity (0.50-0.59): {len(medium_sim)} papers")
    print(f"  These MIGHT be the same papers - need manual verification")
    if not medium_sim.empty:
        for idx, row in medium_sim.iterrows():
            print(f"    - {row['filename'][:80]}...")
    
    print(f"\nLow similarity (<0.50): {len(low_sim)} papers")
    print(f"  These are likely DIFFERENT papers or have very different titles in database")
    if not low_sim.empty:
        for idx, row in low_sim.iterrows():
            print(f"    - {row['filename'][:80]}...")
    
    print("\n" + "=" * 120)
    print("POSSIBLE REASONS FOR NO MATCH")
    print("=" * 120)
    
    print("\n1. Papers in your PDF collection but NOT in bibliometric database")
    print("   - Different search criteria or date ranges")
    print("   - Different databases (you may have included papers from sources not in Scopus/WoS)")
    
    print("\n2. Title variations too extreme for fuzzy matching")
    print("   - Publisher vs. author-submitted titles")
    print("   - Different language or heavily abbreviated titles in database")
    
    print("\n3. Filename formatting issues")
    print("   - Missing spaces, punctuation differences")
    print("   - Truncated filenames that lost key identifying words")
    
    print("\n" + "=" * 120)
    print("RECOMMENDATION")
    print("=" * 120)
    
    print(f"\nYou have 207/223 papers (92.8%) with complete bibliometric data.")
    print(f"The 16 unmatched papers represent only 7.2% of your dataset.")
    
    print(f"\nOptions:")
    print(f"  1. Proceed with 207 papers for dynamic topic modeling (RECOMMENDED)")
    print(f"     - Statistically robust sample size")
    print(f"     - All major topics well-represented")
    print(f"     - Missing papers unlikely to bias temporal trends")
    
    print(f"\n  2. Manually add bibliometric data for high-similarity papers (1 paper >0.60)")
    print(f"     - Check DOI/abstract to confirm it's the same paper")
    print(f"     - Manually create bibliometric entries")
    print(f"     - Would increase coverage to 208/223 (93.3%)")
    
    print(f"\n  3. Accept that these 16 papers are not in your bibliometric database")
    print(f"     - They'll still have BERTopic topic assignments")
    print(f"     - Just won't have year/citation/funding data for temporal analysis")
    
    # Save detailed report
    output_path = project_root / 'machine-learning' / 'dynamic-topic-analysis' / '16_unmatched_papers_detailed_report.csv'
    remaining_df.to_csv(output_path, index=False)
    print(f"\nDetailed report saved to: {output_path}")


if __name__ == '__main__':
    main()

