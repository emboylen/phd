import pandas as pd

# Load the new report
xl = pd.ExcelFile('output/BiblioshinyReport-2025-11-19.xlsx', engine='openpyxl')

print("NEW BIBLIOSHINY REPORT STRUCTURE")
print("="*70)
print(f"Total sheets: {len(xl.sheet_names)}\n")

for i, sheet in enumerate(xl.sheet_names, 1):
    df = pd.read_excel(xl, sheet_name=sheet)
    print(f"{i:2d}. {sheet:30s} - {df.shape[0]:4d} rows x {df.shape[1]:2d} cols")

# Check if stopwords or synonyms files exist
print("\n" + "="*70)
print("CHECKING FOR STOPWORDS/SYNONYMS FILES:")
print("="*70)

import os
import glob

# Look for common names
patterns = ['*stopword*', '*synonym*', '*stop*word*', '*stop_word*']
for pattern in patterns:
    files = glob.glob(f'**/{pattern}', recursive=True)
    if files:
        print(f"\nFound files matching '{pattern}':")
        for f in files:
            print(f"  {f}")

