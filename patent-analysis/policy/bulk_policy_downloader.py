import pandas as pd
import requests
import os
import time
import random
from urllib.parse import urlparse

# --- CONFIGURATION ---
CSV_FILE = "policies-export-2025-11-19.csv"
OUTPUT_DIR = "downloaded_policies"
# Fake browser user-agent to prevent immediate 403 Forbidden errors
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def setup_environment():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")

def download_pdf(url, filename):
    try:
        # 1. Request the file
        response = requests.get(url, headers=HEADERS, timeout=15, stream=True)
        response.raise_for_status() # Raise error for 404/403/500

        # 2. Check if content type is actually PDF (sometimes links redirect to HTML login pages)
        content_type = response.headers.get('Content-Type', '').lower()
        if 'pdf' not in content_type and 'application/octet-stream' not in content_type:
            # Warning: You might be downloading a webpage instead of a PDF
            print(f"  [!] Warning: Content-Type is {content_type}, not PDF. Skipping.")
            return False

        # 3. Write to file
        file_path = os.path.join(OUTPUT_DIR, filename)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True

    except requests.exceptions.RequestException as e:
        print(f"  [x] Failed: {e}")
        return False

def main():
    setup_environment()
    
    # Load CSV
    print("Loading CSV...")
    df = pd.read_csv(CSV_FILE)
    
    # Filter for rows that actually have a URL
    df = df[df['Document URL'].notna()]
    total = len(df)
    print(f"Found {total} documents with URLs to attempt.")

    success_count = 0
    failure_count = 0

    # Iterate
    for index, row in df.iterrows():
        overton_id = row['Overton id']
        url = row['Document URL']
        
        # Create a safe filename
        # We use the Overton ID because titles can have weird characters
        filename = f"{overton_id}.pdf"
        
        # Skip if already downloaded
        if os.path.exists(os.path.join(OUTPUT_DIR, filename)):
            print(f"[{index+1}/{total}] Skipping {overton_id} (Already exists)")
            continue

        # Handle missing or non-string titles
        title = row['Title'] if isinstance(row['Title'], str) else str(overton_id)
        print(f"[{index+1}/{total}] Downloading: {title[:30]}...")
        
        if download_pdf(url, filename):
            success_count += 1
            print("  [v] Success")
        else:
            failure_count += 1
        
        # RATE LIMITING: Sleep between 0.5 and 1.5 seconds
        # This is crucial to stop servers from blocking your IP
        time.sleep(random.uniform(0.5, 1.5))

    print("-" * 30)
    print(f"Download Complete.")
    print(f"Success: {success_count}")
    print(f"Failed:  {failure_count}")
    print(f"Total:   {total}")

if __name__ == "__main__":
    main()