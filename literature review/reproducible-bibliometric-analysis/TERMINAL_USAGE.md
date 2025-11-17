# Running from Terminal/Command Line

## ✅ Yes! You can run the analysis from terminal

### Windows PowerShell

```powershell
cd "D:\Github\phd\literature review\reproducible-bibliometric-analysis"
Rscript run_all.R
```

### Windows Command Prompt (CMD)

```cmd
cd "D:\Github\phd\literature review\reproducible-bibliometric-analysis"
Rscript run_all.R
```

---

## 🔧 If "Rscript" is not recognized

If you get an error that `Rscript` is not found, you have two options:

### Option 1: Use Full Path to Rscript

Find where R is installed (typically `C:\Program Files\R\R-x.x.x\bin\`) and use the full path:

```powershell
cd "D:\Github\phd\literature review\reproducible-bibliometric-analysis"
"C:\Program Files\R\R-4.4.0\bin\Rscript.exe" run_all.R
```

### Option 2: Add R to Your PATH (Permanent Solution)

1. Find your R installation directory (e.g., `C:\Program Files\R\R-4.4.0\bin`)
2. Add it to your Windows PATH:
   - Press `Win + X` → System → Advanced system settings
   - Click "Environment Variables"
   - Under "System variables", select "Path" → Edit
   - Click "New" and add: `C:\Program Files\R\R-4.4.0\bin`
   - Click OK, restart PowerShell

Then you can use `Rscript` directly.

---

## 📝 Running Individual Steps

### Step 1 Only: Data Wrangling
```powershell
cd "D:\Github\phd\literature review\reproducible-bibliometric-analysis"
Rscript wrangle_data.R
```

### Step 2 Only: Analysis (after data wrangling)
```powershell
cd "D:\Github\phd\literature review\reproducible-bibliometric-analysis"
Rscript run_bibliometric_analysis.R
```

### Complete Workflow: Both Steps
```powershell
cd "D:\Github\phd\literature review\reproducible-bibliometric-analysis"
Rscript run_all.R
```

---

## 📊 What You'll See

When running from terminal, you'll see progress messages like:

```
=============================================================================
COMPLETE BIBLIOMETRIC ANALYSIS WORKFLOW
=============================================================================

STEP 1/2: DATA WRANGLING
-----------------------------------------------------------------------------
[2025-11-17 10:30:15] Loading screened paper list...
[2025-11-17 10:30:16] Loaded 150 screened papers
[2025-11-17 10:30:16] Importing raw citation files...
[2025-11-17 10:30:20] Successfully imported 12 files
[2025-11-17 10:30:22] Matched 147 of 150 screened papers
[2025-11-17 10:30:22] Match rate: 98.0 %
✓ Data wrangling completed successfully

STEP 2/2: BIBLIOMETRIC ANALYSIS
-----------------------------------------------------------------------------
[2025-11-17 10:30:25] Running bibliometric analysis...
[2025-11-17 10:30:30] Exporting standard tables...
✓ Bibliometric analysis completed successfully

=============================================================================
WORKFLOW COMPLETED SUCCESSFULLY!
=============================================================================
```

---

## ⚡ Quick Command (Copy-Paste)

```powershell
cd "D:\Github\phd\literature review\reproducible-bibliometric-analysis"; Rscript run_all.R
```

Or if you need full path to Rscript:

```powershell
cd "D:\Github\phd\literature review\reproducible-bibliometric-analysis"; & "C:\Program Files\R\R-4.4.0\bin\Rscript.exe" run_all.R
```

*(Adjust R version number to match your installation)*

---

## 🎯 Benefits of Terminal Execution

✅ **No GUI needed** - Perfect for automation  
✅ **Server-friendly** - Can run on remote machines  
✅ **Scriptable** - Can integrate into larger workflows  
✅ **Background execution** - Terminal can stay open while processing  
✅ **Easy logging** - Redirect output to file:

```powershell
Rscript run_all.R > analysis_log.txt 2>&1
```

---

## 🔍 Finding Your R Installation

To find where R is installed:

```powershell
Get-ChildItem "C:\Program Files\R" -Recurse -Filter "Rscript.exe" | Select-Object FullName
```

Or check:
```powershell
where.exe Rscript
```

---

**Ready to run!** Just navigate to the directory and execute `Rscript run_all.R` ✨

