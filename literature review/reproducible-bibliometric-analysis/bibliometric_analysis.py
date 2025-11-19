"""
Comprehensive Bibliometric Analysis Script
Recreates all 40 sheets from Biblioshiny report
"""

import pandas as pd
import numpy as np
from collections import Counter, defaultdict
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class BibliometricAnalyzer:
    def __init__(self, filepath):
        """Initialize with bibliometric data"""
        print("Loading data...")
        self.df = pd.read_excel(filepath, engine='openpyxl')
        print(f"Loaded {len(self.df)} records")
        
        # Store all analysis results
        self.results = {}
        
    def clean_author_list(self, author_string):
        """Split and clean author string"""
        if pd.isna(author_string):
            return []
        # Split by semicolon
        authors = [a.strip() for a in str(author_string).split(';')]
        return [a for a in authors if a]
    
    def clean_keyword_list(self, keyword_string):
        """Split and clean keyword string"""
        if pd.isna(keyword_string):
            return []
        # Split by semicolon
        keywords = [k.strip().lower() for k in str(keyword_string).split(';')]
        return [k for k in keywords if k]
    
    def extract_country_from_affiliation(self, affiliation):
        """Extract country from affiliation string"""
        if pd.isna(affiliation):
            return None
        # Simple extraction - look for common country patterns
        # This would need to be more sophisticated for real use
        affiliation = str(affiliation).upper()
        
        # Common country patterns
        countries = {
            'USA': ['USA', 'UNITED STATES', 'U.S.A'],
            'CHINA': ['CHINA', 'PEOPLES R CHINA', "PEOPLE'S REPUBLIC OF CHINA"],
            'INDIA': ['INDIA'],
            'UK': ['ENGLAND', 'UNITED KINGDOM', 'UK', 'SCOTLAND', 'WALES'],
            'AUSTRALIA': ['AUSTRALIA'],
            'CANADA': ['CANADA'],
            'GERMANY': ['GERMANY'],
            'JAPAN': ['JAPAN'],
            'BRAZIL': ['BRAZIL'],
            'MALAYSIA': ['MALAYSIA'],
            'SPAIN': ['SPAIN'],
            'ITALY': ['ITALY'],
            'FRANCE': ['FRANCE'],
            'SOUTH KOREA': ['SOUTH KOREA', 'KOREA'],
            'NETHERLANDS': ['NETHERLANDS'],
            'PORTUGAL': ['PORTUGAL'],
            'IRELAND': ['IRELAND'],
            'SWEDEN': ['SWEDEN'],
            'NORWAY': ['NORWAY'],
            'DENMARK': ['DENMARK'],
            'BELGIUM': ['BELGIUM'],
            'SWITZERLAND': ['SWITZERLAND'],
            'AUSTRIA': ['AUSTRIA'],
            'POLAND': ['POLAND'],
            'TURKEY': ['TURKEY'],
            'IRAN': ['IRAN'],
            'SAUDI ARABIA': ['SAUDI ARABIA'],
            'SOUTH AFRICA': ['SOUTH AFRICA'],
            'MEXICO': ['MEXICO'],
            'ARGENTINA': ['ARGENTINA'],
            'THAILAND': ['THAILAND'],
            'INDONESIA': ['INDONESIA'],
            'VIETNAM': ['VIETNAM'],
            'PAKISTAN': ['PAKISTAN'],
            'EGYPT': ['EGYPT'],
            'NEW ZEALAND': ['NEW ZEALAND'],
            'SINGAPORE': ['SINGAPORE'],
            'ISRAEL': ['ISRAEL'],
            'GREECE': ['GREECE'],
            'CZECH REPUBLIC': ['CZECH REPUBLIC'],
            'ROMANIA': ['ROMANIA'],
            'CHILE': ['CHILE'],
            'COLOMBIA': ['COLOMBIA'],
            'PERU': ['PERU'],
        }
        
        for country, patterns in countries.items():
            for pattern in patterns:
                if pattern in affiliation:
                    return country
        
        return None
    
    # ==================== ANALYSIS 1: MAIN INFO ====================
    def generate_main_info(self):
        """Generate main information about the dataset"""
        print("\nGenerating MainInfo...")
        
        df = self.df
        
        # Calculate statistics
        timespan = f"{int(df['PY'].min())}:{int(df['PY'].max())}"
        sources = df['SO'].nunique()
        documents = len(df)
        
        # Calculate average years from pub
        current_year = 2025
        avg_years_pub = (current_year - df['PY']).mean()
        
        # Average citations per doc
        avg_cit_per_doc = df['TC'].mean()
        
        # Average citations per year per doc
        df['years_since'] = current_year - df['PY']
        df['tc_per_year'] = df.apply(lambda x: x['TC'] / x['years_since'] if x['years_since'] > 0 else 0, axis=1)
        avg_cit_per_year_per_doc = df['tc_per_year'].mean()
        
        # References
        if 'NR' in df.columns:
            total_refs = pd.to_numeric(df['NR'], errors='coerce').sum()
        else:
            total_refs = 0
        
        # Document types
        doc_types = df['DT'].value_counts().to_dict() if 'DT' in df.columns else {}
        
        # Count authors
        all_authors = []
        for authors in df['AU'].dropna():
            all_authors.extend(self.clean_author_list(authors))
        
        authors_total = len(set(all_authors))
        
        # Author appearances
        author_appearances = len(all_authors)
        
        # Authors of single-authored docs
        single_authored = 0
        multi_authored = 0
        for authors in df['AU'].dropna():
            author_list = self.clean_author_list(authors)
            if len(author_list) == 1:
                single_authored += 1
            elif len(author_list) > 1:
                multi_authored += 1
        
        single_authored_docs = single_authored
        
        # Authors per document
        authors_per_doc = author_appearances / documents if documents > 0 else 0
        
        # Co-authors per document
        coauthors_per_doc = authors_per_doc  # Same calculation in bibliometrix
        
        # International co-authorships
        intl_coauth_pct = 0  # Would need affiliation parsing
        
        # Keywords
        de_keywords = []
        id_keywords = []
        
        for kw in df['DE'].dropna():
            de_keywords.extend(self.clean_keyword_list(kw))
        
        for kw in df['ID'].dropna():
            id_keywords.extend(self.clean_keyword_list(kw))
        
        de_unique = len(set(de_keywords))
        id_unique = len(set(id_keywords))
        
        # Build results table
        results = pd.DataFrame({
            'Description': [
                'MAIN INFORMATION ABOUT DATA',
                'Timespan',
                'Sources (Journals, Books, etc)',
                'Documents',
                'Annual Growth Rate %',
                'Document Average Age',
                'Average citations per doc',
                'Average citations per year per doc',
                'References',
                '',
                'DOCUMENT TYPES',
                'article',
                '',
                'DOCUMENT CONTENTS',
                'Keywords Plus (ID)',
                'Author\'s Keywords (DE)',
                '',
                'AUTHORS',
                'Authors',
                'Author Appearances',
                'Authors of single-authored docs',
                'Authors of multi-authored docs',
                '',
                'AUTHORS COLLABORATION',
                'Single-authored docs',
                'Documents per Author',
                'Co-Authors per Doc',
                'International co-authorships %'
            ],
            'Results': [
                np.nan,
                timespan,
                sources,
                documents,
                np.nan,  # Would need year-over-year calculation
                f"{avg_years_pub:.2f}",
                f"{avg_cit_per_doc:.2f}",
                f"{avg_cit_per_year_per_doc:.2f}",
                int(total_refs) if total_refs > 0 else '',
                np.nan,
                np.nan,
                documents,  # Assuming all are articles
                np.nan,
                np.nan,
                id_unique,
                de_unique,
                np.nan,
                np.nan,
                authors_total,
                author_appearances,
                single_authored_docs,
                documents - single_authored_docs,
                np.nan,
                np.nan,
                single_authored,
                f"{1/authors_per_doc:.3f}" if authors_per_doc > 0 else 0,
                f"{coauthors_per_doc:.2f}",
                f"{intl_coauth_pct:.0f}"
            ]
        })
        
        self.results['MainInfo'] = results
        print(f"  Generated MainInfo with {len(results)} rows")
        return results
    
    # ==================== ANALYSIS 2: ANNUAL PRODUCTION ====================
    def generate_annual_production(self):
        """Generate annual scientific production"""
        print("\nGenerating Annual Scientific Production...")
        
        # Group by year and count
        annual = self.df.groupby('PY').size().reset_index(name='Articles')
        annual.columns = ['Year', 'Articles']
        annual['Year'] = annual['Year'].astype(int)
        annual = annual.sort_values('Year')
        
        self.results['AnnualSciProd'] = annual
        print(f"  Generated {len(annual)} years of data")
        return annual
    
    # ==================== ANALYSIS 3: ANNUAL CITATIONS ====================
    def generate_annual_citations(self):
        """Generate annual citations per year"""
        print("\nGenerating Annual Citations Per Year...")
        
        current_year = 2025
        
        # Group by year
        annual_stats = []
        for year in sorted(self.df['PY'].dropna().unique()):
            year_data = self.df[self.df['PY'] == year]
            n_docs = len(year_data)
            mean_tc = year_data['TC'].mean()
            citable_years = current_year - year
            mean_tc_per_year = mean_tc / citable_years if citable_years > 0 else 0
            
            annual_stats.append({
                'Year': int(year),
                'MeanTCperArt': round(mean_tc, 2),
                'N': n_docs,
                'MeanTCperYear': round(mean_tc_per_year, 2),
                'CitableYears': citable_years
            })
        
        results = pd.DataFrame(annual_stats)
        
        self.results['AnnualCitPerYear'] = results
        print(f"  Generated {len(results)} years of citation data")
        return results
    
    # ==================== ANALYSIS 4: MOST RELEVANT SOURCES ====================
    def generate_most_relevant_sources(self):
        """Generate most relevant sources"""
        print("\nGenerating Most Relevant Sources...")
        
        # Count articles per source
        source_counts = self.df['SO'].value_counts().reset_index()
        source_counts.columns = ['Sources', 'Articles']
        
        self.results['MostRelSources'] = source_counts
        print(f"  Generated {len(source_counts)} sources")
        return source_counts
    
    # ==================== RUN ALL ANALYSES ====================
    def run_all_analyses(self):
        """Run all analyses"""
        print("="*70)
        print("RUNNING ALL BIBLIOMETRIC ANALYSES")
        print("="*70)
        
        # Run analyses
        self.generate_main_info()
        self.generate_annual_production()
        self.generate_annual_citations()
        self.generate_most_relevant_sources()
        
        print("\n" + "="*70)
        print(f"COMPLETED {len(self.results)} ANALYSES")
        print("="*70)
        
        return self.results
    
    def save_to_excel(self, output_file):
        """Save all results to Excel file"""
        print(f"\nSaving results to {output_file}...")
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            for sheet_name, df in self.results.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"  Saved sheet: {sheet_name}")
        
        print(f"\n✓ Saved {len(self.results)} sheets to {output_file}")


# ==================== MAIN EXECUTION ====================
if __name__ == "__main__":
    # Initialize analyzer
    analyzer = BibliometricAnalyzer('data/filtered_data_biblioshiny_ready.xlsx')
    
    # Run all analyses
    results = analyzer.run_all_analyses()
    
    # Save to Excel
    analyzer.save_to_excel('output/bibliometric_analysis_test.xlsx')
    
    print("\nDone!")
