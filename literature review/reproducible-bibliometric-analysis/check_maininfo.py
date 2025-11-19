import pandas as pd

ref = pd.ExcelFile('output/BiblioshinyReport-2025-11-19.xlsx')
main_info = pd.read_excel(ref, sheet_name='MainInfo')

print("Reference MainInfo structure:")
print(main_info.to_string())
print(f"\nShape: {main_info.shape}")

