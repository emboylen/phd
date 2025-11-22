#You can copy and paste this entire block into a text editor (like VS Code, Notepad, etc.) and save it as run_bertopic_kg.py.
#run_bertopic_kg.py

# Fix Unicode encoding issues on Windows
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import fitz  # PyMuPDF
import glob
from pathlib import Path
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer
import networkx as nx
from pyvis.network import Network
import pandas as pd

# --- Configuration ---
# *** Replace this with the path to your PDF folder ***
PDF_FOLDER_PATH = r"D:\Github\phd\ML\included" 
OUTPUT_FILENAME = "pdf_knowledge_graph.html"
MIN_TOPIC_SIZE = 10 # Adjust this to get more (lower) or fewer (higher) topics


print("--- Script Started ---")

# ==============================================================================
# STEP 1: EXTRACT TEXT FROM ALL PDFs
# ==============================================================================
print(f"\n--- Step 1: Extracting Text from PDFs in '{PDF_FOLDER_PATH}' ---")

pdf_files = list(Path(PDF_FOLDER_PATH).glob("*.pdf"))
print(f"Found {len(pdf_files)} PDF files.")

documents = []  # List to hold the text of each PDF
doc_names = []    # List to hold the filenames

for pdf_path in pdf_files:
    try:
        doc = fitz.open(pdf_path)
        full_text = ""
        
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            full_text += page.get_text("text")
            
        documents.append(full_text)
        doc_names.append(pdf_path.name) # Store just the filename
        doc.close()
    except Exception as e:
        print(f"  [Error] Failed to read {pdf_path}: {e}")

print(f"Successfully extracted text from {len(documents)} documents.")


# ==============================================================================
# STEP 2: TRAIN BERTOPIC MODEL
# ==============================================================================
if documents:
    print(f"\n--- Step 2: Training BERTopic Model (min_topic_size={MIN_TOPIC_SIZE}) ---")

    # Create a vectorizer to remove stop words and find 1- and 2-word phrases
    vectorizer_model = CountVectorizer(stop_words="english", ngram_range=(1, 2))

    # Initialize BERTopic
    topic_model = BERTopic(
        vectorizer_model=vectorizer_model,
        embedding_model="sentence-transformers/all-mpnet-base-v2",
        min_topic_size=MIN_TOPIC_SIZE,
        language="english",
        verbose=True 
    )

    # Fit the model to the extracted text
    # This is the most time-consuming step
    topics, probabilities = topic_model.fit_transform(documents)

    print("BERTopic model training complete.")
else:
    print("\nNo documents were successfully extracted. Exiting script.")
    exit()


# ==============================================================================
# STEP 3: PREPARE DATA FOR KNOWLEDGE GRAPH
# ==============================================================================
print("\n--- Step 3: Preparing Data for Knowledge Graph ---")

# 1. Get Document-to-Topic Mappings (using our filenames)
print("Getting document info...")
doc_info = topic_model.get_document_info(documents)
# Add the filenames to the dataframe
doc_info['Name'] = doc_names

# 2. Get Topic-to-Keyword Mappings
print("Getting topic keywords...")
topic_keywords = topic_model.get_topics()

# 3. Get General Topic Info (for names, sizes, etc.)
topic_info = topic_model.get_topic_info()

print(f"Loaded {len(doc_info)} documents and {len(topic_info)} topics (including outliers).")

# ==============================================================================
# STEP 3.5: CREATE TOPICS SUMMARY HTML TABLE
# ==============================================================================
print("\n--- Creating Topics Summary Table ---")

# Calculate statistics
total_topics_count = len(topic_info) - 1  # Exclude outlier topic
total_docs_count = len(doc_info[doc_info['Topic'] != -1])

# Add rows for each topic (excluding outliers)
topic_rows = ""
total_keywords_count = 0

for index, row in topic_info.iterrows():
    topic_id = row['Topic']
    if topic_id == -1:  # Skip outliers
        continue
    
    # Get keywords for this topic
    keywords = topic_keywords.get(topic_id, [])
    keywords_str = ", ".join([f"{word}" for word, score in keywords[:10]])  # Top 10 keywords
    total_keywords_count += len(keywords)
    
    # Get documents for this topic
    topic_docs = doc_info[doc_info['Topic'] == topic_id]['Name'].tolist()
    docs_html = "<ul class='documents-list'>"
    for doc in topic_docs[:10]:  # Show first 10 documents
        docs_html += f"<li>{doc}</li>"
    if len(topic_docs) > 10:
        docs_html += f"<li><em>... and {len(topic_docs) - 10} more</em></li>"
    docs_html += "</ul>"
    
    topic_rows += f"""
        <tr>
            <td class="topic-id">Topic {topic_id}</td>
            <td class="topic-name">{row['Name']}</td>
            <td class="keywords">{keywords_str}</td>
            <td class="doc-count">{row['Count']}</td>
            <td class="documents">{docs_html}</td>
        </tr>
    """

# Build complete HTML
html_table = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PDF Topic Analysis - Topics Summary</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{
            color: #333;
            text-align: center;
            margin-bottom: 10px;
        }}
        .subtitle {{
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }}
        .stats {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            text-align: center;
        }}
        .stats span {{
            display: inline-block;
            margin: 0 20px;
            font-size: 18px;
        }}
        .stats strong {{
            color: #2c3e50;
            font-size: 24px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}
        thead {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #f0f0f0;
        }}
        tr:hover {{
            background-color: #f8f9fa;
        }}
        .topic-id {{
            font-weight: bold;
            color: #667eea;
            font-size: 16px;
        }}
        .topic-name {{
            color: #2c3e50;
            font-weight: 500;
        }}
        .keywords {{
            color: #27ae60;
            font-family: 'Courier New', monospace;
            font-size: 13px;
        }}
        .doc-count {{
            text-align: center;
            font-weight: bold;
            color: #e74c3c;
        }}
        .documents {{
            font-size: 12px;
            color: #7f8c8d;
            max-height: 100px;
            overflow-y: auto;
        }}
        .documents-list {{
            margin: 5px 0;
            padding-left: 20px;
        }}
        .documents-list li {{
            margin: 3px 0;
        }}
    </style>
