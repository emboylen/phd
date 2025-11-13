#You can copy and paste this entire block into a text editor (like VS Code, Notepad, etc.) and save it as run_bertopic_kg.py.
#run_bertopic_kg.py


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
PDF_FOLDER_PATH = "my_screened_pdfs" 
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
doc_info = topic_model.get_document_info(documents, doc_names=doc_names)

# 2. Get Topic-to-Keyword Mappings
print("Getting topic keywords...")
topic_keywords = topic_model.get_topics()

# 3. Get General Topic Info (for names, sizes, etc.)
topic_info = topic_model.get_topic_info()

print(f"Loaded {len(doc_info)} documents and {len(topic_info)} topics (including outliers).")


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

# Save and show the interactive HTML file
nt.show(OUTPUT_FILENAME)

print(f"\n--- Script Finished ---")
print(f"Successfully created and saved interactive knowledge graph to:")
print(f"{Path(OUTPUT_FILENAME).resolve()}")

#----------------------------------
#How to Run This File
#Install all dependencies:

#Bash
pip install bertopic "scikit-learn>=1.3.0" PyMuPDF networkx pyvis pandas
#Save the Code: Save the code block above as run_bertopic_kg.py.

#Set Your Folder: Change the PDF_FOLDER_PATH = "my_screened_pdfs" variable at the top of the file to point to your actual folder of PDFs.
#Run the Script: Open your terminal or command prompt, navigate to the directory where you saved the file, and run:

#Bash
python run_bertopic_kg.py
#The script will print its progress to the terminal. When it's finished, it will automatically open the interactive pdf_knowledge_graph.html file in your default web browser.