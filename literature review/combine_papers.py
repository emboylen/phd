import os
from pathlib import Path
from datetime import datetime

# List of papers to include (from the user's image)
PAPERS_TO_INCLUDE = [
    "Expanding the microalgal industry - continuing controversy or compelling case",
    "Exploiting outcomes of life cycle costing to conduct coherent screening social life cycle assessments of e",
    "Exploring the potential of microalgae cell factories for generation of biofuels",
    "Feasibility of microalgae as feedstock for alternative fuel in Malaysia A review",
    "Fourth generation biofuel a review on risks and mitigation strategies",
    "Harnessing microalgae Innovations for achieving UN Sustainable Development Goals and climate resilie",
    "Insights into the potential impact of algae-mediated wastewater",
    "Integrated Applications of Microalgae to Wastewater Treatment and Biorefinery Recent Advances and Op",
    "Integrated CO2 capture, wastewater treatment and biofuel production by microalgae culturing - A review",
    "Integrated marine biogas a promising approach towards sustainability",
    "Integration of microalgae cultivation with industrial waste remediation for biofuel and bioenergy productio",
    "Integration of microalgae production with industrial biofuel facilities A critical review",
    "Large Scale Microalgae Biofuel TechnologyAn Development Perspectives in Light of the Barriers and Limit",
    "Life cycle assessment of green diesel production from microalgae",
    "Life Cycle Based GHG Emissions from Algae Based Bioenergy with a Special Emphasis on Climate Change",
    "Lignocellulosic biorefinery as a model for sustainable development of",
    "Marine microalgae contribution to sustainable development",
    "Marine microalgae for production of biofuels and chemicals",
    "Mass cultivation and harvesting of microalgal biomass current trends",
    "Mechanism and challenges in commercialisation of algal biofuels",
    "Micro-algae cultivation for biofuels Cost, energy balance, environmental impacts and future prospects",
    "Microalgae  a green multi- product biorefinery for future industrial prospects",
    "Microalgae  a robust  green bio-bridge  between energy and environment",
    "Microalgae A green multi-product biorefinery for future industrial prospects",
    "Microalgae a promising source for biofuel production",
    "Microalgae An alternative as sustainable source of biofuels",
    "Microalgae as A Potential Feedstock for Biodiesel Production in The Philippines A Review",
    "Microalgae as a solution of third world energy crisis for biofuels production from wastewater toward carbo",
    "Microalgae as a sustainable energy source for biodiesel production A review",
    "Microalgae as tools for bio-circular-green economy Zero-waste approaches for sustainable production at",
    "Microalgae based biorefinery promoting circular bioeconomy-techno economic and life-cycle analysis",
    "Microalgae Bioenergy with Carbon Capture and Storage (BECCS) An emerging sustainable bioprocess for",
    "Microalgae biofuels A critical review of issues, problems and the way forward",
    "Microalgae biofuels as an alternative to fossil fuel for power generation",
    "Microalgae biofuels illuminating the path to a sustainable future amidst challenges and opportunities",
    "Microalgae biofuels production A systematic review on socioeconomic prospects of microalgae biofuels",
    "Microalgae Biomass Production for Biofuels in Brazilian Scenario  A Critical Review",
    "Microalgae biomass production for a biorefinery system Recent advances and the way towards sustaina",
    "Microalgae biorefineries  Applications and emerging technologies",
    "Microalgae biorefinery  An integrated route for the sustainable production of high-value-added products",
    "Microalgae biorefinery alternatives and hazard evaluation",
    "Microalgae fast-growth sustainable green factories",
    "Microalgae for biofuels, wastewater treatment and environmental monitoring",
    "Microalgae for Sustainable Biofuel Generation Innovations, Bottlenecks, and Future Directions",
    "Microalgae in a global world New solutions for old problems",
    "Microalgae potential and multiple roles - current progress and future",
    "Microalgae production as a biofuel feedstock Risks and challenges",
    "Microalgae  a promising source for biofuel production",
    "Microalgae  a robust  green bio-bridge  between energy and environment",
    "Microalgae An alternative as sustainable source of biofuels",
    "Microalgae and biofuels A promising partnership",
    "Microalgae-Based BiorefineriesChallenges and Future Trends to Produce Carbohydrate Enriched Biomas",
    "Microalgae-based biodiesel production and its challenges and future opportunities A review",
    "Microalgal Biodiesel A Challenging Route toward a Sustainable Aviation Fuel",
    "Microalgal biodiesel in China Opportunities and challenges",
    "Microalgal Biodiesel Production  Realizing the Sustainability Index",
    "Microalgal Bioeconomy A Green Economy Approach Towards Achieving Sustainable Development Goals",
    "Microalgal bioenergy production under zero-waste biorefinery approach Recent advances and future pers",
    "Microalgal biofuel production Potential challenges and prospective research",
    "Microalgal biofuel revisitedAn informatics-based analysis of developments to date and future prospects",
    "Microalgal biofuels in ChinaThe past, progress and prospects",
    "Microalgal biofuelsChallenges and prospective in the framework of circular bioeconomy",
    "Microalgal biomass production as a sustainable feedstock for biodieselCurrent status and perspectives",
    "Microalgal Biorefineries for Bioenergy Production Can We Move from Concept to Industrial Reality",
    "Microalgal Co-cultivation for Biofuel Production and Bioremediation Current Status and Benefits",
    "Microalgal cultivation in secondary effluentrecent developments and",
    "Microalgal cultivation with biogas slurry for biofuel production",
    "Microalgal culture strategies for biofuel productionA review",
    "Microalgal drying and cell disruption - recent advances.",
    "Microalgal industry in China challenges and prospects.",
    "Microalgal systems for wastewater treatment technological trends and",
    "Microalgal-Based Bioenergy Strategies, Prospects, and Sustainability",
    "Multifaceted Role of Microalgae for Municipal Wastewater Treatment A Futuristic Outlook toward Waztew",
    "Net zero emission in circular bioeconomy from microalgae biochar",
    "Optimal design of microalgae-based biorefinery Economics, opportunities and challenges",
    "Overview of Carbon Capture Technology Microalgal Biorefinery Concept and State-of-the-Art",
    "Overview of CO2bioconversion into third-generation (3G) bioethanol - a",
    "Paradigm shift in algal biomass refinery and its challenges.",
    "Perspectives and challenges of small scale plant microalgae cultivation. Evidences from Southern Italy",
    "Perspectives of microalgal biofuels as a renewable source of energy",
    "Photobiological effects of converting biomass into hydrogen - challenges",
    "Photosynthetic green hydrogen Advances, challenges, opportunities, and prospects",
    "Potential of microalgal biodiesel production and its sustainability perspectives in Pakistan",
    "Potential of microalgal bioproducts general perspectives and main",
    "Potential use of saline resources for biofuel production using",
    "Progress of microalgae biofuel's commercialization",
    "Promising solutions to solve the bottlenecks in the large-scale cultivation of microalgae for biomassbioen",
    "Prospects of using microalgae for biofuels production Results of a Delphi study",
    "Realization process of microalgal biorefinery The optional approach toward carbon net-zero emission",
    "Recent advances in biodiesel production from agricultural products and",
    "Recent advances in the integrated biorefinery concept for the valorization of algal biomass through sustai",
    "Recent advances in wastewater microalgae-based biofuels production A state-of-the-art review",
    "Socioeconomic indicators for sustainable design and commercial",
    "Stakeholder perceptions of biofuels from microalgae",
    "Strategies and challenges to enhance commercial viability of algal",
    "Sustainability and carbon neutralization trends in microalgae bioenergy production from wastewater treat",
    "Sustainability and economic evaluation of microalgae grown in brewery",
    "Sustainability assessment of combined animal fodder and fuel production",
    "Sustainability considerations of biodiesel based on supply chain",
    "Sustainability index analysis of microalgae cultivation from biorefinery palm oil mill effluent",
    "Sustainability metrics on microalgae-based wastewater treatment system",
    "Sustainability of direct biodiesel synthesis from microalgae biomass A critical review",
    "Sustainable algal biorefinery a review on current perspective on",
    "Sustainable biofuels from algae",
    "Sustainable energy harnessing Microalgae as a potential biofuel source and carbon sequestration solutio",
    "Sustainable energy transitions Evaluating microalgal biodiesel feedstocks using multi-criteria decision m",
    "Sustainable hydrogen production via microalgae technological",
    "Sustainable microalgal biomass production in food industry wastewater",
    "Sustainable technologies for the reclamation of greenhouse gas CO2",
    "System integration for producing microalgae as biofuel feedstock",
    "The Analysis on the Current Situation of the Utilization Mode of Microalgal Biomass Materials",
    "The Contribution of Microalgae in Bio-refinery and Resource Recovery A Sustainable Approach leading to",
    "The current state of algae in wastewater treatment and energy",
    "The potential of microalgae biorefineries in Belgium and IndiaAn environmental techno-economic assess",
    "The promise and challenges of microalgal-derived biofuels",
    "The role of microalgae in the bioeconomy.",
    "The urge of algal biomass-based fuels for environmental sustainability against a steady tide of biofuel con",
    "The water-energy nexus at the hybrid bioenergy supply chain a",
    "Third-generation biofuel supply chain A comprehensive review and future research directions",
    "Towards a sustainable approach for development of biodiesel from plant and microalgae",
    "Upcycling food waste into biorefinery production by microalgae",
    "Using atmospheric emissions as CO2source in the cultivation of",
    "Using microalgae in the circular economy to valorise anaerobic",
    "Using microalgae to produce liquid transportation biodiesel What is next",
    "Valorisation of algal biomass to value-added metabolites emerging trends and opportunities",
    "Valorization of abattoir water discharge through phycoremediation for",
    "Valorization of micro-algae biomass for the development of green biorefinery Perspectives on techno-ec",
    "Valorization of microalgae biomass into bioproducts promoting circular bioeconomy a holistic approach",
    "Wastewater and waste CO2 for sustainable biofuels from microalgae",
    "Wastewater use in algae production for generation of renewable",
    "Water and emissions nexus for biodiesel in Iran",
    "Way forward to achieve sustainable and cost-effective biofuel production from microalgae a review",
    "Zero-carbon solution Microalgae as a low-cost feedstock for fuel production and carbon sequestration",
    "Zero-waste algal biorefinery for bioenergy and biochar A green leap towards achieving energy and environ",
]

