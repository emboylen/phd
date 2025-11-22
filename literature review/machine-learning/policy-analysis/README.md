# Policy Analysis - Biofuel Policy Documents

This directory contains scripts and data for collecting and analyzing biofuel-related policy documents to understand regulatory frameworks, barriers, and support mechanisms.

## Overview

Policy analysis examines government policies, regulations, and frameworks related to biofuel production and sustainability. This analysis helps identify:
- Policy barriers to commercialization
- Regulatory support mechanisms
- Geographic variation in policy approaches
- Gaps between policy and technology readiness

## Research Context

Part of PhD research investigating: **Why is algae not being used for biofuel despite its promise?**

Policy analysis addresses the regulatory and governance dimension:
- What policies support or hinder algae biofuel development?
- How do policy frameworks vary across countries?
- Are there gaps in policy coverage?
- What policy themes emerge from the corpus?

## Contents

### Scripts
**`bulk_policy_downloader.py`**
- Automated policy document downloader
- Downloads from Overton policy database export
- Handles PDF, HTML, and text formats
- Includes rate limiting and error handling

### Data Files

**Input:**
- **`policies-export-2025-11-19.csv`** - Overton database export with policy metadata and URLs

**Outputs:**
- **`download_log.csv`** - Detailed log of all download attempts
- **`failed_downloads.csv`** - Records of failed downloads
- **`download_analysis_report.txt`** - Summary statistics and analysis
- **`failure_detailed_breakdown.txt`** - Detailed failure analysis

**Downloaded Documents:**
- **`downloaded_policies/`** - Directory containing all successfully downloaded policy documents
  - PDFs, HTML files, and text documents
  - Named by Overton ID for easy reference

## Policy Document Collection

### Data Source

**Overton Policy Database:**
- Academic policy document database
- Tracks policy documents citing research
- Global coverage of government policies, white papers, guidelines
- URL: https://www.overton.io/

### Download Statistics

Based on last download (November 19, 2025):
- **Total policy documents identified:** [Check CSV file]
- **Successfully downloaded:** [Check download_log.csv]
- **Failed downloads:** [Check failed_downloads.csv]
- **Formats:** PDF, HTML, plain text

## Usage

### 1. Downloading Policy Documents

```bash
cd machine-learning/policy-analysis
python bulk_policy_downloader.py
```

**What the script does:**
1. Reads `policies-export-2025-11-19.csv`
2. Extracts document URLs and metadata
3. Downloads each document with appropriate extension
4. Logs all attempts (success/failure)
5. Implements rate limiting to respect servers
6. Skips already downloaded documents
7. Generates summary reports

**Configuration (in script):**
```python
CSV_FILE = "policies-export-2025-11-19.csv"
OUTPUT_DIR = "downloaded_policies"
LOG_FILE = "download_log.csv"
HEADERS = {'User-Agent': 'Mozilla/5.0...'}  # Browser user agent
```

**Rate Limiting:**
- Random delay between 0.5-1.5 seconds per download
- Prevents server blocking
- Can be adjusted if needed

### 2. Reviewing Download Results

**Check download log:**
```powershell
# View successful downloads
Import-Csv download_log.csv | Where-Object {$_.Status -eq 'SUCCESS'}

# View failed downloads
Import-Csv download_log.csv | Where-Object {$_.Status -eq 'FAILED'}

# Count by status
Import-Csv download_log.csv | Group-Object Status
```

**Check downloaded files:**
```powershell
# Count files by type
Get-ChildItem downloaded_policies | Group-Object Extension

# List largest files
Get-ChildItem downloaded_policies | Sort-Object Length -Descending | Select-Object -First 10

# Check total size
(Get-ChildItem downloaded_policies | Measure-Object -Property Length -Sum).Sum / 1MB
```

### 3. Analyzing Policies (Future)

Once documents are downloaded, analyze using BERTopic:

**Planned workflow:**
1. Extract text from downloaded documents (PDF/HTML/TXT)
2. Preprocess policy text (similar to scientific papers)
3. Run BERTopic topic modeling
4. Identify policy themes and frameworks
5. Compare with scientific literature topics
6. Analyze geographic and temporal patterns

**Script to be created:**
- `analyze_policies.py` - BERTopic analysis on policy corpus
- Integration with literature and patent analyses

## Download Log Structure

**Columns in `download_log.csv`:**

| Column | Description |
|--------|-------------|
| `Timestamp` | When download was attempted |
| `Index` | Row number in source CSV |
| `Overton_ID` | Unique Overton document ID |
| `URL` | Document URL |
| `Status` | SUCCESS, FAILED, or SKIPPED |
| `Content_Type` | MIME type (application/pdf, text/html, etc.) |
| `File_Saved` | Filename of saved document |
| `Message` | Success confirmation or error message |

## Failure Analysis

### Common Failure Reasons

**1. Access Restrictions (403 Forbidden, 401 Unauthorized)**
- Government servers blocking automated access
- Authentication required
- Geographic restrictions

**2. Broken Links (404 Not Found)**
- Document moved or removed
- Outdated URL in Overton database
- Policy archived or withdrawn

**3. Server Issues (500 Internal Server Error, Timeout)**
- Temporary server problems
- Overloaded servers
- Network connectivity issues

**4. Format Issues**
- Unexpected content type
- Corrupted files
- Dynamic content requiring JavaScript

### Handling Failures

**Automatic handling:**
- Script logs all failures
- Continues with remaining documents
- Generates detailed failure report

