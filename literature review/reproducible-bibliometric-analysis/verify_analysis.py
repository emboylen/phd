"""
Compare our reproduced analysis with Biblioshiny report
"""
import pandas as pd

ref_file = 'output/BiblioshinyReport-2025-11-19.xlsx'
our_file = 'output/ReproducedBibliometricAnalysis.xlsx'

ref = pd.ExcelFile(ref_file)
our = pd.ExcelFile(our_file)

print("VERIFICATION REPORT")
print("="*70)
print(f"\nComparing: {our_file}")
print(f"Against:   {ref_file}\n")

sheets_to_verify = [
    'MainInfo', 'AnnualSciProd', 'AnnualCitPerYear', 
    'MostRelSources', 'BradfordLaw', 'MostRelAuthors',
    'MostFreqWords', 'WordCloud', 'CorrAuthCountries'
]

for sheet in sheets_to_verify:
    print(f"\n{sheet}:")
    print("-"*70)
    
    if sheet not in ref.sheet_names:
        print(f"  Not in reference report")
        continue
    
    df_ref = pd.read_excel(ref, sheet_name=sheet)
    df_our = pd.read_excel(our, sheet_name=sheet)
    
    print(f"  Reference shape: {df_ref.shape}")
    print(f"  Our shape:       {df_our.shape}")
    
    if df_ref.shape == df_our.shape:
        print(f"  OK Shape matches!")
    else:
        print(f"  X Shape mismatch")
    
    # Check first few values
    if len(df_ref) > 0 and len(df_our) > 0:
        print(f"\n  First 3 rows comparison:")
        print(f"\n  Reference:")
        print(f"  {df_ref.head(3).to_string().replace(chr(10), chr(10) + '  ')}")
        print(f"\n  Ours:")
        print(f"  {df_our.head(3).to_string().replace(chr(10), chr(10) + '  ')}")

print("\n" + "="*70)
print("VERIFICATION COMPLETE")
print("="*70)