</head>
<body>
    <h1>📊 PDF Topic Analysis Summary</h1>
    <div class="subtitle">Topics and Keywords extracted from PDF documents</div>
    
    <div class="stats">
        <span><strong>{total_topics_count}</strong> Topics</span>
        <span><strong>{total_docs_count}</strong> Documents</span>
        <span><strong>{total_keywords_count}</strong> Unique Keywords</span>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>Topic ID</th>
                <th>Topic Name</th>
                <th>Top Keywords</th>
                <th>Docs</th>
                <th>Documents</th>
            </tr>
        </thead>
        <tbody>
{topic_rows}
        </tbody>
    </table>
</body>
</html>
"""

# Save the HTML table
table_filename = "topics_summary.html"
with open(table_filename, 'w', encoding='utf-8') as f:
    f.write(html_table)

print(f"✓ Topics summary table saved to: {Path(table_filename).resolve()}")


# ==============================================================================
# STEP 4: BUILD THE KNOWLEDGE GRAPH WITH NETWORKX
# ==============================================================================
print("\n--- Step 4: Building Knowledge Graph with NetworkX ---")

# Initialize the Graph
G = nx.Graph()

# --- 1. Add Topic Nodes ---
print("  Adding Topic nodes...")
for index, row in topic_info.iterrows():
    topic_id = row['Topic']
    if topic_id == -1:  # Skip the outlier topic
        continue
        
    G.add_node(
        f"Topic_{topic_id}", 
        type='topic', 
        size=max(row['Count'] / 5, 10),  # Scale size, ensure min size 10
        title=f"Topic {topic_id}: {row['Name']}", # Hover-over text
        color='#f08080' # Light red for topics
    )

# --- 2. Add Document Nodes and Document-Topic Edges ---
print("  Adding Document nodes and edges...")
for index, row in doc_info.iterrows():
    topic_id = row['Topic']
    if topic_id == -1:  # Skip outlier documents
        continue
    
    doc_name = row['Name']
    
    # Add the document node
    G.add_node(
        doc_name, 
        type='document', 
        size=5, 
        title=doc_name,
        color='#87ceeb' # Sky blue for documents
    )
    
    # Add the edge connecting the document to its topic
    G.add_edge(doc_name, f"Topic_{topic_id}", type='belongs_to')

# --- 3. Add Keyword Nodes and Topic-Keyword Edges ---
print("  Adding Keyword nodes and edges...")
for topic_id, keywords in topic_keywords.items():
    if topic_id == -1:  # Skip outlier topic
        continue
        
    for keyword, score in keywords:
        G.add_node(
            keyword, 
            type='keyword', 
            size=max(score * 100, 5), # Scale keyword size, ensure min size 5
            title=f"Keyword: {keyword}",
            color='#90ee90' # Light green for keywords
        )
        
        G.add_edge(
            f"Topic_{topic_id}", 
            keyword, 
            type='has_keyword', 
            weight=score 
        )

# --- 4. (Optional) Add Topic-to-Topic Edges ---
print("  Calculating and adding topic-to-topic similarity edges...")
try:
    similarity_matrix = topic_model.topic_similarity_matrix()
    topic_ids = topic_info['Topic'].tolist()

    for i in range(len(topic_ids)):
        for j in range(i + 1, len(topic_ids)):
            
            topic_id_i = topic_ids[i]
            topic_id_j = topic_ids[j]
            
            if topic_id_i == -1 or topic_id_j == -1: # Skip outliers
                continue
                
            similarity_score = similarity_matrix[i, j]
            
            # Add an edge if the similarity is above a certain threshold
            if similarity_score > 0.1: 
                G.add_edge(
                    f"Topic_{topic_id_i}", 
                    f"Topic_{topic_id_j}", 
                    type='related_to', 
                    weight=similarity_score,
                    title=f"Related (Score: {similarity_score:.2f})",
                    color='#cccccc' # Gray for related topic edges
                )
except Exception as e:
    print(f"  [Warning] Could not calculate topic similarity matrix. Skipping. Error: {e}")


print(f"Graph created with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")


# ==============================================================================
# STEP 5: VISUALIZE AND SAVE THE GRAPH WITH PYVIS
# ==============================================================================
print(f"\n--- Step 5: Visualizing Graph and Saving to '{OUTPUT_FILENAME}' ---")

# Create a pyvis network
nt = Network(notebook=True, height='800px', width='100%', cdn_resources='in_line', heading='PDF Topic Knowledge Graph')

# Load the networkx graph into pyvis
nt.from_nx(G)

# Add visualization options for better physics
nt.set_options("""
var options = {
  "nodes": {
    "font": {
      "size": 12,
      "face": "Tahoma"
    }
  },
  "edges": {
    "color": {
      "inherit": false
    },
    "smooth": false
  },
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -40000,
      "centralGravity": 0.1,
      "springLength": 120,
      "springConstant": 0.05
    },
    "maxVelocity": 50,
    "minVelocity": 0.75,
    "solver": "barnesHut"
  }
}
""")

# Save the interactive HTML file with UTF-8 encoding
# We need to manually write with UTF-8 to avoid encoding issues
html_content = nt.generate_html()
with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"\n--- Script Finished ---")
print(f"Successfully created and saved interactive knowledge graph to:")
print(f"{Path(OUTPUT_FILENAME).resolve()}")

#----------------------------------