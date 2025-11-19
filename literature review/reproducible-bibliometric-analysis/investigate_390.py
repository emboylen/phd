import pandas as pd

print("Investigating why Biblioshiny shows 390 records...")
print("="*70)

# Check the original filtered_data.xlsx
df_orig = pd.read_excel('data/filtered_data.xlsx', engine='openpyxl')
print(f"\nOriginal filtered_data.xlsx: {len(df_orig)} records")

# Check for any duplicate issues
print("\nChecking for duplicate identifiers in SR column:")
if 'SR' in df_orig.columns:
    sr_null = df_orig['SR'].isna().sum()
    sr_non_null = df_orig['SR'].notna().sum()
    print(f"  Non-null SR: {sr_non_null}")
    print(f"  Null SR: {sr_null}")
    
    # Check for duplicates in SR
    sr_dups = df_orig[df_orig['SR'].notna() & df_orig['SR'].duplicated(keep=False)]
    if len(sr_dups) > 0:
        print(f"  DUPLICATE SR values found: {len(sr_dups)} rows")
        print(f"  Unique duplicate SR values: {sr_dups['SR'].nunique()}")

# Check DI column for duplicates
print("\nChecking for duplicate DOIs:")
if 'DI' in df_orig.columns:
    di_null = df_orig['DI'].isna().sum()
    di_non_null = df_orig['DI'].notna().sum()
    print(f"  Non-null DI: {di_non_null}")
    print(f"  Null DI: {di_null}")
    
    # Check for duplicates
    di_dups = df_orig[df_orig['DI'].notna() & df_orig['DI'].duplicated(keep=False)]
    if len(di_dups) > 0:
        print(f"  DUPLICATE DI values found: {len(di_dups)} rows")
        dup_dois = df_orig[df_orig['DI'].notna()]['DI'].value_counts()
        dup_dois = dup_dois[dup_dois > 1]
        print(f"  Number of DOIs appearing multiple times: {len(dup_dois)}")
        if len(dup_dois) <= 20:
            print("\n  All duplicate DOIs:")
            for doi, count in dup_dois.items():
                print(f"    {doi}: appears {count} times")

# Check if there are completely empty rows
print("\nChecking for empty rows:")
empty_rows = df_orig[df_orig.isna().all(axis=1)]
print(f"  Completely empty rows: {len(empty_rows)}")

# Check if there are rows with all key fields null
key_fields = ['SR', 'DI', 'TI', 'AU', 'PY']
available_key_fields = [f for f in key_fields if f in df_orig.columns]
mostly_empty = df_orig[df_orig[available_key_fields].isna().all(axis=1)]
print(f"  Rows with all key fields null: {len(mostly_empty)}")

# Look at the Biblioshiny report to see what might cause 390
print("\n" + "="*70)
print("Checking Biblioshiny MainInfo for clues...")
bib_main = pd.read_excel('output/BiblioshinyReport-2025-11-19.xlsx', sheet_name='MainInfo')
print("\nBiblioshiny MainInfo:")
print(bib_main.head(10).to_string())

# Could there be an issue with how the file was read?
# Maybe Biblioshiny saw the file twice somehow, or there's an encoding issue?
print("\n" + "="*70)
print("HYPOTHESIS:")
print("390 documents / 222 original = 1.76")
print("This doesn't match any obvious duplication pattern (not 2x)")
print("\nLet me check if 390 could come from counting something else...")

# Maybe it's counting references or something?
if 'CR' in df_orig.columns:
    # Count total references
    total_refs = 0
    for refs in df_orig['CR'].dropna():
        if isinstance(refs, str):
            # Count semicolon-separated references
            ref_list = [r.strip() for r in refs.split(';') if r.strip()]
            total_refs += len(ref_list)
    print(f"\nTotal cited references in CR column: {total_refs}")

print("\n" + "="*70)
print("RECOMMENDATION:")
print("Use filtered_data.xlsx (222 records) and upload it fresh to Biblioshiny")
print("The 390 figure seems incorrect - possibly from a different/corrupted upload")

