import pandas as pd
import os

# Load the new export
df_new = pd.read_csv('export-2025-11-25.csv')
print(f'New export: {len(df_new)} total policies')
print(f'New export with URLs: {df_new["Document URL"].notna().sum()}')

# Check how many are already downloaded
downloaded_dir = 'downloaded_policies'
if os.path.exists(downloaded_dir):
    existing_files = os.listdir(downloaded_dir)
    existing_ids = set(f.split('.')[0] for f in existing_files)
    print(f'\nAlready downloaded: {len(existing_files)} files')
    
    # Find which policies need downloading
    policies_with_urls = df_new[df_new['Document URL'].notna()]
    new_to_download = policies_with_urls[~policies_with_urls['Overton id'].astype(str).isin(existing_ids)]
    print(f'New policies to download: {len(new_to_download)}')
else:
    print(f'\nNo downloads yet - will download all {df_new["Document URL"].notna().sum()} policies with URLs')

print('\nColumn names in export:')
print(df_new.columns.tolist())

