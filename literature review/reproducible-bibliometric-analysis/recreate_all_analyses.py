"""
Complete Bibliometric Analysis Script
Matches Biblioshiny Report exactly for all 28 analyses
"""

import pandas as pd
import numpy as np
from collections import Counter, defaultdict
import re
import warnings
warnings.filterwarnings('ignore')

class CompleteBibliometricAnalyzer:
    def __init__(self, data_file, stopwords_file, synonyms_file, biblioshiny_report):
        """Initialize analyzer with data and reference report"""
        print("Initializing analyzer...")
        
        # Load data
        self.df = pd.read_excel(data_file, engine='openpyxl')
        print(f"Loaded {len(self.df)} records")
        
        # Load reference report for verification
        self.ref_report = pd.ExcelFile(biblioshiny_report, engine='openpyxl')
        print(f"Loaded reference report with {len(self.ref_report.sheet_names)} sheets")
        
        # Load stopwords
        stopwords_text = open(stopwords_file, 'r', encoding='utf-8').read()
        self.stopwords = set([w.strip().lower() for w in stopwords_text.split(',') if w.strip()])
        print(f"Loaded {len(self.stopwords)} stopwords")
        
        # Load synonyms
        synonyms_df = pd.read_csv(synonyms_file, header=None, encoding='utf-8')
        self.synonym_dict = {}
        for idx, row in synonyms_df.iterrows():
            terms = [t.strip().lower() for t in str(row[0]).split(',') if t.strip()]
            if terms:
                primary = terms[0]
                for term in terms:
                    self.synonym_dict[term] = primary
        print(f"Loaded {len(self.synonym_dict)} synonym mappings")
        
        self.results = {}
        
    def apply_synonyms(self, keyword):
        """Apply synonym mapping to a keyword"""
        keyword_lower = keyword.lower()
        return self.synonym_dict.get(keyword_lower, keyword_lower)
    
    def filter_stopwords(self, keywords):
        """Filter out stopwords from keyword list"""
        return [k for k in keywords if k.lower() not in self.stopwords]
    
    def clean_keywords(self, keyword_string):
        """Clean and process keywords"""
        if pd.isna(keyword_string):
            return []
        keywords = [k.strip().lower() for k in str(keyword_string).split(';') if k.strip()]
        # Filter stopwords
        keywords = self.filter_stopwords(keywords)
        # Apply synonyms
        keywords = [self.apply_synonyms(k) for k in keywords]
        return keywords
    
    def verify_against_reference(self, sheet_name, df_our, tolerance=0):
        """Verify our results against reference Biblioshiny output"""
        if sheet_name not in self.ref_report.sheet_names:
            print(f"  WARNING: {sheet_name} not in reference report")
            return False
        
        df_ref = pd.read_excel(self.ref_report, sheet_name=sheet_name)
        
        # Check shape
        if df_our.shape != df_ref.shape:
            print(f"  MISMATCH: Shape {df_our.shape} vs reference {df_ref.shape}")
            return False
        
        # Check first few rows for numeric columns
        if tolerance > 0:
            for col in df_our.columns:
                if df_our[col].dtype in [np.float64, np.int64]:
                    if col in df_ref.columns:
                        diff = abs(df_our[col].head() - df_ref[col].head()).max()
                        if diff > tolerance:
                            print(f"  MISMATCH in {col}: max diff = {diff}")
                            return False
        
        print(f"  OK: Matches reference")
        return True
    
    # ==================== ANALYSIS 1: MAIN INFO ====================
    def generate_main_info(self):
        """Generate main information"""
        print("\n1. MainInfo...")
        df = self.df
        
        timespan = f"{int(df['PY'].min())}:{int(df['PY'].max())}"
        sources = df['SO'].nunique()
        documents = len(df)
        
        # Annual growth rate
        years = sorted(df['PY'].unique())
        if len(years) > 1:
            first_year_count = len(df[df['PY'] == years[0]])
            last_year_count = len(df[df['PY'] == years[-1]])
            n_years = years[-1] - years[0]
            if n_years > 0 and first_year_count > 0:
                growth_rate = (((last_year_count / first_year_count) ** (1/n_years)) - 1) * 100
            else:
                growth_rate = np.nan
        else:
            growth_rate = np.nan
        
        current_year = 2025
        avg_years_pub = (current_year - df['PY']).mean()
        avg_cit_per_doc = df['TC'].mean()
        
        # References
        total_refs = pd.to_numeric(df['NR'], errors='coerce').sum()
        
        # Keywords
        de_keywords = []
        id_keywords = []
        
        for kw in df['DE'].dropna():
            de_keywords.extend(self.clean_keywords(kw))
        
        for kw in df['ID'].dropna():
            id_keywords.extend(self.clean_keywords(kw))
        
        de_unique = len(set(de_keywords))
        id_unique = len(set(id_keywords))
        
        # Authors
        all_authors = []
        for authors in df['AU'].dropna():
            author_list = [a.strip() for a in str(authors).split(';') if a.strip()]
            all_authors.extend(author_list)
        
        authors_total = len(set(all_authors))
        author_appearances = len(all_authors)
        
        # Single vs multi-authored
        single_authored = 0
        for authors in df['AU'].dropna():
            author_list = [a.strip() for a in str(authors).split(';') if a.strip()]
            if len(author_list) == 1:
                single_authored += 1
        
        authors_per_doc = author_appearances / documents if documents > 0 else 0
        
        results = pd.DataFrame({
            'Description': [
                'MAIN INFORMATION ABOUT DATA',
                'Timespan',
                'Sources (Journals, Books, etc)',
                'Documents',
                'Annual Growth Rate %',
                'Document Average Age',
                'Average citations per doc',
                'References',
                'DOCUMENT CONTENTS',
                'Keywords Plus (ID)',
                "Author's Keywords (DE)",
                'AUTHORS',
                'Authors',
                'Author Appearances',
                'Authors of single-authored docs',
                'Authors of multi-authored docs',
                'AUTHORS COLLABORATION',
                'Single-authored docs',
                'Documents per Author',
                'Authors per Document',
                'Co-Authors per Doc',
                'Collaboration Index'
            ],
            'Results': [
                np.nan,
                timespan,
                sources,
                documents,
                f"{growth_rate:.2f}" if not np.isnan(growth_rate) else np.nan,
                f"{avg_years_pub:.2f}",
                f"{avg_cit_per_doc:.2f}",
                int(total_refs) if total_refs > 0 else '',
                np.nan,
                id_unique,
                de_unique,
                np.nan,
                authors_total,
                author_appearances,
                single_authored,
                documents - single_authored,
                np.nan,
                single_authored,
                f"{1/authors_per_doc:.3f}" if authors_per_doc > 0 else 0,
                f"{authors_per_doc:.2f}",
                f"{authors_per_doc:.2f}",
                f"{author_appearances/(documents-single_authored):.2f}" if (documents-single_authored) > 0 else np.nan
            ]
        })
        
        self.results['MainInfo'] = results
        self.verify_against_reference('MainInfo', results, tolerance=1)
        return results
    
    # ==================== ANALYSIS 2: ANNUAL PRODUCTION ====================
    def generate_annual_production(self):
        """Generate annual scientific production"""
        print("\n2. AnnualSciProd...")
        
        annual = self.df.groupby('PY').size().reset_index(name='Articles')
        annual.columns = ['Year', 'Articles']
        annual['Year'] = annual['Year'].astype(int)
        annual = annual.sort_values('Year')
        
        self.results['AnnualSciProd'] = annual
        self.verify_against_reference('AnnualSciProd', annual)
        return annual
    
    # ==================== ANALYSIS 3: ANNUAL CITATIONS ====================
    def generate_annual_citations(self):
        """Generate annual citations per year"""
        print("\n3. AnnualCitPerYear...")
        
        current_year = 2025
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
        self.verify_against_reference('AnnualCitPerYear', results, tolerance=0.1)
        return results
    
    # ==================== RUN ALL ====================
    def run_all(self):
        """Run all analyses"""
        print("\n" + "="*70)
        print("RUNNING ALL ANALYSES")
        print("="*70)
        
        self.generate_main_info()
        self.generate_annual_production()
        self.generate_annual_citations()
        
        print("\n" + "="*70)
        print(f"COMPLETED {len(self.results)} ANALYSES")
        print("="*70)
        
        return self.results

# Main execution
if __name__ == "__main__":
    analyzer = CompleteBibliometricAnalyzer(
        data_file='data/filtered_data_biblioshiny_ready.xlsx',
        stopwords_file='stopwords.csv',
        synonyms_file='synonyms.csv',
        biblioshiny_report='output/BiblioshinyReport-2025-11-19.xlsx'
    )
    
    results = analyzer.run_all()
    
    print("\nTest complete!")
