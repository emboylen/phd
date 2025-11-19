import pandas as pd
import os

# Find the new report
report_files = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if 'BiblioshinyReport-2025-11-19' in file and file.endswith('.xlsx'):
            report_files.append(os.path.join(root, file))

print("Found Biblioshiny reports:")
for f in report_files:
    stat = os.stat(f)
    print(f"  {f} - Modified: {pd.Timestamp.fromtimestamp(stat.st_mtime)}")

if report_files:
    # Use the most recently modified
    latest = max(report_files, key=lambda x: os.stat(x).st_mtime)
    print(f"\nUsing: {latest}")
    
    xl = pd.ExcelFile(latest, engine='openpyxl')
    print(f"\nSheets: {len(xl.sheet_names)}")
    
    # Check MainInfo to verify document count
    main_info = pd.read_excel(xl, sheet_name='MainInfo')
    print("\nMainInfo preview:")
    print(main_info.head(10).to_string())

