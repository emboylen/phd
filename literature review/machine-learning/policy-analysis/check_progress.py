import pandas as pd
import os

# Check the log
log = pd.read_csv('download_log.csv')
print(f'Total attempts logged: {len(log)}')
print(f'Successful: {(log["Status"] == "SUCCESS").sum()}')
print(f'Failed: {(log["Status"] == "FAILED").sum()}')
print(f'Skipped: {(log["Status"] == "SKIPPED").sum()}')
print(f'Last entry index: {log["Index"].max()}')

# Check downloaded files
if os.path.exists('downloaded_policies'):
    files = os.listdir('downloaded_policies')
    print(f'\nFiles in downloaded_policies: {len(files)}')

# Check total policies
df = pd.read_csv('export-2025-11-25.csv')
print(f'\nTotal policies in new export: {len(df)}')
print(f'Policies with URLs: {df["Document URL"].notna().sum()}')

