import pandas as pd

files = [
    'data/filtered_data.xlsx',
    'data/filtered_data_biblioshiny_ready.xlsx'
]

for file in files:
    df = pd.read_excel(file)
    print(f"\n{file}:")
    print(f"  Records: {len(df)}")
    print(f"  Columns: {len(df.columns)}")
    if 'PY' in df.columns:
        print(f"  Years: {int(df['PY'].min())} to {int(df['PY'].max())}")
    if 'SO' in df.columns:
        print(f"  Unique sources: {df['SO'].nunique()}")

