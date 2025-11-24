import os
from pathlib import Path
from datetime import datetime

# Papers to EXCLUDE from the combined document
PAPERS_TO_EXCLUDE = [
    "A Comprehensive Review on Microalgae-Based Biorefinery as Two-Way Source of Wastewater Treatment and Bioresource Recovery",
    "A comprehensive review on the advances of bioproducts from biomass        towards meeting net zero carbon emissions (NZCE).",
    "A conceptual review on microalgae biorefinery through thermochemical and biological pathways Bio-circular approach on carbon capture and wastewater treatment",
    "A critical overview of upstream cultivation and downstream processing of algae-based biofuelsOpportunity, technological barriers and future perspective",
    "A critical review on life cycle analysis of algae biodiesel current challenges and future prospects",
    "A Holistic Approach to Circular Bioeconomy Through the Sustainable Utilization of Microalgal Biomass for Biofuel and Other Value-Added Products",
    "A Microalgae-Based Biodiesel Refinery  Sustainability Concerns and Challenges",
    "A review of the strategy to promote microalgae value in CO2 conversion-lipid enrichment-biodiesel production",
    "A review of the sustainability of algal-based biorefineries Towards an integrated assessment framework",
    "A review on microalgae biofuel and biorefinery  challenges and way forward",
    "A review on sustainable microalgae based biofuel and bioenergy productionRecent developments",
    "A review on the current status and post-pandemic prospects of third-generation biofuels",
    "A state of the art review on the cultivation of algae for energy and other valuable products application, challenges, and opportunities.",
    "A sustainable perspective of microalgal biorefinery for co‐production and",
    "A systematic review on biofuel production and utilization from algae and waste feedstocks a circular economy approach",
    "Advancements and Prospects in Algal Biofuel Production A Comprehensive Review",
    "Advancements in sustainable production of biofuel by microalgae  Recent insights and future directions",
    "Advances and perspectives in using microalgae to produce biodiesel",
    "Advances in attached growth microalgae cultivation for third-generation biofuel production opportunities, challenges, and future prospect",
    "Agro-industrial wastewaters for algal biomass production, bio-based        products, and biofuels in a circular bioeconomy.",
    "Algae and their potential for a future bioeconomy, landless food        production, and the socio-economic impact of an algae industry.",
    "Algae as a source of renewable energy opportunities, challenges, and recent developments",
    "Algae-based bioenergy production aligns with the Paris agreement goals as a carbon mitigation technology",
    "Algal bioenergy production and utilization Technologies, challenges, and prospects",
    "Algal biofuel and their impact on agriculture and environment",
    "Algal biofuel production and mitigation potential in India",
    "Algal biofuels in Canada Status and potential",
    "Algal biomass valorization for biofuel production and carbon sequestration a review",
    "Algal bioplastics current market trends and technical aspects",
    "Algal biorefinery a potential solution to the food-energy-water-environment nexus",
    "Algal biorefinery An integrated approach for sustainable biodiesel production",
    "Algal biorefinery culminating multiple value-added productsrecent advances, emerging trends, opportunities, and challenges",
    "Algal biorefinery models with self-sustainable closed loop approachtrends and prospective for blue-bioeconomy",
    "Algal-Based Carbonaceous Materials for Environmental Remediation  Advances in Wastewater Treatment, Carbon Sequestration, and Biofuel Applications",
    "Aligning sustainable aviation fuel research with sustainable development goals Trends and thematic analysis",
    "An economic and technical evaluation of microalgal biofuels",
    "An integrated approach of algae-bacteria mediated treatment of industries generated wastewater optimal recycling of water and safe way        of resource recovery",
    "An outlook on microalgal biofuels",
    "An overview on microalgae as renewable resources for meeting sustainable development goals",
    "Anaerobic digestate as a low-cost nutrient source for sustainable  microalgae cultivation a way forward through waste valorization   approach",
    "Anaerobic digestion of microalgae as a necessary step to make microalgal biodiesel sustainable",
    "Anaerobic digestion of microalgal biomass Challenges, opportunities and research needs",
    "Analysis of the limiting factors for large scale microalgal cultivation a promising future for renewable and sustainable biofuel industry.",
    "Application of Microalgae to Wastewater Bioremediation, with CO2 Biomitigation, Health Product and Biofuel Development, and Environmental Biomonitoring",
    "Application of microbial resources in biorefineries current trend and future prospects",
    "Assessing global carbon sequestration and bioenergy potential from microalgae cultivation on marginal lands leveraging machine learning",
    "Assessing sustainability of microalgae-based wastewater treatmentEnvironmental considerations and impacts on human health",
    "Aviation fuel based on wastewater-grown microalgae Challenges and opportunities of hydrothermal liquefaction and hydrotreatment",
    "Bibliometric insights into microalgae cultivation in wastewater trends        and future prospects for biolipid production and environmental        sustainability",
    "Bio-mitigation of carbon dioxide using microalgal systems Advances and perspectives",
    "Bio-processing of algal bio-refinery  a review on current advances and future perspectives",
    "Biofuel from microalgae Sustainable pathways",
    "Biofuel policy in India A review of policy barriers in sustainable marketing of biofuel",
    "Biofuel production from microalgae challenges and chances",
    "Biofuel Production Using Cultivated Algae Technologies, Economics, and Its Environmental Impacts",
    "Biogas from microalgae Technologies, challenges and opportunities",
    "Bioproducts from microalgae biomass Technology, sustainability, challenges and opportunities",
    "Bioremediation of water containing pesticides by microalgae mechanisms, methods, and prospects for future research.",
    "Biotechnological perspectives on algae a viable option for next generation biofuels.",
    "Biotreatment of Industrial Wastewater using Microalgae A Tool for a Sustainable Bioeconomy",
    "Carbon sequestration using microalgae - a review",
    "Challenges and opportunities for microalgae-mediated CO2capture and biorefinery",
    "Challenges and opportunities in application of microalgae (Chlorophyta) for wastewater treatment a review",
    "Closed loop bioeconomy opportunities through the integration of microalgae cultivation with anaerobic digestion A critical review",
    "Co-pyrolysis of sewage sludge with lignocellulosic and algal biomass for sustainable liquid and gaseous fuel productiona life cycle assessment and techno-economic analysis",
    "CO2 mitigation and phycoremediation of industrial flue gas and wastewater via microalgae-bacteria consortium possibilities and challenges.",
    "Commercialization potential of microalgae for biofuels production",
    "Comprehensive insights into conversion of microalgae to feed, food, and biofuels Current status and key challenges towards implementation of sustainable biorefineries",
    "Consequential analysis of algal biofuels benefits to ocean resources",
    "Continuous cultivation of microalgae in photobioreactors as a source of renewable energy Current status and future challenges",
    "Coupling bioremediation and biorefinery prospects of microalgae for circular economy",
    "Critical factors in energy generation from microalgae",
    "Cultivation and Processing of Microalgae for Its Sustainability as a Feedstock for Biodiesel Production",
    "Cultivation in wastewaters for energy A microalgae platform",
    "Current and Future Perspective of Microalgae for Simultaneous Wastewater Treatment and Feedstock for Biofuels Production",
    "Current Bottlenecks and Challenges of the Microalgal Biorefinery",
    "Current Issues and Developments in Cyanobacteria-Derived Biofuel as a Potential Source of Energy for Sustainable Future",
    "Current perspectives, future challenges and key technologies of biohydrogen production for building a carbon-neutral futura review",
    "Current research and perspectives on microalgae-derived biodiesel",
    "Current Status and Challenges of Microalgae as an Eco-Friendly Biofuel Feedstock A Review",
    "Current status, issues and developments in microalgae derived biodiesel production",
    "Current trends and prospects in microalgae-based bioenergy production",
    "Current trends in biodiesel production technologies and future progressions A possible displacement of the petro-diesel",
    "Development of Microalgae Biodiesel Current Status and Perspectives",
    "Development perspectives of promising lignocellulose feedstocks for production of advanced generation biofuelsA review",
    "Developments and challenges in biodiesel production from microalgae A review",
    "Dual potential of microalgae as a sustainable biofuel feedstock and animal feed",
    "Economic and policy issues in the production of algae-based biofuels a review.",
    "Enhanced CO2 fixation and biofuel production via microalgaeRecent developments and future directions",
    "Enhancing sustainability  microalgae cultivation for biogas enrichment and phycoremediation of palm oil mill effluent - a comprehensive review",
    "Environmental life cycle assessment of algae systems Critical review of modelling approaches",
    "Environmental pollution mitigation through utilization of carbon dioxideby microalgae",
]