**Manual recovery:**
1. Review `failed_downloads.csv`
2. Identify patterns in failures
3. For high-priority documents:
   - Manual download via web browser
   - Check if URL still valid
   - Use alternative sources if available

## Dependencies

```bash
pip install pandas requests
```

**Standard library modules:**
- `os` - File operations
- `time` - Rate limiting delays
- `csv` - Log file handling
- `datetime` - Timestamps
- `urllib.parse` - URL parsing
- `random` - Random delay generation

## Analysis Pipeline (Planned)

### Phase 1: Collection ✅
- [x] Export policy metadata from Overton
- [x] Create bulk download script
- [x] Download policy documents
- [x] Log and error handling
- [x] Generate summary reports

### Phase 2: Text Extraction (Pending)
- [ ] Extract text from PDFs
- [ ] Parse HTML documents
- [ ] Handle multiple formats
- [ ] Clean and normalize text
- [ ] Create unified corpus CSV

### Phase 3: Topic Modeling (Pending)
- [ ] Preprocess policy text
- [ ] Run BERTopic analysis
- [ ] Identify policy themes
- [ ] Classify documents by topic
- [ ] Generate visualizations

### Phase 4: Integration (Pending)
- [ ] Compare policy topics with literature topics
- [ ] Geographic analysis of policy approaches
- [ ] Temporal trends in policy focus
- [ ] Identify policy-research gaps
- [ ] Synthesize findings for thesis

## File Naming Convention

Downloaded files are named using Overton IDs:
- Format: `{Overton_ID}.{extension}`
- Example: `8123456.pdf`, `9234567.html`
- Ensures uniqueness
- Easy cross-reference with CSV metadata

**Looking up document details:**
```python
import pandas as pd

# Load metadata
policies = pd.read_csv('policies-export-2025-11-19.csv')

# Find document by ID
doc_id = '8123456'
doc_info = policies[policies['Overton id'] == doc_id]
print(doc_info['Title'].values[0])
print(doc_info['Document URL'].values[0])
```

## Best Practices

### When Running Downloader

**Before running:**
1. Check available disk space (policies can be large)
2. Ensure stable internet connection
3. Review rate limiting settings
4. Backup existing downloaded files if re-running

**During execution:**
- Script can run for hours depending on corpus size
- Safe to interrupt (Ctrl+C) - will resume on next run
- Monitor download_log.csv for progress

**After completion:**
- Review failure report
- Check file integrity (corrupted downloads)
- Validate content types match expectations

### Data Management

**Storage:**
- Policy documents can be 100s of MB to GBs
- Consider compression for archival:
  ```powershell
  Compress-Archive -Path downloaded_policies -DestinationPath policies_backup.zip
  ```

**Version control:**
- Do NOT commit large PDF/HTML files to Git
- Add to `.gitignore`:
  ```
  downloaded_policies/
  *.pdf
  *.html
  ```
- Keep metadata CSVs and logs in version control

## Ethical & Legal Considerations

**Copyright:**
- Most government policy documents are public domain
- Some may have copyright restrictions
- Verify usage rights for your jurisdiction

**Access:**
- Respect robots.txt and terms of service
- Use appropriate rate limiting
- Don't overwhelm servers

**Data Privacy:**
- Policy documents generally don't contain personal data
- Review content before sharing or publishing
- Comply with institutional data policies

## Troubleshooting

### Script won't run

**Error: "No such file 'policies-export-2025-11-19.csv'"**
```powershell
# Check file exists
Test-Path policies-export-2025-11-19.csv

# List all CSV files
Get-ChildItem *.csv
```

### All downloads failing

**Check internet connection:**
```powershell
Test-Connection google.com
```

**Test a single URL:**
```python
import requests
url = "https://example.com/policy.pdf"
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0...'})
print(response.status_code)
```

### Slow download speed

- Increase delay between requests (reduce server load)
- Check network bandwidth
- Consider running during off-peak hours

### Disk space issues

**Check available space:**
```powershell
Get-PSDrive C | Select-Object Used,Free
```

**Clean up if needed:**
```powershell
# Remove failed/corrupted downloads
Get-ChildItem downloaded_policies | Where-Object {$_.Length -eq 0} | Remove-Item
```

## Integration with BERTopic

Once text extraction is complete, policy documents will be analyzed using the same BERTopic pipeline as scientific papers:

**Comparison analysis:**
1. Topics in scientific literature
2. Topics in policy documents  
3. Topics in patent abstracts
4. Cross-cutting themes and gaps

**Expected insights:**
- Are policy priorities aligned with research focus?
- Are there policy gaps for key technologies?
- How do different countries approach regulation?
- What barriers emerge from policy analysis?

## Future Enhancements

**Planned features:**
1. Automatic text extraction script
2. Metadata enrichment (countries, dates, types)
3. Geographic clustering of policies
4. Temporal trend analysis
5. Citation network (policies citing research)
6. Integration with Overton API for updates

## References

**Overton Policy Database:**
- https://www.overton.io/
- Database of policy documents citing research
- Global coverage, regularly updated

**Related Tools:**
- PyMuPDF - PDF text extraction
- BeautifulSoup - HTML parsing
- BERTopic - Topic modeling

## Contact

For questions about policy data collection or analysis:
- See main project README
- Check Overton documentation
- Review error logs for specific issues

---

**Last Updated**: November 22, 2025  
**Data Source**: Overton Policy Database  
**Download Date**: November 19, 2025  
**Status**: Documents downloaded, text extraction and analysis pending

