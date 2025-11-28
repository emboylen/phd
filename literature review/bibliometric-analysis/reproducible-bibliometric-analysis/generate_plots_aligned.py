"""
Generate Plots for Aligned 207 Papers Bibliometric Analysis
============================================================

Creates all visualization plots for the bibliometric analysis.

Author: PhD Literature Review Analysis
Date: November 2025
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from wordcloud import WordCloud
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

def generate_all_plots(data_file, output_dir):
    """Generate all plots from bibliometric analysis results."""
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*80)
    print("GENERATING BIBLIOMETRIC PLOTS")
    print("="*80)
    
    # Load Excel file
    xl = pd.ExcelFile(data_file)
    print(f"\nLoaded data from: {data_file}")
    print(f"Sheets available: {len(xl.sheet_names)}")
    
    # 1. Annual Scientific Production
    try:
        print("\n[1/15] Annual Scientific Production...")
        df_annual = pd.read_excel(xl, sheet_name='AnnualSciProd')
        
        plt.figure(figsize=(12, 6))
        plt.bar(df_annual.iloc[:, 0], df_annual.iloc[:, 1], color='steelblue', alpha=0.8)
        plt.plot(df_annual.iloc[:, 0], df_annual.iloc[:, 1], 'o-', color='darkblue', linewidth=2, markersize=6)
        plt.xlabel('Year', fontsize=12, fontweight='bold')
        plt.ylabel('Number of Articles', fontsize=12, fontweight='bold')
        plt.title('Annual Scientific Production (2009-2025)', fontsize=14, fontweight='bold')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_dir / '01_Annual_Scientific_Production.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("    [OK] Saved")
    except Exception as e:
        print(f"    [SKIP] {e}")
    
    # 2. Annual Citations per Year
    try:
        print("[2/15] Annual Citations per Year...")
        df_cit = pd.read_excel(xl, sheet_name='AnnualCitPerYear')
        
        fig, ax1 = plt.subplots(figsize=(12, 6))
        
        # Use iloc to access columns by position
        years = df_cit.iloc[:, 0]
        mean_tc_per_art = df_cit.iloc[:, 1] if len(df_cit.columns) > 1 else None
        mean_tc_per_year = df_cit.iloc[:, 2] if len(df_cit.columns) > 2 else None
        
        if mean_tc_per_art is not None:
            ax1.bar(years, mean_tc_per_art, alpha=0.7, color='lightcoral', label='Mean TC per Article')
            ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
            ax1.set_ylabel('Mean Total Citations per Article', fontsize=12, fontweight='bold', color='darkred')
            ax1.tick_params(axis='y', labelcolor='darkred')
        
        if mean_tc_per_year is not None:
            ax2 = ax1.twinx()
            ax2.plot(years, mean_tc_per_year, 'o-', color='darkblue', linewidth=2, markersize=6, label='Mean TC per Year')
            ax2.set_ylabel('Mean Total Citations per Year', fontsize=12, fontweight='bold', color='darkblue')
            ax2.tick_params(axis='y', labelcolor='darkblue')
        
        plt.title('Annual Citation Trends', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(output_dir / '02_Annual_Citations_per_Year.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("    [OK] Saved")
    except Exception as e:
        print(f"    [SKIP] {e}")
    
    # 3. Most Relevant Sources
    try:
        print("[3/15] Most Relevant Sources...")
        df_sources = pd.read_excel(xl, sheet_name='MostRelSources')
        
        plt.figure(figsize=(12, 8))
        top_sources = df_sources.head(15)
        plt.barh(range(len(top_sources)), top_sources.iloc[:, 1], color='mediumseagreen', alpha=0.8)
        plt.yticks(range(len(top_sources)), top_sources.iloc[:, 0], fontsize=10)
        plt.xlabel('Number of Articles', fontsize=12, fontweight='bold')
        plt.title('Most Relevant Sources (Top 15)', fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig(output_dir / '03_Most_Relevant_Sources.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("    [OK] Saved")
    except Exception as e:
        print(f"    [SKIP] {e}")
    
    # 4. Bradford's Law
    try:
        print("[4/15] Bradford's Law...")
        df_bradford = pd.read_excel(xl, sheet_name='BradfordLaw')
        
        plt.figure(figsize=(12, 6))
        plt.scatter(range(len(df_bradford)), np.cumsum(df_bradford.iloc[:, 1]), alpha=0.6, s=50, color='purple')
        plt.plot(range(len(df_bradford)), np.cumsum(df_bradford.iloc[:, 1]), color='purple', linewidth=2, alpha=0.8)
        plt.xlabel('Source Rank (log scale)', fontsize=12, fontweight='bold')
        plt.ylabel('Cumulative Number of Articles', fontsize=12, fontweight='bold')
        plt.title("Bradford's Law - Source Concentration", fontsize=14, fontweight='bold')
        plt.xscale('log')
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_dir / '04_Bradford_Law.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("    [OK] Saved")
    except Exception as e:
        print(f"    [SKIP] {e}")
    
    # 5. Most Relevant Authors
    try:
        print("[5/15] Most Relevant Authors...")
        df_authors = pd.read_excel(xl, sheet_name='MostRelAuthors')
        
        plt.figure(figsize=(12, 8))
        top_authors = df_authors.head(15)
        plt.barh(range(len(top_authors)), top_authors.iloc[:, 1], color='darkorange', alpha=0.8)
        plt.yticks(range(len(top_authors)), top_authors.iloc[:, 0], fontsize=10)
        plt.xlabel('Number of Articles', fontsize=12, fontweight='bold')
        plt.title('Most Prolific Authors (Top 15)', fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig(output_dir / '05_Most_Relevant_Authors.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("    [OK] Saved")
    except Exception as e:
        print(f"    [SKIP] {e}")
    
    # 6. Lotka's Law
    try:
        print("[6/15] Lotka's Law...")
        df_lotka = pd.read_excel(xl, sheet_name='LotkaLaw')
        
        plt.figure(figsize=(12, 6))
        if len(df_lotka) > 0:
            plt.plot(df_lotka.iloc[:, 0], df_lotka.iloc[:, 1], 'o-', color='teal', linewidth=2, markersize=8, label='Observed')
            if len(df_lotka.columns) > 2:
                plt.plot(df_lotka.iloc[:, 0], df_lotka.iloc[:, 2], 's--', color='crimson', linewidth=2, markersize=6, label='Lotka\'s Law')
            plt.xlabel('Documents Written', fontsize=12, fontweight='bold')
            plt.ylabel('Proportion of Authors', fontsize=12, fontweight='bold')
            plt.title("Lotka's Law - Author Productivity Distribution", fontsize=14, fontweight='bold')
            plt.legend()
            plt.grid(alpha=0.3)
            plt.tight_layout()
            plt.savefig(output_dir / '06_Lotka_Law.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("    [OK] Saved")
    except Exception as e:
        print(f"    [SKIP] {e}")
    
    # 7. Country Scientific Production
    try:
        print("[7/15] Country Scientific Production...")
        df_countries = pd.read_excel(xl, sheet_name='CountrySciProd')
        
        plt.figure(figsize=(12, 8))
        top_countries = df_countries.head(15)
        plt.barh(range(len(top_countries)), top_countries.iloc[:, 1], color='royalblue', alpha=0.8)
        plt.yticks(range(len(top_countries)), top_countries.iloc[:, 0], fontsize=10)
        plt.xlabel('Number of Documents', fontsize=12, fontweight='bold')
        plt.title('Most Productive Countries (Top 15)', fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig(output_dir / '07_Country_Scientific_Production.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("    [OK] Saved")
    except Exception as e:
        print(f"    [SKIP] {e}")
    
    # 8. Most Cited Countries
    try:
        print("[8/15] Most Cited Countries...")
        df_cit_countries = pd.read_excel(xl, sheet_name='MostCitCountries')
        
        plt.figure(figsize=(12, 8))
        top_cit_countries = df_cit_countries.head(15)
        plt.barh(range(len(top_cit_countries)), top_cit_countries.iloc[:, 1], color='indianred', alpha=0.8)
        plt.yticks(range(len(top_cit_countries)), top_cit_countries.iloc[:, 0], fontsize=10)
        plt.xlabel('Total Citations', fontsize=12, fontweight='bold')
        plt.title('Most Cited Countries (Top 15)', fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig(output_dir / '08_Most_Cited_Countries.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("    [OK] Saved")
    except Exception as e:
        print(f"    [SKIP] {e}")
    
    # 9. Most Frequent Words
    try:
        print("[9/15] Most Frequent Words...")
        df_words = pd.read_excel(xl, sheet_name='MostFreqWords')
        
        plt.figure(figsize=(12, 8))
        top_words = df_words.head(20)
        plt.barh(range(len(top_words)), top_words.iloc[:, 1], color='darkviolet', alpha=0.8)
        plt.yticks(range(len(top_words)), top_words.iloc[:, 0], fontsize=10)
        plt.xlabel('Occurrences', fontsize=12, fontweight='bold')
        plt.title('Most Frequent Keywords (Top 20)', fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig(output_dir / '09_Most_Frequent_Words.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("    [OK] Saved")
    except Exception as e:
        print(f"    [SKIP] {e}")
    
    # 10. Word Cloud
    try:
        print("[10/15] Word Cloud...")
        df_wordcloud = pd.read_excel(xl, sheet_name='WordCloud')
        
        if len(df_wordcloud) > 0:
            word_freq = dict(zip(df_wordcloud.iloc[:, 0], df_wordcloud.iloc[:, 1]))
            
            wordcloud = WordCloud(
                width=1600,
                height=800,
                background_color='white',
                colormap='viridis',
                relative_scaling=0.5,
                min_font_size=10
            ).generate_from_frequencies(word_freq)
            
            plt.figure(figsize=(16, 8))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title('Keyword Word Cloud', fontsize=18, fontweight='bold', pad=20)
            plt.tight_layout()
            plt.savefig(output_dir / '10_Word_Cloud.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("    [OK] Saved")
    except Exception as e:
        print(f"    [SKIP] {e}")
    
    # 11. Trend Topics
    try:
        print("[11/15] Trend Topics...")
        df_trends = pd.read_excel(xl, sheet_name='TrendTopics')
        
        if len(df_trends) > 0:
            plt.figure(figsize=(14, 8))
            
            # Group by year and topic (assuming columns: Year, Topic, Frequency)
            years = df_trends.iloc[:, 0].unique()
            
            # Plot top 5 topics over time
            top_topics = df_trends.groupby(df_trends.columns[1]).sum().nlargest(5, df_trends.columns[2]).index
            
            for topic in top_topics:
                topic_data = df_trends[df_trends.iloc[:, 1] == topic]
                plt.plot(topic_data.iloc[:, 0], topic_data.iloc[:, 2], marker='o', linewidth=2, label=str(topic)[:30])
            
            plt.xlabel('Year', fontsize=12, fontweight='bold')
            plt.ylabel('Frequency', fontsize=12, fontweight='bold')
            plt.title('Trending Topics Over Time', fontsize=14, fontweight='bold')
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.grid(alpha=0.3)
            plt.tight_layout()
            plt.savefig(output_dir / '11_Trend_Topics.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("    [OK] Saved")
    except Exception as e:
        print(f"    [SKIP] {e}")
    
    # 12. Most Globally Cited Documents
    try:
        print("[12/15] Most Globally Cited Documents...")
        df_glob_cit = pd.read_excel(xl, sheet_name='MostGlobCitDocs')
        
        plt.figure(figsize=(14, 8))
        top_cited = df_glob_cit.head(15)
        
        # Truncate long titles
        titles = [str(t)[:60] + '...' if len(str(t)) > 60 else str(t) for t in top_cited.iloc[:, 0]]
        
        plt.barh(range(len(top_cited)), top_cited.iloc[:, 1], color='crimson', alpha=0.8)
        plt.yticks(range(len(top_cited)), titles, fontsize=9)
        plt.xlabel('Total Citations', fontsize=12, fontweight='bold')
        plt.title('Most Globally Cited Documents (Top 15)', fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig(output_dir / '12_Most_Globally_Cited_Documents.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("    [OK] Saved")
    except Exception as e:
        print(f"    [SKIP] {e}")
    
    # 13. Source Production Over Time
    try:
        print("[13/15] Source Production Over Time...")
        df_source_time = pd.read_excel(xl, sheet_name='SourceProdOverTime')
        
        if len(df_source_time) > 5:
            plt.figure(figsize=(14, 8))
            
            # Get top 5 sources
            top_sources_names = df_source_time.groupby(df_source_time.columns[0]).sum().nlargest(5, df_source_time.columns[2]).index
            
            for source in top_sources_names:
                source_data = df_source_time[df_source_time.iloc[:, 0] == source]
                plt.plot(source_data.iloc[:, 1], source_data.iloc[:, 2], marker='o', linewidth=2, label=str(source)[:40])
            
            plt.xlabel('Year', fontsize=12, fontweight='bold')
            plt.ylabel('Number of Articles', fontsize=12, fontweight='bold')
            plt.title('Source Production Over Time (Top 5 Sources)', fontsize=14, fontweight='bold')
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
            plt.grid(alpha=0.3)
            plt.tight_layout()
            plt.savefig(output_dir / '13_Source_Production_Over_Time.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("    [OK] Saved")
    except Exception as e:
        print(f"    [SKIP] {e}")
    
    # 14. Country Collaboration Map
    try:
        print("[14/15] Country Collaboration Map...")
        df_collab = pd.read_excel(xl, sheet_name='CollabWorldMap')
        
        if len(df_collab) > 0:
            plt.figure(figsize=(12, 8))
            
            # Create network visualization of top collaborations
            top_collab = df_collab.head(20)
            
            countries = list(set(list(top_collab.iloc[:, 0]) + list(top_collab.iloc[:, 1])))
            country_counts = {}
            
            for country in countries:
                count = len(top_collab[(top_collab.iloc[:, 0] == country) | (top_collab.iloc[:, 1] == country)])
                country_counts[country] = count
            
            sorted_countries = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            
            plt.barh(range(len(sorted_countries)), [c[1] for c in sorted_countries], color='teal', alpha=0.8)
            plt.yticks(range(len(sorted_countries)), [c[0] for c in sorted_countries], fontsize=10)
            plt.xlabel('Number of Collaborations', fontsize=12, fontweight='bold')
            plt.title('Most Collaborative Countries (Top 10)', fontsize=14, fontweight='bold')
            plt.gca().invert_yaxis()
            plt.tight_layout()
            plt.savefig(output_dir / '14_Country_Collaboration_Map.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("    [OK] Saved")
    except Exception as e:
        print(f"    [SKIP] {e}")
    
    # 15. Corresponding Author Countries
    try:
        print("[15/15] Corresponding Author Countries...")
        df_corr_auth = pd.read_excel(xl, sheet_name='CorrAuthCountries')
        
        plt.figure(figsize=(12, 8))
        top_corr = df_corr_auth.head(15)
        plt.barh(range(len(top_corr)), top_corr.iloc[:, 1], color='gold', alpha=0.8)
        plt.yticks(range(len(top_corr)), top_corr.iloc[:, 0], fontsize=10)
        plt.xlabel('Number of Corresponding Authors', fontsize=12, fontweight='bold')
        plt.title('Corresponding Author Countries (Top 15)', fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig(output_dir / '15_Corresponding_Author_Countries.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("    [OK] Saved")
    except Exception as e:
        print(f"    [SKIP] {e}")
    
    print("\n" + "="*80)
    print("PLOT GENERATION COMPLETE")
    print("="*80)
    print(f"\nPlots saved to: {output_dir}")
    print(f"Total plots generated: {len(list(output_dir.glob('*.png')))}")


def main():
    """Main execution."""
    
    # Define paths
    script_dir = Path(__file__).parent
    data_file = script_dir / 'output_aligned_207' / 'BibliometricAnalysis_Aligned_207_Papers.xlsx'
    output_dir = script_dir / 'output_aligned_207' / 'plots'
    
    print("\n" + "="*80)
    print("BIBLIOMETRIC PLOT GENERATION - ALIGNED 207 PAPERS")
    print("="*80)
    print(f"\nData file: {data_file}")
    print(f"Output directory: {output_dir}")
    
    if not data_file.exists():
        print(f"\n[ERROR] Data file not found: {data_file}")
        return
    
    # Generate plots
    generate_all_plots(data_file, output_dir)
    
    print(f"\n[OK] All plots generated successfully!")
    print(f"\nPlots location: {output_dir}")
    print(f"\nYou can now view the plots in the folder above.")


if __name__ == '__main__':
    main()