def find_analysis_file(paper_title, analyses_dir):
    """Find the analysis file for a given paper title."""
    # The analysis files are named: [original-pdf-name]_analysis.txt
    # We need to match the paper title to find the right file
    
    analyses_path = Path(analyses_dir)
    if not analyses_path.exists():
        return None
    
    # Try to find a matching file
    for analysis_file in analyses_path.glob("*_analysis.txt"):
        # Remove the _analysis.txt suffix
        file_stem = analysis_file.stem.replace("_analysis", "")
        
        # Check if the paper title is contained in the filename
        if paper_title.lower() in file_stem.lower():
            return analysis_file
        
        # Also check reverse - if filename start is in paper title
        if file_stem.lower()[:50] in paper_title.lower():
            return analysis_file
    
    return None

def combine_analyses(papers_list, analyses_dir, output_file):
    """Combine multiple paper analyses into one document."""
    
    combined_content = []
    found_count = 0
    missing_papers = []
    
    # Header
    combined_content.append("=" * 100)
    combined_content.append("COMBINED LITERATURE REVIEW ANALYSES")
    combined_content.append("Microalgae Biofuel Sustainability - PhD Literature Review")
    combined_content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    combined_content.append(f"Total Papers: {len(papers_list)}")
    combined_content.append("=" * 100)
    combined_content.append("\n\n")
    
    # Process each paper
    for i, paper_title in enumerate(papers_list, 1):
        print(f"[{i}/{len(papers_list)}] Looking for: {paper_title[:60]}...")
        
        analysis_file = find_analysis_file(paper_title, analyses_dir)
        
        if analysis_file and analysis_file.exists():
            print(f"  [OK] Found: {analysis_file.name}")
            
            # Read the analysis content
            with open(analysis_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add to combined document
            combined_content.append("\n" + "─" * 100 + "\n")
            combined_content.append(f"PAPER {i}/{len(papers_list)}")
            combined_content.append("─" * 100 + "\n")
            combined_content.append(content)
            combined_content.append("\n")
            
            found_count += 1
        else:
            print(f"  [MISSING] NOT FOUND")
            missing_papers.append(paper_title)
    
    # Summary at the end
    combined_content.append("\n\n")
    combined_content.append("=" * 100)
    combined_content.append("SUMMARY")
    combined_content.append("=" * 100)
    combined_content.append(f"Papers found and included: {found_count}/{len(papers_list)}")
    combined_content.append(f"Papers not found: {len(missing_papers)}")
    
    if missing_papers:
        combined_content.append("\nMissing papers:")
        for paper in missing_papers:
            combined_content.append(f"  - {paper}")
    
    combined_content.append("=" * 100)
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(combined_content))
    
    print(f"\n{'='*80}")
    print(f"[SUCCESS] Combined document created: {output_file}")
    print(f"  Papers included: {found_count}/{len(papers_list)}")
    print(f"  Papers missing: {len(missing_papers)}")
    print(f"{'='*80}")

if __name__ == "__main__":
    ANALYSES_DIR = "paper-analyses"
    OUTPUT_FILE = "COMBINED_ANALYSES.txt"
    
    combine_analyses(PAPERS_TO_INCLUDE, ANALYSES_DIR, OUTPUT_FILE)

