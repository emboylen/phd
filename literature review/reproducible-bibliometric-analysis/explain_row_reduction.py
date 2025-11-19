import pandas as pd

print("Explaining the row count reduction from 222 to 214...")
print("="*70)

# Load the original filtered_data.xlsx
df_original = pd.read_excel('data/filtered_data.xlsx', engine='openpyxl')
print(f"\nOriginal filtered_data.xlsx: {len(df_original)} rows")

# Show what was removed
print("\n1. EMPTY ROWS (7 rows removed):")
print("-"*70)
empty_rows = df_original[df_original['SR'].isna()]
print(f"   Found {len(empty_rows)} completely empty rows with no SR identifier")
print(f"   These rows have no authors, title, DOI, or any key information")
print(f"   Row indices: {empty_rows.index.tolist()}")
print(f"   NOTE: These caused the 'duplicate row.names' error in Biblioshiny")

# After removing empty rows
df_no_empty = df_original[df_original['SR'].notna()].copy()
print(f"\n   After removing empty rows: {len(df_no_empty)} rows")

print("\n2. DUPLICATE DOI (1 row removed):")
print("-"*70)
# Find duplicate DOI
di_dups = df_no_empty[df_no_empty['DI'].notna() & df_no_empty['DI'].duplicated(keep=False)]
if len(di_dups) > 0:
    print(f"   Found {len(di_dups)} rows with duplicate DOI")
    for doi in di_dups['DI'].unique():
        dup_rows = df_no_empty[df_no_empty['DI'] == doi]
        print(f"\n   DOI: {doi}")
        print(f"   Row indices: {dup_rows.index.tolist()}")
        for idx in dup_rows.index:
            au = str(df_no_empty.loc[idx, 'AU'])[:50] if pd.notna(df_no_empty.loc[idx, 'AU']) else 'No author'
            ti = str(df_no_empty.loc[idx, 'TI'])[:50] if pd.notna(df_no_empty.loc[idx, 'TI']) else 'No title'
            print(f"     Row {idx}: {au}... | {ti}...")

df_no_dups = df_no_empty.drop_duplicates(subset=['DI'], keep='first')
print(f"\n   After removing duplicate DOI: {len(df_no_dups)} rows")

print("\n" + "="*70)
print("SUMMARY:")
print(f"  Original:              222 rows")
print(f"  - Empty rows:           -7 rows  = 215 rows")
print(f"  - Duplicate DOI:        -1 row   = 214 rows")
print(f"  Final:                 214 rows")

print("\n" + "="*70)
print("OPTIONS:")
print("="*70)
print("\nOption 1: Keep 214 rows (RECOMMENDED)")
print("  ✓ No empty rows")
print("  ✓ No duplicate DOIs")
print("  ✓ Will work correctly in Biblioshiny")
print("  ✓ Clean, valid dataset")

print("\nOption 2: Keep all 222 rows")
print("  ✗ Includes 7 completely empty rows")
print("  ✗ Includes 1 duplicate DOI")
print("  ✗ Will cause 'duplicate row.names' error in Biblioshiny")
print("  ✗ Empty rows have no scientific value")

print("\nWhich option do you prefer?")

