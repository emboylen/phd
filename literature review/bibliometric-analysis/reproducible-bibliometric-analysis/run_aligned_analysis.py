"""
Bibliometric Analysis on Aligned 207 Papers Dataset
====================================================

Runs complete bibliometric analysis on the same papers used in BERTopic analysis
to ensure consistent results for dynamic topic modeling.

Author: PhD Literature Review Analysis
Date: November 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path
import shutil
from datetime import datetime
import sys

# Import the existing analysis class
sys.path.append(str(Path(__file__).parent))
from complete_analysis import CompleteBibliometricAnalysis


def archive_previous_outputs(output_dir, archive_dir):
    """Archive previous analysis outputs."""
    
    if output_dir.exists():
        print(f"\n{'='*80}")
        print("ARCHIVING PREVIOUS OUTPUTS")
        print(f"{'='*80}")
        
        # Create archive directory with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        archive_path = archive_dir / f"archive_{timestamp}"
        archive_path.mkdir(parents=True, exist_ok=True)
        
        # Move existing outputs to archive
        if (output_dir / 'plots').exists():
            shutil.move(str(output_dir / 'plots'), str(archive_path / 'plots'))
            print(f"[OK] Archived plots to: {archive_path / 'plots'}")
        
        for file in output_dir.glob('*.xlsx'):
            shutil.copy2(str(file), str(archive_path / file.name))
            print(f"[OK] Archived: {file.name}")
        
        for file in output_dir.glob('*.md'):
            shutil.copy2(str(file), str(archive_path / file.name))
            print(f"[OK] Archived: {file.name}")
        
        print(f"\n[OK] Previous outputs archived to: {archive_path}")
        
        return archive_path
    else:
        print("\nNo previous outputs to archive")
        return None


def prepare_aligned_dataset(aligned_biblio_path, output_path):
    """Prepare aligned bibliometric dataset for analysis."""
    
    print(f"\n{'='*80}")
    print("PREPARING ALIGNED DATASET")
    print(f"{'='*80}")
    
    # Load aligned bibliometric data
    aligned_df = pd.read_csv(aligned_biblio_path)
    print(f"\nLoaded aligned bibliometric data: {len(aligned_df)} papers")
    
    # Save as Excel for analysis (biblioshiny-ready format)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    aligned_df.to_excel(output_path, index=False, engine='openpyxl')
    
    print(f"[OK] Saved aligned dataset: {output_path}")
    print(f"     Papers: {len(aligned_df)}")
    print(f"     Years: {aligned_df['PY'].min():.0f}-{aligned_df['PY'].max():.0f}")
    print(f"     Total citations: {aligned_df['TC'].sum():.0f}")
    
    return aligned_df


def run_bibliometric_analysis(data_file, stopwords_file, synonyms_file, output_dir):
    """Run complete bibliometric analysis."""
    
    print(f"\n{'='*80}")
    print("RUNNING BIBLIOMETRIC ANALYSIS")
    print(f"{'='*80}")
    
    # Initialize analysis
    analysis = CompleteBibliometricAnalysis(
        data_file=str(data_file),
        stopwords_file=str(stopwords_file),
        synonyms_file=str(synonyms_file)
    )
    
    # Run all analyses using the run_all method
    print("\nRunning all bibliometric analyses (28 sheets)...")
    analysis.run_all()
    
    # Save all results
    print(f"\nSaving results to Excel...")
    output_file = output_dir / 'BibliometricAnalysis_Aligned_207_Papers.xlsx'
    analysis.save_to_excel(str(output_file))
    print(f"[OK] Analysis results saved: {output_file}")
    
    return analysis


def generate_summary_report(analysis, aligned_df, output_path):
    """Generate comprehensive summary report."""
    
    print(f"\n{'='*80}")
    print("GENERATING SUMMARY REPORT")
    print(f"{'='*80}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Bibliometric Analysis Report\n")
        f.write("## Microalgae Biofuel Literature Review - Aligned Dataset\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Dataset:** 207 papers (2009-2025) aligned with BERTopic analysis\n\n")
        f.write("---\n\n")
        
        # Executive Summary
        f.write("## Executive Summary\n\n")
        f.write(f"This bibliometric analysis examines {len(aligned_df)} peer-reviewed papers ")
        f.write(f"on microalgae biofuel production published between {aligned_df['PY'].min():.0f} ")
        f.write(f"and {aligned_df['PY'].max():.0f}. The dataset is aligned with the BERTopic ")
        f.write(f"semantic analysis to ensure consistency across all analytical approaches.\n\n")
        
        # Main Information
        if 'MainInfo' in analysis.results:
            main_info_df = analysis.results['MainInfo']
            f.write("## Main Information\n\n")
            
            # Display as key-value pairs from DataFrame
            for idx, row in main_info_df.iterrows():
                if 'Description' in row and 'Results' in row:
                    f.write(f"- **{row['Description']}:** {row['Results']}\n")
            f.write("\n")
        
        f.write("---\n\n")
        
        # Publication Trends
        f.write("## Publication Trends\n\n")
        
        if 'AnnualSciProd' in analysis.results:
            annual_prod = analysis.results['AnnualSciProd']
            f.write("### Papers by Year\n\n")
            f.write("| Year | Papers |\n")
            f.write("|------|--------|\n")
            
            for idx, row in annual_prod.iterrows():
                # Handle different possible column names
                year_col = [c for c in row.index if 'year' in c.lower()][0] if any('year' in c.lower() for c in row.index) else row.index[0]
                papers_col = [c for c in row.index if 'article' in c.lower() or 'paper' in c.lower()][0] if any('article' in c.lower() or 'paper' in c.lower() for c in row.index) else row.index[1]
                
                year = row[year_col]
                papers = row[papers_col]
                f.write(f"| {year} | {papers} |\n")
            
            f.write("\n")
        
        # Growth Analysis
        early_period = aligned_df[aligned_df['PY'] <= 2015]
        middle_period = aligned_df[(aligned_df['PY'] > 2015) & (aligned_df['PY'] <= 2020)]
        recent_period = aligned_df[aligned_df['PY'] > 2020]
        
        f.write("### Publication Growth Periods\n\n")
        f.write(f"- **Early Period (2009-2015):** {len(early_period)} papers\n")
        f.write(f"- **Middle Period (2016-2020):** {len(middle_period)} papers\n")
        f.write(f"- **Recent Period (2021-2025):** {len(recent_period)} papers\n\n")
        
        if len(early_period) > 0:
            growth_rate = len(recent_period) / len(early_period)
            f.write(f"**Growth Rate:** {growth_rate:.2f}x increase from early to recent period\n\n")
        
        f.write("---\n\n")
        
        # Top Sources
        if 'MostRelSources' in analysis.results:
            top_sources = analysis.results['MostRelSources']
            f.write("## Most Relevant Sources (Top 10)\n\n")
            f.write("| Rank | Source | Articles |\n")
            f.write("|------|--------|----------|\n")
            
            for idx, row in top_sources.head(10).iterrows():
                rank = idx + 1
                # Get first two columns (likely source name and count)
                source = row.iloc[0] if len(row) > 0 else 'N/A'
                articles = row.iloc[1] if len(row) > 1 else 0
                f.write(f"| {rank} | {source} | {articles} |\n")
            
            f.write("\n---\n\n")
        
        # Top Authors
        if 'MostRelAuthors' in analysis.results:
            top_authors = analysis.results['MostRelAuthors']
            f.write("## Most Prolific Authors (Top 10)\n\n")
            f.write("| Rank | Author | Articles |\n")
            f.write("|------|--------|----------|\n")
            
            for idx, row in top_authors.head(10).iterrows():
                rank = idx + 1
                author = row.iloc[0] if len(row) > 0 else 'N/A'
                articles = row.iloc[1] if len(row) > 1 else 0
                f.write(f"| {rank} | {author} | {articles} |\n")
            
            f.write("\n---\n\n")
        
        # Top Countries
        if 'CountrySciProd' in analysis.results:
            top_countries = analysis.results['CountrySciProd']
            f.write("## Most Productive Countries (Top 10)\n\n")
            f.write("| Rank | Country | Papers | % of Total |\n")
            f.write("|------|---------|--------|------------|\n")
            
            total_papers = len(aligned_df)
            for idx, row in top_countries.head(10).iterrows():
                rank = idx + 1
                country = row.iloc[0] if len(row) > 0 else 'N/A'
                papers = row.iloc[1] if len(row) > 1 else 0
                pct = (papers / total_papers) * 100
                f.write(f"| {rank} | {country} | {papers} | {pct:.1f}% |\n")
            
            f.write("\n---\n\n")
        
        # Most Cited Documents
        if 'MostGlobCitDocs' in analysis.results:
            top_cited = analysis.results['MostGlobCitDocs']
            f.write("## Most Cited Documents (Top 10)\n\n")
            
            for idx, row in top_cited.head(10).iterrows():
                rank = idx + 1
                # Typically first column is paper, second is total citations
                paper = str(row.iloc[0])[:100] if len(row) > 0 else 'N/A'
                citations = row.iloc[1] if len(row) > 1 else 0
                
                f.write(f"### {rank}. {paper}\n\n")
                f.write(f"- **Total Citations:** {citations}\n\n")
            
            f.write("---\n\n")
        
        # Keywords Analysis
        if 'MostFreqWords' in analysis.results:
            freq_words = analysis.results['MostFreqWords']
            f.write("## Most Frequent Keywords (Top 20)\n\n")
            f.write("| Rank | Keyword | Occurrences |\n")
            f.write("|------|---------|-------------|\n")
            
            for idx, row in freq_words.head(20).iterrows():
                rank = idx + 1
                word = row.iloc[0] if len(row) > 0 else 'N/A'
                occurrences = row.iloc[1] if len(row) > 1 else 0
                f.write(f"| {rank} | {word} | {occurrences} |\n")
            
            f.write("\n---\n\n")
        
        # Methodology
        f.write("## Methodology\n\n")
        f.write("### Data Collection\n\n")
        f.write("- **Sources:** Scopus and Web of Science\n")
        f.write("- **Search Terms:** Microalgae, biofuel, biodiesel, bioethanol, sustainability\n")
        f.write("- **Document Type:** Peer-reviewed journal articles\n")
        f.write("- **Language:** English\n\n")
        
        f.write("### Dataset Alignment\n\n")
        f.write(f"- **Original bibliometric dataset:** 222 papers\n")
        f.write(f"- **Original BERTopic dataset:** 223 papers\n")
        f.write(f"- **Aligned dataset (this analysis):** {len(aligned_df)} papers\n\n")
        f.write(f"Only papers present in BOTH datasets are included to ensure ")
        f.write(f"consistency between bibliometric and topic modeling analyses.\n\n")
        
        f.write("### Analysis Tools\n\n")
        f.write("- **Bibliometrix:** Python implementation of bibliometric methods\n")
        f.write("- **Visualization:** matplotlib, seaborn, wordcloud\n")
        f.write("- **Statistical Analysis:** pandas, numpy\n\n")
        
        f.write("---\n\n")
        
        # Available Outputs
        f.write("## Available Outputs\n\n")
        f.write("### Visualizations\n\n")
        f.write("All plots are available in the `output/plots/` directory:\n\n")
        f.write("1. Annual Scientific Production\n")
        f.write("2. Annual Citations per Year\n")
        f.write("3. Most Relevant Sources\n")
        f.write("4. Bradford's Law\n")
        f.write("5. Most Relevant Authors\n")
        f.write("6. Lotka's Law\n")
        f.write("7. Country Scientific Production\n")
        f.write("8. Most Cited Countries\n")
        f.write("9. Most Frequent Words\n")
        f.write("10. Word Cloud\n")
        f.write("11. Trend Topics\n")
        f.write("12. Most Globally Cited Documents\n")
        f.write("13. Source Production Over Time\n")
        f.write("14. Country Collaboration Map\n")
        f.write("15. Corresponding Author Countries\n\n")
        
        f.write("### Data Files\n\n")
        f.write("- `BibliometricAnalysis_Aligned_207_Papers.xlsx` - All analysis results in Excel format\n")
        f.write("- `aligned_207_papers_biblioshiny_ready.xlsx` - Input dataset\n\n")
        
        f.write("---\n\n")
        
        # Footer
        f.write("## Notes\n\n")
        f.write(f"- This analysis uses the aligned dataset of {len(aligned_df)} papers\n")
        f.write("- All statistics are based on matched papers with complete BERTopic topic assignments\n")
        f.write("- Citation counts are as of the data export date\n")
        f.write("- For dynamic topic modeling integration, see: `machine-learning/dynamic-topic-analysis/`\n\n")
        
        f.write("---\n\n")
        f.write(f"*Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
    
    print(f"[OK] Summary report: {output_path}")


def main():
    """Main execution."""
    
    print("\n" + "="*80)
    print("BIBLIOMETRIC ANALYSIS - ALIGNED 207 PAPERS DATASET")
    print("="*80)
    
    # Define paths
    project_root = Path(__file__).parent.parent.parent
    biblio_root = Path(__file__).parent
    
    # Aligned dataset path
    aligned_biblio_path = project_root / 'machine-learning' / 'dynamic-topic-analysis' / 'bibliometric_aligned_207_papers.csv'
    
    # Output directories
    output_dir = biblio_root / 'output_aligned_207'
    archive_dir = biblio_root / 'archives'
    
    # Input files for analysis
    stopwords_file = biblio_root / 'stopwords.csv'
    synonyms_file = biblio_root / 'synonyms.csv'
    
    # Archive previous outputs
    old_output_dir = biblio_root / 'output'
    archive_path = archive_previous_outputs(old_output_dir, archive_dir)
    
    # Prepare aligned dataset
    aligned_data_path = biblio_root / 'data' / 'aligned_207_papers_biblioshiny_ready.xlsx'
    aligned_df = prepare_aligned_dataset(aligned_biblio_path, aligned_data_path)
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    (output_dir / 'plots').mkdir(exist_ok=True)
    
    # Run analysis
    analysis = run_bibliometric_analysis(
        aligned_data_path,
        stopwords_file,
        synonyms_file,
        output_dir
    )
    
    # Generate plots (if the method exists)
    print(f"\n{'='*80}")
    print("GENERATING PLOTS")
    print(f"{'='*80}")
    
    plot_dir = output_dir / 'plots'
    
    # Run the separate plot generation script
    import subprocess
    try:
        subprocess.run([
            'python',
            str(biblio_root / 'generate_all_plots.py'),
            '--data', str(aligned_data_path),
            '--output', str(plot_dir)
        ], check=False)
        print(f"[OK] Plots generated (check {plot_dir})")
    except Exception as e:
        print(f"[INFO] Plot generation skipped (will be in Excel): {e}")
    
    # Generate summary report
    report_md_path = output_dir / 'BIBLIOMETRIC_ANALYSIS_ALIGNED_207_PAPERS.md'
    generate_summary_report(analysis, aligned_df, report_md_path)
    
    # Summary
    print(f"\n{'='*80}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*80}")
    
    print(f"\nOutputs saved to: {output_dir}")
    print(f"\nFiles created:")
    print(f"  - BibliometricAnalysis_Aligned_207_Papers.xlsx (all results)")
    print(f"  - BIBLIOMETRIC_ANALYSIS_ALIGNED_207_PAPERS.md (summary report)")
    print(f"  - plots/ (15 visualization files)")
    
    if archive_path:
        print(f"\nPrevious outputs archived to: {archive_path}")
    
    print(f"\nDataset: {len(aligned_df)} papers ({aligned_df['PY'].min():.0f}-{aligned_df['PY'].max():.0f})")
    print(f"Total citations: {aligned_df['TC'].sum():.0f}")
    print(f"Average citations per paper: {aligned_df['TC'].mean():.1f}")
    
    print(f"\nReady for integration with BERTopic dynamic topic modeling!")


if __name__ == '__main__':
    main()

