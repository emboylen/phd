# Patent Analysis - Microalgae Biofuel Technologies

This directory contains data and queries for analyzing patent activity in microalgae biofuel technologies using Google BigQuery's public patent dataset.

## Overview

Patent analysis helps identify:
- Technological innovation trends
- Key patent holders (companies, universities)
- Geographic distribution of R&D activity
- Technology maturity and commercial readiness
- Gaps between research and commercialization

## Research Context

Part of PhD research investigating: **Why is algae not being used for biofuel despite its promise?**

Patent analysis provides insights into:
- Commercial interest and investment
- Technology transfer from research to industry
- Barriers to commercialization
- Innovation hotspots and key players

## Contents

### Query File
**`big-query-patent-download.sql`**
- SQL query for Google BigQuery
- Searches Google Patents Public Data
- Filters for microalgae + biofuel related patents
- Date range: 2010-present
- Extracts: title, abstract, assignees, CPC codes, dates

### Data File
**`bq-results-20251119-051840-1763529534350.csv`**
- Results from BigQuery execution
- Contains patent metadata and full text
- Ready for topic modeling analysis

### Credentials
**`phd-patent-analysis-860d100de9d9.json`**
- Google Cloud service account credentials
- Required for BigQuery API access
- ⚠️ **Do not commit to public repositories**

## Query Details

### Search Criteria

**Organism keywords:**
- microalgae, algae, cyanobacteria, phytoplankton, seaweed

**Technology keywords:**
- biofuel, biodiesel, ethanol, biomass, lipid
- cultivation, harvesting, photobioreactor
- raceway pond, culture

**Time filter:**
- Publication date >= 2010-01-01

**Language:**
- English titles and abstracts only

### Fields Extracted

| Field | Description |
|-------|-------------|
| `publication_number` | Unique patent identifier |
| `title` | Patent title (English) |
| `abstract` | Patent abstract (English) |
| `publication_date` | Date patent was published |
| `filing_date` | Date patent was filed |
| `country_code` | Country of patent office |
| `assignees` | Companies/institutions owning patent |
| `cpc_codes` | Cooperative Patent Classification codes |

## Usage

### Running the Query

#### Option 1: BigQuery Console (Web Interface)

