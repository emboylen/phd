import os
from pathlib import Path
from openai import OpenAI
import PyPDF2

# Configuration
OPENWEBUI_API_KEY = os.environ.get("OPENWEBUI_API_KEY")
OPENWEBUI_BASE_URL = os.environ.get("OPENWEBUI_BASE_URL", "http://localhost:8080/api")
OPENWEBUI_MODEL = os.environ.get("OPENWEBUI_MODEL", "gpt-5")

client = OpenAI(
    api_key=OPENWEBUI_API_KEY,
    base_url=OPENWEBUI_BASE_URL
)

PROMPT = """Extract from this paper in SHORT NOTE-TAKING FORMAT for a PhD lit review on microalgae biofuel sustainability.

Output ONLY 3 sections:
1) KEY FINDINGS - 3-5 bullet points max
2) GAPS - 2-4 bullet points max  
3) OPPORTUNITIES - 2-4 bullet points max

Keep each bullet to ONE line. No background/methods. High-level only. Be ruthlessly brief."""

def extract_text_from_pdf(pdf_path):
    """Extract text content from PDF file."""
    text = []
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        print(f"Total pages: {len(pdf_reader.pages)}")
        for page_num, page in enumerate(pdf_reader.pages[:3]):  # Just first 3 pages for testing
            try:
                page_text = page.extract_text()
                if page_text:
                    text.append(f"--- Page {page_num + 1} ---\n{page_text}")
                    print(f"Extracted page {page_num + 1}: {len(page_text)} characters")
            except Exception as e:
                print(f"Error extracting page {page_num + 1}: {e}")
    
    full_text = "\n\n".join(text)
    return full_text

# Find first PDF
pdf_files = list(Path("included-papers").glob("*.pdf"))
if not pdf_files:
    print("No PDFs found!")
    exit(1)

test_pdf = pdf_files[0]
print(f"Testing with: {test_pdf.name}\n")

# Extract text
print("=== EXTRACTING TEXT ===")
pdf_text = extract_text_from_pdf(test_pdf)
print(f"\nTotal extracted text length: {len(pdf_text)} characters")
print(f"\nFirst 500 characters of extracted text:")
print(pdf_text[:500])
print("\n")

# Test API call
print("=== TESTING API CALL ===")
try:
    response = client.chat.completions.create(
        model=OPENWEBUI_MODEL,
        messages=[
            {
                "role": "user",
                "content": f"{PROMPT}\n\n--- PDF CONTENT ---\n{pdf_text}"
            }
        ],
        temperature=0.7,
        max_tokens=16384  # High limit for GPT-5 reasoning + output tokens
    )
    
    print(f"Response object: {response}")
    print(f"\nResponse choices: {response.choices}")
    print(f"\nMessage content type: {type(response.choices[0].message.content)}")
    print(f"Message content length: {len(str(response.choices[0].message.content))}")
    print(f"\n=== ACTUAL RESPONSE ===")
    print(response.choices[0].message.content)
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

