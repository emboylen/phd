# Included PDF Documents

This directory contains the corpus of PDF documents to be analyzed by the topic modeling pipeline.

## 📄 Current Corpus

**Document Count:** 223 scientific papers  
**Domain:** Microalgae and biofuel research  
**File Format:** PDF (text-extractable)

## 📁 Directory Structure

```
included/
├── paper1.pdf
├── paper2.pdf
├── paper3.pdf
├── ...
└── paper223.pdf
```

## 🔧 Requirements

### PDF Format Requirements

**✅ Valid PDFs:**
- Text-extractable PDFs (not scanned images without OCR)
- Research papers, articles, reports
- Any language (but stopwords are optimized for English)
- No minimum/maximum page count

**❌ Invalid PDFs:**
- Scanned documents without OCR text layer
- Password-protected PDFs
- Corrupted or unreadable files
- Image-only PDFs

### Testing PDF Readability

To check if a PDF is text-extractable:

**Method 1: Open in Adobe/browser**
- Open PDF
- Try to select text with cursor
- If you can select/copy text → ✅ Valid

**Method 2: Python test**
```python
import fitz  # PyMuPDF

pdf = fitz.open("included/your_paper.pdf")
text = pdf[0].get_text()
print(f"First page text length: {len(text)} characters")

if len(text) > 100:
    print("✅ PDF is readable")
else:
    print("❌ PDF may be image-only or corrupted")
```

## 📊 Expected Content

The topic modeling pipeline works best with:

- **Scientific papers** - Research articles, conference papers
- **Technical reports** - White papers, technical documentation
- **Academic content** - Dissertations, theses, reviews

**Minimum recommended corpus size:** 50-100 documents  
**Optimal corpus size:** 200-500 documents  
**Maximum tested:** 1000+ documents (may require increased RAM)

## 🔄 Adding New Documents

### To add new PDFs:

1. **Copy PDFs to this directory:**
```powershell
# Single file
Copy-Item "C:\Downloads\new_paper.pdf" included/

# Multiple files
Copy-Item "C:\Downloads\*.pdf" included/

# Entire folder
Copy-Item "C:\Downloads\papers\*" included/ -Recurse
```

2. **Verify document count:**
```powershell
(Get-ChildItem included/*.pdf).Count
```

3. **Run pipeline:**
```powershell
cd machine-learning
python run_bertopic_analysis.py
```

### To update corpus:

```powershell
# Remove old documents (optional)
Remove-Item machine-learning/included/*.pdf

# Add new documents
Copy-Item "new_corpus\*.pdf" machine-learning/included/

# Re-run pipeline
cd machine-learning
python run_bertopic_analysis.py
```

## 🔍 Validation

The pipeline automatically validates documents:

### Checks Performed:
1. **Folder exists** - Verifies `included/` directory exists
2. **Contains PDFs** - At least 1 PDF file found
3. **Readable content** - Each PDF has extractable text
4. **Minimum content** - Each document has >100 characters
5. **No empty documents** - All documents have substantial content

### Validation Errors:

**"No PDF files found"**
- Check folder path in script (line ~48)
- Verify PDFs are actually in `included/`
- Check file extensions are `.pdf` (case-sensitive on some systems)

**"Document X has insufficient content"**
- PDF may be image-only (needs OCR)
- PDF may be corrupted
- Remove or re-process that specific file

**"Vocabulary is empty after filtering"**
- Documents may be too similar (all using same words)
- Documents may be in non-English language
- Adjust stopword lists or filtering parameters

## 📈 Corpus Statistics

### Current Corpus (223 documents):

**Estimated metrics:**
- Total pages: ~2,000-3,000 pages
- Total words: ~1.5-2 million words
- Unique vocabulary: ~50,000-80,000 words
- Filtered vocabulary: ~11,000-15,000 words (after stopwords & frequency filtering)

**Processing time:**
- Text extraction: ~30 seconds - 1 minute
- Preprocessing: ~3-5 minutes
- Model training (k=2-50): ~2-4 hours

## 🔧 Changing Data Source

### To use a different folder:

**Edit `run_bertopic_analysis.py` (line ~49):**

```python
# Current (relative path)
PDF_FOLDER = "included"

# Change to absolute path (update to your system)
PDF_FOLDER = r"C:\Github\phd\literature review\machine-learning\included"

# Or different folder entirely
PDF_FOLDER = r"C:\My_Research\Papers"
```

### To use multiple folders:

The pipeline currently supports only one folder. To combine multiple folders:

```powershell
# Option 1: Copy all to included/
Copy-Item "C:\Folder1\*.pdf" included/
Copy-Item "C:\Folder2\*.pdf" included/

# Option 2: Use symbolic link (advanced)
New-Item -ItemType SymbolicLink -Path included/folder2 -Target "C:\Other_Folder"
```

## 🧹 Cleanup

### Remove temporary files:
```powershell
# Remove any non-PDF files
Get-ChildItem included/* -Exclude *.pdf | Remove-Item

# Remove zero-byte PDFs
Get-ChildItem included/*.pdf | Where-Object {$_.Length -eq 0} | Remove-Item
```

### Backup corpus:
```powershell
# Create backup before major changes
Compress-Archive -Path included -DestinationPath "corpus_backup_$(Get-Date -Format 'yyyyMMdd').zip"
```

## 📊 Document Metadata (Optional)

The pipeline extracts text only. Document metadata (title, author, year) can be extracted separately if needed:

```python
import fitz

pdf = fitz.open("included/paper.pdf")
metadata = pdf.metadata

print(f"Title: {metadata.get('title', 'Unknown')}")
print(f"Author: {metadata.get('author', 'Unknown')}")
print(f"Subject: {metadata.get('subject', 'Unknown')}")
print(f"Keywords: {metadata.get('keywords', 'Unknown')}")
```

**Note:** Metadata quality varies by PDF. Many PDFs have incomplete or missing metadata.

## 🐛 Troubleshooting

### "Permission denied" when copying files
**Solution:**
```powershell
# Run PowerShell as Administrator
# Or check file permissions
Get-Acl included
```

### Some PDFs not being processed
**Solution:**
```powershell
# Check which PDFs have content
python -c "
import fitz, os
for pdf in os.listdir('included'):
    if pdf.endswith('.pdf'):
        doc = fitz.open(f'included/{pdf}')
        text = ''.join(page.get_text() for page in doc)
        print(f'{pdf}: {len(text)} chars')
"
```

### "Out of memory" during extraction
**Solution:**
- Process PDFs in batches
- Increase system RAM
- Or modify script to process incrementally

### PDFs with strange characters
**Solution:**
- Usually not a problem (preprocessing handles it)
- If issues persist, check PDF encoding
- Consider re-exporting PDF from original source

---

## 📚 Data Privacy & Ethics

**Important considerations:**

1. **Copyright:** Ensure you have rights to process these documents
2. **Privacy:** Check documents don't contain sensitive/personal information
3. **Licensing:** Verify document licenses permit text mining
4. **Attribution:** Keep track of original sources for citation

**Recommendation:** Use open-access papers or papers you have institutional access to.

---

**Last Updated:** 2025-11-17  
**Document Count:** 223  
**Total Size:** ~500-800 MB  
**Domain:** Microalgae/biofuel research