1. Go to [Google BigQuery Console](https://console.cloud.google.com/bigquery)
2. Create a new project or select existing project
3. Open `big-query-patent-download.sql`
4. Copy query into BigQuery editor
5. Click "Run" (check estimated data processed)
6. Export results as CSV

#### Option 2: Command Line (requires `bq` CLI)

```bash
# Authenticate
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Run query and save results
bq query --use_legacy_sql=false --format=csv \
  "$(cat big-query-patent-download.sql)" > patent_results.csv
```

#### Option 3: Python (using `google-cloud-bigquery`)

```python
from google.cloud import bigquery
import pandas as pd

# Initialize client
client = bigquery.Client.from_service_account_json(
    'phd-patent-analysis-860d100de9d9.json'
)

# Load query
with open('big-query-patent-download.sql', 'r') as f:
    query = f.read()

# Execute query
df = client.query(query).to_dataframe()

# Save results
df.to_csv('patent_results.csv', index=False)
print(f"Downloaded {len(df)} patents")
```

### Analyzing Results

Once patent data is downloaded, analyze using BERTopic:

```bash
# Move CSV to machine-learning directory
# Create a new script to load CSV instead of PDFs
# Run topic modeling on patent abstracts
```

**Future analysis script (to be created):**
- `analyze_patents.py` - Topic modeling on patent abstracts
- Integration with scientific literature topics
- Comparison of academic vs. commercial focus areas
- Geographic and temporal trend analysis

## Data Structure

### Expected Columns

```
publication_number  | Patent ID (e.g., US-20150218525-A1)
title              | Patent title
abstract           | Patent abstract (full text)
publication_date   | YYYYMMDD format
filing_date        | YYYYMMDD format
country_code       | Country code (US, CN, WO, etc.)
assignees          | Company/institution names (semicolon separated)
cpc_codes          | Classification codes (comma separated)
```

### Sample CPC Codes for Algae Biofuel

- **C12N 1/12** - Microorganisms for biofuel production
- **C12P 7/64** - Production of organic compounds (ethanol, etc.)
- **C10L 1/00** - Liquid fuels
- **C10L 1/02** - Biodiesel
- **Y02E 50/10** - Energy generation from biomass

## Analysis Plan

### Phase 1: Data Collection ✅
- [x] Create BigQuery SQL query
- [x] Execute query and download results
- [x] Validate data quality

### Phase 2: Topic Modeling (Pending)
- [ ] Preprocess patent abstracts
- [ ] Run BERTopic on patent corpus
- [ ] Identify technology themes
- [ ] Compare with scientific literature topics

### Phase 3: Trend Analysis (Pending)
- [ ] Temporal trends (filing/publication dates)
- [ ] Geographic analysis (country codes)
- [ ] Assignee analysis (corporate vs. academic)
- [ ] CPC code distribution

### Phase 4: Integration (Pending)
- [ ] Compare patent topics with literature topics
- [ ] Identify research-to-commercialization gaps
- [ ] Analyze patent-paper overlap
- [ ] Generate insights for PhD thesis

## Prerequisites

### For BigQuery Access

**Option A: Web Console (Easiest)**
- Google account
- Access to Google Cloud Console
- Basic SQL knowledge

**Option B: API/CLI**
```bash
pip install google-cloud-bigquery pandas
```

**Required credentials:**
- Service account JSON file (already included)
- Or personal Google account authentication

### For Patent Analysis

```bash
pip install pandas numpy bertopic sentence-transformers
```

## Cost Considerations

**BigQuery Pricing:**
- First 1 TB/month: FREE
- After 1 TB: $5 per TB

**Estimated data processed for this query:**
- ~10-50 GB (well within free tier)
- Typically processes in 1-5 seconds

**Tips to reduce costs:**
- Use `LIMIT` clause for testing
- Filter by date range to reduce dataset size
- Use cached results when possible

## Security Notes

⚠️ **Important: Credential Management**

The file `phd-patent-analysis-860d100de9d9.json` contains sensitive credentials.

**Best practices:**
1. Do NOT commit to public GitHub repositories
2. Add to `.gitignore`:
   ```
   *.json
   *credentials*
   ```
3. Rotate credentials periodically
4. Use environment variables for automation:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
   ```

## Troubleshooting

### "Permission denied" error
**Solution:**
- Verify service account has BigQuery access
- Check project billing is enabled
- Ensure correct credentials file path

### Query timeout or too slow
**Solution:**
- Add date range limits
- Use `LIMIT` for testing
- Break into smaller queries by year

### No results or very few results
**Solution:**
- Check search terms (too restrictive?)
- Verify date range
- Review `WHERE` clause logic
- Test with broader search first

### Invalid credentials
**Solution:**
- Re-download service account JSON
- Check file path is correct
- Verify project ID matches

## Next Steps

1. **Immediate:**
   - Review downloaded patent data
   - Validate quality and relevance
   - Check for duplicates

2. **Short-term:**
   - Create patent-specific BERTopic analysis script
   - Preprocess patent abstracts
   - Run topic modeling

3. **Integration:**
   - Compare patent topics with literature topics
   - Identify gaps between research and commercialization
   - Analyze geographic/institutional patterns

4. **Thesis:**
   - Synthesize findings
   - Generate visualizations
   - Write methodology section

## References

**Google Patents Public Data:**
- Dataset: `patents-public-data.patents.publications`
- Documentation: https://cloud.google.com/bigquery/public-data/patents
- Coverage: 90+ million patents worldwide

**Cooperative Patent Classification (CPC):**
- https://www.cooperativepatentclassification.org/

## Contact

For questions about this analysis or BigQuery setup:
- See main project README
- Check Google Cloud documentation
- Review BigQuery public data examples

---

**Last Updated**: November 22, 2025  
**Query Date**: November 19, 2025  
**Status**: Data collected, analysis pending  
**Dataset**: Google Patents Public Data (2010-present)

