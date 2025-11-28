"""
Generate BERTopic Analysis Summary for Aligned Dataset
=======================================================

Creates comprehensive, printable summary of BERTopic results
for the 207 aligned papers used in dynamic topic modeling.

Author: PhD Literature Review Analysis
Date: November 2025
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
from bertopic import BERTopic


def generate_markdown_summary(merged_df, topic_info_df, output_path):
    """Generate comprehensive Markdown summary."""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        # Header
        f.write("# BERTopic Analysis Summary\n")
        f.write("## Microalgae Biofuel Literature Review - Aligned Dataset\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Dataset:** 207 papers (2009-2025) with complete bibliometric data\n\n")
        
        f.write("---\n\n")
        
        # Executive Summary
        f.write("## Executive Summary\n\n")
        f.write(f"This document presents the results of BERTopic semantic topic modeling ")
        f.write(f"performed on {len(merged_df)} peer-reviewed papers investigating microalgae ")
        f.write(f"for biofuel production. The analysis identified **{merged_df['topic'].nunique()} ")
        f.write(f"distinct research topics** spanning {merged_df['PY'].min():.0f}-{merged_df['PY'].max():.0f}.\n\n")
        
        # Key Statistics
        f.write("### Key Statistics\n\n")
        f.write(f"- **Total Papers:** {len(merged_df)}\n")
        f.write(f"- **Time Period:** {merged_df['PY'].min():.0f}-{merged_df['PY'].max():.0f} ({merged_df['PY'].max() - merged_df['PY'].min():.0f} years)\n")
        f.write(f"- **Total Citations:** {merged_df['TC'].sum():.0f}\n")
        f.write(f"- **Average Citations per Paper:** {merged_df['TC'].mean():.1f}\n")
        f.write(f"- **Median Citations per Paper:** {merged_df['TC'].median():.0f}\n")
        f.write(f"- **Topics Identified:** {merged_df['topic'].nunique()}\n")
        f.write(f"- **Average Topic Probability:** {merged_df['topic_probability'].mean():.3f}\n\n")
        
        # Most cited papers
        top_cited = merged_df.nlargest(5, 'TC')[['TI', 'PY', 'TC', 'topic_name']]
        f.write("### Most Cited Papers\n\n")
        for idx, row in top_cited.iterrows():
            f.write(f"{idx+1}. **{row['TI']}** ({row['PY']:.0f})\n")
            f.write(f"   - Citations: {row['TC']:.0f}\n")
            f.write(f"   - Topic: {row['topic_name']}\n\n")
        
        f.write("---\n\n")
        
        # Topic Overview
        f.write("## Topic Distribution\n\n")
        
        topic_dist = merged_df.groupby('topic').agg({
            'filename': 'count',
            'TC': ['sum', 'mean'],
            'PY': ['min', 'max']
        }).round(1)
        
        topic_dist.columns = ['Paper_Count', 'Total_Citations', 'Avg_Citations', 'First_Year', 'Last_Year']
        topic_dist = topic_dist.reset_index()
        
        f.write("| Topic | Papers | Total Citations | Avg Citations | Year Range |\n")
        f.write("|-------|--------|-----------------|---------------|------------|\n")
        
        for _, row in topic_dist.iterrows():
            topic_num = int(row['topic'])
            topic_name = merged_df[merged_df['topic'] == topic_num]['topic_name'].iloc[0]
            papers = int(row['Paper_Count'])
            pct = (papers / len(merged_df)) * 100
            total_cit = int(row['Total_Citations'])
            avg_cit = row['Avg_Citations']
            year_range = f"{int(row['First_Year'])}-{int(row['Last_Year'])}"
            
            f.write(f"| Topic {topic_num} | {papers} ({pct:.1f}%) | {total_cit} | {avg_cit:.1f} | {year_range} |\n")
        
        f.write("\n---\n\n")
        
        # Detailed Topic Descriptions
        f.write("## Detailed Topic Descriptions\n\n")
        
        for topic_num in sorted(merged_df['topic'].unique()):
            topic_papers = merged_df[merged_df['topic'] == topic_num]
            topic_name = topic_papers['topic_name'].iloc[0]
            
            f.write(f"### Topic {topic_num}: {topic_name}\n\n")
            
            # Topic statistics
            f.write(f"**Papers:** {len(topic_papers)} ({len(topic_papers)/len(merged_df)*100:.1f}%)\n\n")
            f.write(f"**Citations:** {topic_papers['TC'].sum():.0f} total, {topic_papers['TC'].mean():.1f} average\n\n")
            f.write(f"**Time Period:** {topic_papers['PY'].min():.0f}-{topic_papers['PY'].max():.0f}\n\n")
            
            # Top keywords (from topic_info if available)
            f.write(f"**Representative Keywords:**\n\n")
            f.write(f"_(BERTopic automatically extracted semantic keywords)_\n\n")
            
            # Most cited papers in this topic
            f.write(f"**Top 5 Most Cited Papers in Topic {topic_num}:**\n\n")
            top_in_topic = topic_papers.nlargest(5, 'TC')[['TI', 'PY', 'TC', 'AU']]
            
            for i, (idx, row) in enumerate(top_in_topic.iterrows(), 1):
                # Truncate long titles
                title = row['TI'][:100] + "..." if len(str(row['TI'])) > 100 else row['TI']
                # Get first author
                authors = str(row['AU']).split(';')[0] if pd.notna(row['AU']) else "Unknown"
                
                f.write(f"{i}. {title}\n")
                f.write(f"   - Author: {authors} ({row['PY']:.0f})\n")
                f.write(f"   - Citations: {row['TC']:.0f}\n\n")
            
            # Recent papers in this topic
            f.write(f"**Recent Papers (2023-2025) in Topic {topic_num}:**\n\n")
            recent_in_topic = topic_papers[topic_papers['PY'] >= 2023].nlargest(3, 'PY')[['TI', 'PY', 'TC']]
            
            if not recent_in_topic.empty:
                for i, (idx, row) in enumerate(recent_in_topic.iterrows(), 1):
                    title = row['TI'][:100] + "..." if len(str(row['TI'])) > 100 else row['TI']
                    f.write(f"{i}. {title} ({row['PY']:.0f}) - {row['TC']:.0f} citations\n")
            else:
                f.write("_No recent papers (2023-2025) in this topic_\n")
            
            f.write("\n---\n\n")
        
        # Temporal Analysis
        f.write("## Temporal Analysis\n\n")
        
        f.write("### Papers by Year\n\n")
        
        year_counts = merged_df['PY'].value_counts().sort_index()
        
        f.write("| Year | Papers | Total Citations | Avg Citations |\n")
        f.write("|------|--------|-----------------|---------------|\n")
        
        for year in sorted(year_counts.index):
            year_papers = merged_df[merged_df['PY'] == year]
            count = len(year_papers)
            total_cit = year_papers['TC'].sum()
            avg_cit = year_papers['TC'].mean()
            f.write(f"| {year:.0f} | {count} | {total_cit:.0f} | {avg_cit:.1f} |\n")
        
        f.write("\n### Publication Trends\n\n")
        
        # Identify growth periods
        early_period = merged_df[merged_df['PY'] <= 2015]
        middle_period = merged_df[(merged_df['PY'] > 2015) & (merged_df['PY'] <= 2020)]
        recent_period = merged_df[merged_df['PY'] > 2020]
        
        f.write(f"- **Early Period (2009-2015):** {len(early_period)} papers ({len(early_period)/len(merged_df)*100:.1f}%)\n")
        f.write(f"- **Middle Period (2016-2020):** {len(middle_period)} papers ({len(middle_period)/len(merged_df)*100:.1f}%)\n")
        f.write(f"- **Recent Period (2021-2025):** {len(recent_period)} papers ({len(recent_period)/len(merged_df)*100:.1f}%)\n\n")
        
        f.write(f"**Growth Rate:** {len(recent_period)/len(early_period):.1f}x increase from early to recent period\n\n")
        
        f.write("---\n\n")
        
        # Methodology
        f.write("## Methodology\n\n")
        
        f.write("### BERTopic Algorithm\n\n")
        f.write("BERTopic is a topic modeling technique that leverages transformer-based language models ")
        f.write("and class-based TF-IDF to create dense clusters and extract meaningful topics.\n\n")
        
        f.write("**Key Steps:**\n\n")
        f.write("1. **Document Embedding:** Papers converted to semantic embeddings using sentence transformers\n")
        f.write("2. **Dimensionality Reduction:** UMAP used to reduce embedding dimensions\n")
        f.write("3. **Clustering:** HDBSCAN algorithm groups similar papers\n")
        f.write("4. **Topic Representation:** Class-based TF-IDF extracts representative keywords\n\n")
        
        f.write("### Dataset Alignment\n\n")
        f.write(f"- **Original BERTopic analysis:** 223 papers\n")
        f.write(f"- **Original bibliometric dataset:** 222 papers\n")
        f.write(f"- **Aligned dataset (this analysis):** {len(merged_df)} papers\n\n")
        f.write(f"Only papers present in BOTH datasets are included to ensure consistent ")
        f.write(f"bibliometric metadata (publication year, citations, funding) for temporal analysis.\n\n")
        
        f.write("### Quality Metrics\n\n")
        f.write(f"- **Average Topic Probability:** {merged_df['topic_probability'].mean():.3f}\n")
        f.write(f"  _(Higher is better; >0.5 indicates strong topic assignment)_\n\n")
        
        high_conf = len(merged_df[merged_df['topic_probability'] > 0.5])
        f.write(f"- **High Confidence Assignments (>0.5):** {high_conf} papers ({high_conf/len(merged_df)*100:.1f}%)\n\n")
        
        f.write("---\n\n")
        
        # Data Sources
        f.write("## Data Sources\n\n")
        f.write("- **BERTopic Analysis:** November 2024\n")
        f.write("- **Bibliometric Data:** Scopus/Web of Science export (filtered)\n")
        f.write("- **Papers:** Peer-reviewed journal articles on microalgae biofuel production\n")
        f.write("- **Search Focus:** Technical barriers, sustainability, commercialization challenges\n\n")
        
        f.write("---\n\n")
        
        # Visualizations
        f.write("## Available Visualizations\n\n")
        f.write("The following visualizations are available in the `bertopic_outputs` directory:\n\n")
        f.write("1. **Intertopic Distance Map** - 2D visualization of topic relationships\n")
        f.write("2. **Topic Hierarchy** - Hierarchical clustering of topics\n")
        f.write("3. **Topic Bar Chart** - Top words per topic\n\n")
        
        f.write("---\n\n")
        
        # Footer
        f.write("## Notes\n\n")
        f.write(f"- This summary reflects the aligned dataset of {len(merged_df)} papers\n")
        f.write("- All statistics are based on matched papers with complete bibliometric data\n")
        f.write("- Topic names are auto-generated by BERTopic based on representative keywords\n")
        f.write("- For detailed analysis files, see: `machine-learning/dynamic-topic-analysis/`\n\n")
        
        f.write("---\n\n")
        f.write(f"*Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")


def generate_html_summary(markdown_path, html_path):
    """Convert Markdown to HTML for printing."""
    
    # Read markdown
    with open(markdown_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Simple markdown to HTML conversion
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BERTopic Analysis Summary - Microalgae Biofuel Literature Review</title>
    <style>
        @media print {{
            @page {{ margin: 2cm; }}
            body {{ margin: 0; }}
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 30px;
        }}
        
        h2 {{
            color: #34495e;
            border-bottom: 2px solid #95a5a6;
            padding-bottom: 5px;
            margin-top: 25px;
            page-break-after: avoid;
        }}
        
        h3 {{
            color: #7f8c8d;
            margin-top: 20px;
            page-break-after: avoid;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
            page-break-inside: avoid;
        }}
        
        th, td {{
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }}
        
        th {{
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }}
        
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        
        ul, ol {{
            margin: 10px 0;
            padding-left: 30px;
        }}
        
        li {{
            margin: 5px 0;
        }}
        
        hr {{
            border: none;
            border-top: 1px solid #ddd;
            margin: 30px 0;
        }}
        
        strong {{
            color: #2c3e50;
        }}
        
        code {{
            background-color: #f4f4f4;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        
        .stats-box {{
            background-color: #ecf0f1;
            padding: 15px;
            border-left: 4px solid #3498db;
            margin: 15px 0;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            page-break-after: avoid;
        }}
        
        .footer {{
            text-align: center;
            color: #7f8c8d;
            font-size: 0.9em;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
        }}
    </style>
</head>
<body>
"""
    
    # Convert markdown to HTML (basic conversion)
    lines = md_content.split('\n')
    in_table = False
    in_list = False
    
    for line in lines:
        # Headers
        if line.startswith('# '):
            html_content += f'<h1>{line[2:]}</h1>\n'
        elif line.startswith('## '):
            html_content += f'<h2>{line[3:]}</h2>\n'
        elif line.startswith('### '):
            html_content += f'<h3>{line[4:]}</h3>\n'
        # Tables
        elif line.startswith('|'):
            if not in_table:
                html_content += '<table>\n'
                in_table = True
            
            if '---' in line:
                continue  # Skip separator line
            
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            if 'Topic' in line or 'Year' in line or 'Papers' in line:
                html_content += '<tr>' + ''.join([f'<th>{cell}</th>' for cell in cells]) + '</tr>\n'
            else:
                html_content += '<tr>' + ''.join([f'<td>{cell}</td>' for cell in cells]) + '</tr>\n'
        else:
            if in_table:
                html_content += '</table>\n'
                in_table = False
            
            # Horizontal rule
            if line.strip() == '---':
                html_content += '<hr>\n'
            # Bold
            elif '**' in line:
                line = line.replace('**', '<strong>', 1).replace('**', '</strong>', 1)
                while '**' in line:
                    line = line.replace('**', '<strong>', 1).replace('**', '</strong>', 1)
                html_content += f'<p>{line}</p>\n'
            # Lists
            elif line.strip().startswith('- '):
                if not in_list:
                    html_content += '<ul>\n'
                    in_list = True
                html_content += f'<li>{line.strip()[2:]}</li>\n'
            elif line.strip().startswith(tuple([f'{i}. ' for i in range(10)])):
                html_content += f'<li>{line.strip()[3:]}</li>\n'
            else:
                if in_list and not line.strip().startswith('-'):
                    html_content += '</ul>\n'
                    in_list = False
                if line.strip():
                    html_content += f'<p>{line}</p>\n'
                else:
                    html_content += '<br>\n'
    
    if in_table:
        html_content += '</table>\n'
    if in_list:
        html_content += '</ul>\n'
    
    html_content += """
</body>
</html>
"""
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)


