import pandas as pd
import os

# Load the new export
df_new = pd.read_csv('export-2025-11-25.csv')
print(f'=== NEW EXPORT (2025-11-25) ===')
print(f'Total policies: {len(df_new)}')
print(f'Policies with URLs: {df_new["Document URL"].notna().sum()}')
print(f'Unique Overton IDs: {df_new["Overton id"].nunique()}')

# Load the log
log = pd.read_csv('download_log.csv')
print(f'\n=== DOWNLOAD LOG ===')
print(f'Total log entries: {len(log)}')
print(f'Unique Overton IDs in log: {log["Overton_ID"].nunique()}')

# Check downloaded files
if os.path.exists('downloaded_policies'):
    files = os.listdir('downloaded_policies')
    print(f'\n=== DOWNLOADED FILES ===')
    print(f'Total files: {len(files)}')
    
    # Extract unique IDs from filenames
    file_ids = set()
    for f in files:
        file_id = f.split('.')[0]
        file_ids.add(file_id)
    print(f'Unique file IDs: {len(file_ids)}')

# Check if log has entries from old export
print(f'\n=== ANALYZING LOG DATES ===')
log['Timestamp'] = pd.to_datetime(log['Timestamp'])
print(log.groupby(log['Timestamp'].dt.date)['Overton_ID'].count().sort_index())

