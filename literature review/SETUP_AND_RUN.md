# PDF Analysis Script Setup

This script processes PDF papers in the `included-papers` directory using your OpenWebUI instance and generates individual text files for each paper that you can print and read.

## Setup

### 1. Install Python Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Get Your OpenWebUI API Key

1. Open your OpenWebUI instance
2. Go to Settings → Account
3. Create or copy your API key

### 3. Set Environment Variables

**Required:**

**PowerShell:**
```powershell
$env:OPENWEBUI_API_KEY='your-api-key-here'
```

**CMD:**
```cmd
set OPENWEBUI_API_KEY=your-api-key-here
```

**Optional (if defaults don't work):**

```powershell
# Set the base URL if your OpenWebUI is not at localhost:8080
$env:OPENWEBUI_BASE_URL='http://localhost:8080/api'

# Set the model name if different from default
$env:OPENWEBUI_MODEL='llama3.2-vision'
```

## Running the Script

```powershell
python process_papers.py
```

## What It Does

1. Scans the `included-papers` folder for all PDF files
2. Extracts text from each PDF
3. Sends the text to your OpenWebUI instance with your specific prompt
4. Creates individual `.txt` files in the `paper-analyses` folder
5. Each output file includes:
   - The paper filename
   - Analysis date/time
   - AI analysis (key findings, gaps, opportunities)
   - Space for handwritten notes at the bottom

## Output

- All analyses are saved to: `paper-analyses/`
- Each file is named: `[original-pdf-name]_analysis.txt`
- Files are formatted for easy printing and reading

## Cost Estimate

- Claude 3.5 Sonnet: ~$3 per 1M input tokens, ~$15 per 1M output tokens
- Typical academic paper (~20 pages): ~$0.15-0.30 per analysis
- For 20 papers: ~$3-6 total

## Troubleshooting

**"No PDF files found"**: Make sure PDFs are in `included-papers/` folder

**"ANTHROPIC_API_KEY not set"**: The environment variable is only set for the current terminal session. Run the `$env:ANTHROPIC_API_KEY='...'` command again in the same terminal before running the script.

**API errors**: Check your API key is valid and has sufficient credits at https://console.anthropic.com/

