# Archive Directory

This directory contains old versions, development scripts, temporary fix files, and historical documentation. These files are **not needed for normal operation** but are preserved for reference.

## 📁 Contents

### Old Script Versions

**`refined-topic-model.py.backup`**
- Backup of main script before major changes
- Created: 2025-11-15
- Purpose: Safety copy before Windows multiprocessing fixes

**`refined-topic-model_WORKING.py`**
- Working version from intermediate development stage
- Purpose: Checkpoint before implementing final optimizations

**`advanced-ML.py`**
- Earlier/alternative implementation
- Status: Legacy, replaced by refined version

### Temporary Fix Scripts

These scripts were created to resolve specific issues and are no longer needed:

**`create_fixed_file.py`**
- Purpose: Attempted to fix indentation issues
- Result: Replaced by manual fixes
- Status: Obsolete

**`final_fix.py`**
- Purpose: Final attempt to fix multiprocessing guard indentation
- Result: Succeeded, changes merged into main script
- Status: Obsolete

**`rebuild.py`**
- Purpose: Reconstruct clean version of main script
- Result: Not used, manual approach taken
- Status: Obsolete

**`reconstruct_clean.py`**
- Purpose: Another attempt at automated indentation fixing
- Result: Not used
- Status: Obsolete

**`test_graph_fix.py`**
- Purpose: Test JSON serialization fix for knowledge graph
- Result: Fix validated and applied to main script
- Status: Obsolete

### Historical Documentation

**`CRITICAL_FIXES_SUMMARY.md`**
- Documents all critical fixes applied to the pipeline
- Covers: Model persistence, memory optimization, validation, logging
- Status: Historical reference

**`GRAPH_FIX_APPLIED.md`**
- Documents fix for JSON serialization issue in knowledge graph
- Covers: NumPy float32 → Python float conversion
- Status: Historical reference

**`QUICK_REFERENCE.md`**
- Quick troubleshooting guide
- Status: Merged into main README.md

**`RUN_CONFIG_UPDATES.md`**
- Documents configuration changes for k=50 and n-gram improvements
- Status: Historical reference

## 🗂️ Why Keep These?

### Reference Value
- Understanding what problems were solved
- Learning from development process
- Tracking evolution of the codebase

### Recovery
- If new changes break something, can reference old working versions
- Compare approaches that were tried
- Restore specific fixes if needed

