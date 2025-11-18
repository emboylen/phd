# Duplicate Paper Removed

## Summary

During the analysis, we identified **1 duplicate paper** that appeared in the raw data with two different DOIs:

### Paper Details

**Title:** "Sustainable algal biorefinery: A review on current perspective on technical maturity..."

**Issue:** This paper existed in two forms:

1. ✅ **Correct entry** (in screened list with `included=TRUE`):
   - DOI: `10.1016/j.jenvman.2024.122208`
   
2. ❌ **Duplicate entry** (in raw data with incorrect/different DOI):
   - DOI: `10.1016/j.rser.2018.05.052`

## Resolution

The duplicate entry with DOI `10.1016/j.rser.2018.05.052` has been **automatically removed** during data wrangling.

This is implemented in `wrangle_data.R` (lines 305-322) to ensure reproducibility.

## Final Dataset

- **Expected papers** (from screened list with `included=TRUE`): **222**
- **Final filtered dataset**: **222** ✓
- **Match rate**: **100%**

## Technical Details

The duplicate was likely caused by:
- Database indexing errors
- Preprint vs. published version with different DOIs
- Journal correction/erratum scenario

The filtering logic ensures that only the correct version (matching the screened list DOI) is retained in the analysis.

---

**Date removed:** 2025-11-18  
**Updated by:** Automated analysis workflow

