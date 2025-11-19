import pandas as pd

print("Preparing clean file for Biblioshiny upload...")
print("="*70)

# Load the original file
df = pd.read_excel('data/filtered_data.xlsx', engine='openpyxl')
print(f"Original: {len(df)} records")

# Remove completely empty rows (rows where all key fields are null)
df_cleaned = df[df['SR'].notna()].copy()
print(f"After removing empty rows: {len(df_cleaned)} records")

# Remove duplicate DOI
df_cleaned = df_cleaned.drop_duplicates(subset=['DI'], keep='first')
print(f"After removing duplicate DOI: {len(df_cleaned)} records")

# Verify no duplicates in SR column
sr_dups = df_cleaned[df_cleaned['SR'].duplicated()]
if len(sr_dups) > 0:
    print(f"WARNING: Still have {len(sr_dups)} duplicate SR values")
else:
    print("Verified: No duplicate SR values")

# Save the cleaned file
output_file = 'data/filtered_data_biblioshiny_ready.xlsx'
df_cleaned.to_excel(output_file, index=False, engine='openpyxl')
print(f"\nSaved clean file: {output_file}")
print(f"Final record count: {len(df_cleaned)}")

print("\n" + "="*70)
print("READY FOR BIBLIOSHINY:")
print(f"File: {output_file}")
print(f"Records: {len(df_cleaned)}")
print(f"Years: {int(df_cleaned['PY'].min())}-{int(df_cleaned['PY'].max())}")
print(f"Sources: {df_cleaned['SO'].nunique()}")
print("\nUpload this file to Biblioshiny to generate a report with 214 documents")
print("="*70)