### Documentation
- Historical record of issues encountered
- Solutions that worked (and didn't work)
- Context for future development

## 🗑️ What Can Be Deleted?

### Safely Deletable (Low Value)
- `create_fixed_file.py` - Failed approach
- `rebuild.py` - Never used successfully
- `reconstruct_clean.py` - Failed approach
- `test_graph_fix.py` - Fix already applied

**Impact if deleted:** None (fixes are already in main script)

### Keep for Reference (Medium Value)
- `final_fix.py` - Shows successful multiprocessing fix approach
- Historical documentation (*.md files) - Context for decisions made

**Impact if deleted:** Loss of historical context, harder to understand why certain decisions were made

### Keep for Safety (High Value)
- `refined-topic-model.py.backup` - Last known good version
- `refined-topic-model_WORKING.py` - Intermediate checkpoint
- `advanced-ML.py` - Alternative implementation

**Impact if deleted:** No safety net if main script gets corrupted

## 📋 File Summary

| File | Type | Size | Keep? | Reason |
|------|------|------|-------|--------|
| `refined-topic-model.py.backup` | Backup | ~30 KB | ✅ Yes | Safety copy |
| `refined-topic-model_WORKING.py` | Backup | ~30 KB | ✅ Yes | Working checkpoint |
| `advanced-ML.py` | Legacy | ~20 KB | ⚠️ Maybe | Historical |
| `create_fixed_file.py` | Failed Fix | ~2 KB | ❌ No | Not useful |
| `final_fix.py` | Successful Fix | ~3 KB | ⚠️ Maybe | Reference |
| `rebuild.py` | Failed Fix | ~2 KB | ❌ No | Not useful |
| `reconstruct_clean.py` | Failed Fix | ~3 KB | ❌ No | Not useful |
| `test_graph_fix.py` | Test Script | ~2 KB | ❌ No | Fix applied |
| `CRITICAL_FIXES_SUMMARY.md` | Docs | ~5 KB | ✅ Yes | Important context |
| `GRAPH_FIX_APPLIED.md` | Docs | ~3 KB | ⚠️ Maybe | Reference |
| `QUICK_REFERENCE.md` | Docs | ~4 KB | ❌ No | Merged to main README |
| `RUN_CONFIG_UPDATES.md` | Docs | ~3 KB | ⚠️ Maybe | Reference |

**Legend:**
- ✅ **Keep** - Important for safety or reference
- ⚠️ **Maybe** - Useful but not critical
- ❌ **Delete** - Safe to remove

## 🧹 Cleanup Recommendations

### Minimal Cleanup (Recommended)
Remove obviously failed/duplicate files:
```powershell
cd archive
Remove-Item create_fixed_file.py
Remove-Item rebuild.py
Remove-Item reconstruct_clean.py
Remove-Item test_graph_fix.py
Remove-Item QUICK_REFERENCE.md  # Already in main README
```

### Moderate Cleanup
Keep only backups and critical docs:
```powershell
cd archive
# Keep: *.backup, *_WORKING.py, CRITICAL_FIXES_SUMMARY.md
# Delete: Everything else
```

### Full Cleanup (Not Recommended)
Only if absolutely certain and disk space is critical:
```powershell
# Create compressed archive first!
Compress-Archive -Path archive -DestinationPath archive_20251117.zip

# Then delete all
Remove-Item archive/* -Recurse
```

## 🔄 Adding to Archive

When creating new backups or archiving files:

```powershell
# Backup current script before major changes
Copy-Item refined-topic-model.py archive/refined-topic-model_$(Get-Date -Format 'yyyyMMdd_HHmmss').py

# Move old outputs to archive
Move-Item outputs/old_results.html archive/

# Create dated archive
Compress-Archive -Path model_checkpoints/old_models* -DestinationPath archive/models_20251117.zip
```

## 📚 Historical Issues Solved

### 1. Windows Multiprocessing Error
**Problem:** `RuntimeError: An attempt has been made to start a new process...`

**Attempted Fixes:**
- `create_fixed_file.py` - Failed (indentation issues)
- `rebuild.py` - Failed (couldn't parse complex structure)
- `reconstruct_clean.py` - Failed (similar issues)
- `final_fix.py` - **Succeeded** (added `if __name__ == '__main__':`)

**Final Solution:**
- Added `if __name__ == '__main__':` guard
- Set `processes=1` in CoherenceModel
- Added `freeze_support()`

**Documented in:** `CRITICAL_FIXES_SUMMARY.md`

### 2. JSON Serialization in Knowledge Graph
**Problem:** `TypeError: Object of type float32 is not JSON serializable`

**Attempted Fix:**
- `test_graph_fix.py` - Tested solution

**Final Solution:**
- Convert NumPy float32 to Python float: `float(value)`
- Convert sizes to int: `int(value)`

**Documented in:** `GRAPH_FIX_APPLIED.md`

### 3. Model Hanging / No Progress Indication
**Problem:** Script appeared to hang at stage 5 (actually just slow)

**Solution:**
- Added `tqdm` progress bars
- Added verbose logging
- Added checkpoint saving

**Documented in:** `CRITICAL_FIXES_SUMMARY.md`

---

## 💡 Best Practices

1. **Always backup before major changes**
   ```powershell
   Copy-Item refined-topic-model.py "archive/refined-topic-model_$(Get-Date -Format 'yyyyMMdd_HHmmss').py"
   ```

2. **Document why you archived something**
   - Add comment in this README
   - Or include a note in the filename
   - Example: `old_model_k20_lowcoherence_20251116.zip`

3. **Compress large archives**
   ```powershell
   Compress-Archive -Path archive/large_models -DestinationPath archive/large_models.zip
   Remove-Item archive/large_models -Recurse
   ```

4. **Periodic cleanup**
   - Every few months, review archive
   - Delete obvious duplicates
   - Compress old files

---

**Last Updated:** 2025-11-17  
**Total Files:** 12  
**Recommended Action:** Minimal cleanup (remove 4-5 failed fix scripts)  
**Storage Used:** ~100 KB (trivial)

