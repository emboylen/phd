import pandas as pd
import requests
import os
import time
import random
import csv
from datetime import datetime
from urllib.parse import urlparse

# --- CONFIGURATION ---
CSV_FILE = "policies-export-2025-11-19.csv"
OUTPUT_DIR = "downloaded_policies"
LOG_FILE = "download_log.csv"
# Fake browser user-agent to prevent immediate 403 Forbidden errors
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def setup_environment():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")
    
    # Create log file with headers if it doesn't exist
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'Index', 'Overton_ID', 'URL', 'Status', 'Content_Type', 'File_Saved', 'Message'])
        print(f"Created log file: {LOG_FILE}")

def download_document(url, base_filename):
    """
    Downloads document (PDF or HTML/text) and returns (success, content_type, saved_filename, message)
    """
    try:
        # 1. Request the file
        response = requests.get(url, headers=HEADERS, timeout=15, stream=True)
        response.raise_for_status() # Raise error for 404/403/500

        # 2. Check content type and determine file extension
        content_type = response.headers.get('Content-Type', '').lower()
        
        # Determine appropriate file extension
        if 'pdf' in content_type or 'application/octet-stream' in content_type:
            extension = '.pdf'
            mode = 'wb'
        elif 'html' in content_type:
            extension = '.html'
            mode = 'wb'
        elif 'text' in content_type or 'plain' in content_type:
            extension = '.txt'
            mode = 'wb'
        else:
            # Try to download anyway, default to .html
            extension = '.html'
            mode = 'wb'

        # 3. Write to file
        filename = base_filename.replace('.pdf', extension)
        file_path = os.path.join(OUTPUT_DIR, filename)
        with open(file_path, mode) as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return True, content_type, filename, "Success"

    except requests.exceptions.RequestException as e:
        return False, None, None, str(e)

def log_attempt(index, overton_id, url, status, content_type, file_saved, message):
    """Log the download attempt to CSV"""
    with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            index,
            overton_id,
            url,
            status,
            content_type or 'N/A',
            file_saved or 'N/A',
            message
        ])

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
    skipped_count = 0

    # Iterate
    for index, row in df.iterrows():
        overton_id = row['Overton id']
        url = row['Document URL']
        
        # Create a safe filename base (will add appropriate extension)
        filename_base = f"{overton_id}.pdf"
        
        # Check if already downloaded (any extension)
        existing_files = [f for f in os.listdir(OUTPUT_DIR) if f.startswith(overton_id + '.')]
        if existing_files:
            print(f"[{index+1}/{total}] Skipping {overton_id} (Already exists: {existing_files[0]})")
            log_attempt(index+1, overton_id, url, 'SKIPPED', None, existing_files[0], 'Already downloaded')
            skipped_count += 1
            continue

        # Handle missing or non-string titles
        title = row['Title'] if isinstance(row['Title'], str) else str(overton_id)
        # Handle Unicode characters that can't be displayed in Windows console
        safe_title = title[:30].encode('ascii', 'replace').decode('ascii')
        print(f"[{index+1}/{total}] Downloading: {safe_title}...")
        
        success, content_type, saved_file, message = download_document(url, filename_base)
        
        if success:
            success_count += 1
            print(f"  [v] Success - Saved as {saved_file}")
            log_attempt(index+1, overton_id, url, 'SUCCESS', content_type, saved_file, message)
        else:
            failure_count += 1
            print(f"  [x] Failed: {message}")
            log_attempt(index+1, overton_id, url, 'FAILED', content_type, saved_file, message)
        
        # RATE LIMITING: Sleep between 0.5 and 1.5 seconds
        # This is crucial to stop servers from blocking your IP
        time.sleep(random.uniform(0.5, 1.5))

    print("-" * 30)
    print(f"Download Complete.")
    print(f"Success:  {success_count}")
    print(f"Failed:   {failure_count}")
    print(f"Skipped:  {skipped_count}")
    print(f"Total:    {total}")
    print(f"Log saved to: {LOG_FILE}")

if __name__ == "__main__":
    main()