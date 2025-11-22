import os
import base64
from pathlib import Path
from openai import OpenAI
from datetime import datetime
import PyPDF2

# Configuration - set these as environment variables
OPENWEBUI_API_KEY = os.environ.get("OPENWEBUI_API_KEY")
OPENWEBUI_BASE_URL = os.environ.get("OPENWEBUI_BASE_URL", "http://localhost:8080/api")  # Default OpenWebUI API endpoint
OPENWEBUI_MODEL = os.environ.get("OPENWEBUI_MODEL", "llama3.2-vision")  # Default model, change as needed

# Initialize OpenAI client pointing to OpenWebUI
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
        for page_num, page in enumerate(pdf_reader.pages):
            try:
                page_text = page.extract_text()
                if page_text:
                    text.append(f"--- Page {page_num + 1} ---\n{page_text}")
            except Exception as e:
                print(f"  ⚠ Warning: Could not extract page {page_num + 1}: {e}")
    
    return "\n\n".join(text)

def get_available_models():
    """Fetch available models from OpenWebUI."""
    try:
        models = client.models.list()
        return [model.id for model in models.data]
    except Exception as e:
        return None

def analyze_pdf(pdf_path):
    """Send PDF content to OpenWebUI and get analysis."""
    print(f"  → Extracting text from PDF...")
    
    pdf_text = extract_text_from_pdf(pdf_path)
    
    if not pdf_text.strip():
        raise Exception("Could not extract any text from PDF")
    
    print(f"  → Sending to OpenWebUI (model: {OPENWEBUI_MODEL})...")
    
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
        
        return response.choices[0].message.content
        
    except Exception as e:
        error_msg = str(e)
        if "Model not found" in error_msg or "404" in error_msg:
            available_models = get_available_models()
            if available_models:
                raise Exception(
                    f"Model '{OPENWEBUI_MODEL}' not found.\n"
                    f"  Available models: {', '.join(available_models)}\n"
                    f"  Set with: $env:OPENWEBUI_MODEL='model-name'"
                )
            else:
                raise Exception(
                    f"Model '{OPENWEBUI_MODEL}' not found.\n"
                    f"  Please check your OpenWebUI instance for available models.\n"
                    f"  Set with: $env:OPENWEBUI_MODEL='model-name'"
                )
        else:
            raise

def process_all_pdfs(input_dir, output_dir):
    """Process all PDFs in input directory and save results to output directory."""
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # Create output directory if it doesn't exist
    output_path.mkdir(exist_ok=True)
    
    # Find all PDF files
    pdf_files = sorted(input_path.glob("*.pdf"))
    
    if not pdf_files:
        print(f"❌ No PDF files found in {input_dir}")
        return
    
    # Verify model availability before processing
    print(f"Checking model availability...")
    available_models = get_available_models()
    if available_models:
        if OPENWEBUI_MODEL not in available_models:
            print(f"\n❌ Error: Model '{OPENWEBUI_MODEL}' not found on your OpenWebUI instance.")
            print(f"\nAvailable models:")
            for model in available_models:
                print(f"  - {model}")
            print(f"\nTo set the model, run:")
            print(f"  $env:OPENWEBUI_MODEL='model-name'")
            print(f"\nThen run the script again.")
            return
        else:
            print(f"✓ Model '{OPENWEBUI_MODEL}' is available\n")
    else:
        print(f"⚠ Warning: Could not verify model availability, proceeding anyway...\n")
    
    print(f"\n{'='*80}")
    print(f"Found {len(pdf_files)} PDF files to process")
    print(f"{'='*80}\n")
    
    # Process each PDF
    results = []
    for i, pdf_path in enumerate(pdf_files, 1):
        print(f"[{i}/{len(pdf_files)}] Processing: {pdf_path.name}")
        
        try:
            # Analyze with Claude
            analysis = analyze_pdf(pdf_path)
            
            # Create output filename
            output_filename = f"{pdf_path.stem}_analysis.txt"
            output_file_path = output_path / output_filename
            
            # Write to individual file
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(f"LITERATURE REVIEW ANALYSIS\n")
                f.write(f"{'='*80}\n")
                f.write(f"Source: {pdf_path.name}\n")
                f.write(f"Analyzed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"{'='*80}\n\n")
                f.write(analysis)
                f.write("\n\n")
                f.write(f"{'='*80}\n")
                f.write("Notes:\n")
                f.write("\n" * 10)  # Space for handwritten notes when printed
            
            print(f"  ✓ Saved to: {output_filename}\n")
            results.append((pdf_path.name, output_filename, "Success"))
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"  ✗ Failed: {error_msg}\n")
            results.append((pdf_path.name, None, error_msg))
    
    # Print summary
    print(f"\n{'='*80}")
    print("PROCESSING COMPLETE")
    print(f"{'='*80}")
    print(f"\nSuccessfully processed: {sum(1 for r in results if r[2] == 'Success')}/{len(results)}")
    print(f"Output location: {output_path.absolute()}")
    print("\nResults:")
    for pdf_name, output_name, status in results:
        if status == "Success":
            print(f"  ✓ {pdf_name} → {output_name}")
        else:
            print(f"  ✗ {pdf_name} → {status}")
    print(f"\n{'='*80}\n")

if __name__ == "__main__":
    # Configuration
    INPUT_DIR = "included-papers"
    OUTPUT_DIR = "paper-analyses"
    
    # Check for API key
    if not os.environ.get("OPENWEBUI_API_KEY"):
        print("❌ Error: OPENWEBUI_API_KEY environment variable not set")
        print("\nTo set it:")
        print("  Windows PowerShell: $env:OPENWEBUI_API_KEY='your-api-key-here'")
        print("  Windows CMD:        set OPENWEBUI_API_KEY=your-api-key-here")
        print("  Linux/Mac:          export OPENWEBUI_API_KEY='your-api-key-here'")
        print("\nOptional configurations:")
        print(f"  OPENWEBUI_BASE_URL: {OPENWEBUI_BASE_URL}")
        print(f"  OPENWEBUI_MODEL: {OPENWEBUI_MODEL}")
        exit(1)
    
    # Process all PDFs
    process_all_pdfs(INPUT_DIR, OUTPUT_DIR)

