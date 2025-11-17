"""Regenerate just the knowledge graph using the existing model"""
import sys
import os
from pathlib import Path
import networkx as nx
from pyvis.network import Network
from gensim.models import LdaModel

# Load the final model
CHECKPOINT_DIR = "model_checkpoints"
checkpoint_files = list(Path(CHECKPOINT_DIR).glob("final_best_model_*.pkl"))

if not checkpoint_files:
    print("ERROR: No final model found. Please run the main script first.")
    sys.exit(1)

model_file = checkpoint_files[0]
print(f"Loading model from: {model_file}")
final_model = LdaModel.load(str(model_file))

# Extract k from filename
k = int(model_file.stem.split('_k')[1])
print(f"Model has {k} topics")

# Load document topics from the HTML file (or recreate)
# For simplicity, let's just create a basic graph without document nodes

print("\nGenerating Knowledge Graph...")

G = nx.Graph()

# Add topic nodes
for topic_id in range(k):
    topic_words = [word for word, _ in final_model.show_topic(topic_id, topn=5)]
    topic_label = f"Topic {topic_id}: {' '.join(topic_words[:3])}"
    
    G.add_node(
        f"Topic_{topic_id}",
        type='topic',
        size=30,
        title=topic_label,
        color='#f08080',
        label=f"T{topic_id}"
    )

# Add top keyword nodes for each topic
for topic_id in range(k):
    top_words = final_model.show_topic(topic_id, topn=7)
    for word, score in top_words:
        word_display = word.replace('_', ' ')
        
        G.add_node(
            word,
            type='keyword',
            size=int(max(score * 80, 5)),  # Convert to int
            title=f"Keyword: {word_display}",
            color='#90ee90',
            label=word_display
        )
        
        G.add_edge(f"Topic_{topic_id}", word, weight=float(score))  # Convert to float

print(f"✓ Graph created: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

# Create Pyvis visualization
nt = Network(notebook=False, height='900px', width='100%', bgcolor='#f5f5f5', 
             font_color='#2c3e50', heading='Refined Topic Model Knowledge Graph')

nt.from_nx(G)

nt.set_options("""
var options = {
  "nodes": {
    "font": {
      "size": 14,
      "face": "Tahoma"
    },
    "borderWidth": 2,
    "shadow": true
  },
  "edges": {
    "color": {
      "inherit": true,
      "opacity": 0.4
    },
    "smooth": {
      "type": "continuous"
    }
  },
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -30000,
      "centralGravity": 0.3,
      "springLength": 150,
      "springConstant": 0.04,
      "damping": 0.09
    },
    "maxVelocity": 50,
    "minVelocity": 0.75,
    "solver": "barnesHut",
    "stabilization": {
      "iterations": 150
    }
  }
}
""")

# Save visualization
OUTPUT_GRAPH_FILENAME = "refined_knowledge_graph.html"
html_graph = nt.generate_html()
with open(OUTPUT_GRAPH_FILENAME, 'w', encoding='utf-8') as f:
    f.write(html_graph)

print(f"✓ Knowledge graph saved to: {Path(OUTPUT_GRAPH_FILENAME).resolve()}")
print("\n✅ Done! Open refined_knowledge_graph.html in your browser.")