def main():
    """Generate printable BERTopic summary."""
    
    project_root = Path(__file__).parent.parent
    
    print("=" * 80)
    print("GENERATING BERTOPIC ANALYSIS SUMMARY - ALIGNED DATASET")
    print("=" * 80)
    
    # Load aligned merged dataset
    merged_path = project_root / 'machine-learning' / 'dynamic-topic-analysis' / 'merged_topic_bibliometric_ALIGNED.csv'
    merged_df = pd.read_csv(merged_path)
    
    print(f"\nLoaded aligned dataset: {len(merged_df)} papers")
    
    # Load topic info if available
    topic_info_path = project_root / 'machine-learning' / 'bertopic_outputs' / 'topic_info_20251119_130232.csv'
    topic_info_df = pd.read_csv(topic_info_path) if topic_info_path.exists() else None
    
    # Output paths
    output_dir = project_root / 'machine-learning' / 'dynamic-topic-analysis'
    md_path = output_dir / 'BERTOPIC_SUMMARY_ALIGNED_207_PAPERS.md'
    html_path = output_dir / 'BERTOPIC_SUMMARY_ALIGNED_207_PAPERS.html'
    
    # Generate Markdown summary
    print("\nGenerating Markdown summary...")
    generate_markdown_summary(merged_df, topic_info_df, md_path)
    print(f"[OK] Markdown summary: {md_path}")
    
    # Generate HTML summary
    print("\nGenerating HTML summary (printable)...")
    generate_html_summary(md_path, html_path)
    print(f"[OK] HTML summary: {html_path}")
    
    print("\n" + "=" * 80)
    print("SUMMARY GENERATION COMPLETE")
    print("=" * 80)
    
    print(f"\nPrintable documents created:")
    print(f"\n1. Markdown format: {md_path}")
    print(f"   - Easy to read in text editor or VS Code")
    print(f"   - Can convert to PDF using pandoc or similar tools")
    
    print(f"\n2. HTML format: {html_path}")
    print(f"   - Open in web browser (Chrome, Edge, Firefox)")
    print(f"   - Print to PDF using browser's print function (Ctrl+P)")
    print(f"   - Professional formatting with tables and styling")
    
    print(f"\nTo print:")
    print(f"  1. Open {html_path.name} in your web browser")
    print(f"  2. Press Ctrl+P (or Cmd+P on Mac)")
    print(f"  3. Select 'Save as PDF' as destination")
    print(f"  4. Adjust margins if needed and save")
    
    print(f"\nSummary includes:")
    print(f"  - Executive summary with key statistics")
    print(f"  - Detailed topic descriptions with representative papers")
    print(f"  - Temporal analysis (2009-2025)")
    print(f"  - Most cited papers overall and by topic")
    print(f"  - Methodology notes")
    print(f"  - Dataset alignment explanation")


if __name__ == '__main__':
    main()