def get_all_analysis_files(analyses_dir):
    """Get all analysis files from the directory."""
    analyses_path = Path(analyses_dir)
    if not analyses_path.exists():
        return []
    return sorted(analyses_path.glob("*_analysis.txt"))

def should_exclude(analysis_file, exclude_list):
    """Check if this analysis file should be excluded."""
    # Remove the _analysis.txt suffix
    file_stem = analysis_file.stem.replace("_analysis", "")
    
    # Check if this paper is in the exclude list
    for excluded_paper in exclude_list:
        # Normalize both strings for comparison
        excluded_normalized = excluded_paper.lower().strip()
        file_normalized = file_stem.lower().strip()
        
        # Check for match (either way)
        if excluded_normalized in file_normalized or file_normalized in excluded_normalized:
            return True
        
        # Also check if first 60 chars match (for truncated titles)
        if excluded_normalized[:60] in file_normalized or file_normalized[:60] in excluded_normalized:
            return True
    
    return False

def combine_analyses_exclude(exclude_list, analyses_dir, output_file):
    """Combine all paper analyses EXCEPT those in the exclude list."""
    
    all_files = get_all_analysis_files(analyses_dir)
    
    if not all_files:
        print(f"No analysis files found in {analyses_dir}")
        return
    
    combined_content = []
    included_count = 0
    excluded_count = 0
    included_papers = []
    excluded_papers = []
    
    # Process each analysis file
    for i, analysis_file in enumerate(all_files, 1):
        # Print progress every 20 files
        if i % 20 == 0 or i == len(all_files):
            print(f"Processing... {i}/{len(all_files)} files checked")
        
        if should_exclude(analysis_file, exclude_list):
            excluded_count += 1
            excluded_papers.append(analysis_file.stem.replace("_analysis", ""))
        else:
            
            # Read the analysis content
            with open(analysis_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract just the source filename and analysis content
            lines = content.split('\n')
            source_line = ""
            analysis_lines = []
            in_analysis = False
            
            for idx, line in enumerate(lines):
                # Get source filename
                if line.startswith("Source:"):
                    source_line = line.replace("Source: ", "").strip()
                
                # Start capturing after second separator (after "Analyzed:")
                if "====" in line and idx > 3:
                    in_analysis = True
                    continue
                
                # Stop at Notes section or second separator
                if in_analysis and ("====" in line or line.strip() == "Notes:"):
                    break
                
                # Capture analysis content (skip empty lines at start)
                if in_analysis and (analysis_lines or line.strip()):
                    analysis_lines.append(line)
            
            # Clean up analysis text (remove leading/trailing blank lines)
            analysis_text = '\n'.join(analysis_lines).strip()
            
            # Add to combined document - minimal format
            combined_content.append(f"\n[{included_count + 1}] {source_line}")
            combined_content.append(analysis_text)
            combined_content.append("-" * 80)
            
            included_count += 1
            included_papers.append(analysis_file.stem.replace("_analysis", ""))
    
    # Add compact header at the start
    header = [
        "=" * 80,
        f"Microalgae Biofuel Sustainability PhD Literature Review | {datetime.now().strftime('%Y-%m-%d')}",
        f"Papers included: {included_count} | Papers excluded: {excluded_count}",
        "=" * 80
    ]
    combined_content = header + combined_content
    
    # Compact summary at end
    combined_content.append(f"\n{'='*80}")
    combined_content.append(f"END - {included_count} papers analyzed")
    combined_content.append("=" * 80)
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(combined_content))
    
    print(f"\n{'='*80}")
    print(f"[SUCCESS] Combined document created: {output_file}")
    print(f"  Total papers found: {len(all_files)}")
    print(f"  Papers included: {included_count}")
    print(f"  Papers excluded: {excluded_count}")
    print(f"{'='*80}")

if __name__ == "__main__":
    ANALYSES_DIR = "paper-analyses"
    OUTPUT_FILE = "COMBINED_ANALYSES_COMPACT.txt"
    
    combine_analyses_exclude(PAPERS_TO_EXCLUDE, ANALYSES_DIR, OUTPUT_FILE)

