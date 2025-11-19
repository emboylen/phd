import pandas as pd

# Load both files
print("Comparing initial analyses with Biblioshiny output...")
print("="*70)

bib = pd.ExcelFile('output/BiblioshinyReport-2025-11-19.xlsx')
test = pd.ExcelFile('output/bibliometric_analysis_test.xlsx')

sheets_to_check = ['MainInfo', 'AnnualSciProd', 'AnnualCitPerYear', 'MostRelSources']

for sheet in sheets_to_check:
    print(f"\n{sheet}:")
    print("-"*70)
    
    df_bib = pd.read_excel(bib, sheet_name=sheet)
    df_test = pd.read_excel(test, sheet_name=sheet)
    
    print(f"Biblioshiny shape: {df_bib.shape}")
    print(f"Our analysis shape: {df_test.shape}")
    
    if sheet == 'MainInfo':
        print("\nFirst 10 rows comparison:")
        print("\nBiblioshiny:")
        print(df_bib.head(10).to_string())
        print("\nOurs:")
        print(df_test.head(10).to_string())
    
    elif sheet == 'AnnualSciProd':
        print("\nFirst 5 rows:")
        print("\nBiblioshiny:")
        print(df_bib.head(5).to_string())
        print("\nOurs:")
        print(df_test.head(5).to_string())
        print(f"\nBiblioshiny total articles: {df_bib['Articles'].sum()}")
        print(f"Our total articles: {df_test['Articles'].sum()}")
    
    elif sheet == 'Most RelSources':
        print("\nTop 10 sources:")
        print("\nBiblioshiny:")
        print(df_bib.head(10).to_string())
        print("\nOurs:")
        print(df_test.head(10).to_string())

