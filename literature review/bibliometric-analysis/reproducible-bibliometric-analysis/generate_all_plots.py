"""
Generate plots for all bibliometric analyses
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from wordcloud import WordCloud
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# Load data
data_file = 'output/ReproducedBibliometricAnalysis.xlsx'
xl = pd.ExcelFile(data_file)

print("Generating plots for all analyses...")
print("="*70)

# 1. Annual Scientific Production
print("1. Annual Scientific Production...")
df_annual = pd.read_excel(xl, sheet_name='AnnualSciProd')
plt.figure(figsize=(12, 6))
plt.bar(df_annual['Year'], df_annual['Articles'], color='steelblue', alpha=0.8)
plt.plot(df_annual['Year'], df_annual['Articles'], 'o-', color='darkblue', linewidth=2, markersize=6)
plt.xlabel('Year', fontsize=12, fontweight='bold')
plt.ylabel('Number of Articles', fontsize=12, fontweight='bold')
plt.title('Annual Scientific Production', fontsize=14, fontweight='bold')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('output/plots/01_Annual_Scientific_Production.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Annual Citations per Year
print("2. Annual Citations per Year...")
df_cit = pd.read_excel(xl, sheet_name='AnnualCitPerYear')
fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.bar(df_cit['Year'], df_cit['MeanTCperArt'], alpha=0.7, color='lightcoral', label='Mean TC per Article')
ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
ax1.set_ylabel('Mean Total Citations per Article', fontsize=12, fontweight='bold', color='darkred')
ax1.tick_params(axis='y', labelcolor='darkred')

ax2 = ax1.twinx()
ax2.plot(df_cit['Year'], df_cit['MeanTCperYear'], 'o-', color='darkblue', linewidth=2, markersize=6, label='Mean TC per Year')
ax2.set_ylabel('Mean Citations per Year', fontsize=12, fontweight='bold', color='darkblue')
ax2.tick_params(axis='y', labelcolor='darkblue')

plt.title('Average Article Citations per Year', fontsize=14, fontweight='bold')
fig.tight_layout()
plt.savefig('output/plots/02_Annual_Citations_per_Year.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Most Relevant Sources
print("3. Most Relevant Sources...")
df_sources = pd.read_excel(xl, sheet_name='MostRelSources').head(15)
plt.figure(figsize=(12, 8))
plt.barh(range(len(df_sources)), df_sources['Articles'], color='teal', alpha=0.8)
plt.yticks(range(len(df_sources)), df_sources['Sources'], fontsize=10)
plt.xlabel('Number of Articles', fontsize=12, fontweight='bold')
plt.title('Most Relevant Sources', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('output/plots/03_Most_Relevant_Sources.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. Bradford's Law
print("4. Bradford's Law...")
df_bradford = pd.read_excel(xl, sheet_name='BradfordLaw')
plt.figure(figsize=(12, 6))
colors = {'Zone 1': 'darkgreen', 'Zone 2': 'orange', 'Zone 3': 'lightcoral'}
for zone in ['Zone 1', 'Zone 2', 'Zone 3']:
    zone_data = df_bradford[df_bradford['Zone'] == zone]
    plt.scatter(zone_data['Rank'], zone_data['cumFreq'], label=zone, color=colors[zone], s=50, alpha=0.7)

plt.xlabel('Source Rank', fontsize=12, fontweight='bold')
plt.ylabel('Cumulative Frequency', fontsize=12, fontweight='bold')
plt.title("Bradford's Law - Source Distribution", fontsize=14, fontweight='bold')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('output/plots/04_Bradford_Law.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. Most Relevant Authors
print("5. Most Relevant Authors...")
df_authors = pd.read_excel(xl, sheet_name='MostRelAuthors').head(15)
plt.figure(figsize=(12, 8))
x = range(len(df_authors))
plt.barh(x, df_authors['Articles'], alpha=0.7, color='steelblue', label='Total Articles')
plt.barh(x, df_authors['Articles Fractionalized'], alpha=0.9, color='darkblue', label='Fractionalized')
plt.yticks(x, df_authors['Authors'], fontsize=10)
plt.xlabel('Number of Articles', fontsize=12, fontweight='bold')
plt.title('Most Relevant Authors', fontsize=14, fontweight='bold')
plt.legend()
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('output/plots/05_Most_Relevant_Authors.png', dpi=300, bbox_inches='tight')
plt.close()

# 6. Lotka's Law
print("6. Lotka's Law...")
df_lotka = pd.read_excel(xl, sheet_name='LotkaLaw')
plt.figure(figsize=(10, 6))
x = df_lotka['Documents written']
plt.plot(x, df_lotka['Proportion of Authors'], 'o-', linewidth=2, markersize=8, label='Observed', color='darkblue')
plt.plot(x, df_lotka['Theoretical'], 's--', linewidth=2, markersize=6, label='Theoretical (Lotka)', color='red')
plt.xlabel('Documents Written', fontsize=12, fontweight='bold')
plt.ylabel('Proportion of Authors', fontsize=12, fontweight='bold')
plt.title("Lotka's Law - Author Productivity Distribution", fontsize=14, fontweight='bold')
plt.legend()
plt.yscale('log')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('output/plots/06_Lotka_Law.png', dpi=300, bbox_inches='tight')
plt.close()

# 7. Country Scientific Production
print("7. Country Scientific Production...")
df_country = pd.read_excel(xl, sheet_name='CountrySciProd').head(15)
plt.figure(figsize=(12, 8))
plt.barh(range(len(df_country)), df_country['Freq'], color='forestgreen', alpha=0.8)
plt.yticks(range(len(df_country)), df_country['region'], fontsize=10)
plt.xlabel('Number of Documents', fontsize=12, fontweight='bold')
plt.title('Country Scientific Production', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('output/plots/07_Country_Scientific_Production.png', dpi=300, bbox_inches='tight')
plt.close()

# 8. Most Cited Countries
print("8. Most Cited Countries...")
df_country_cit = pd.read_excel(xl, sheet_name='MostCitCountries').head(15)
fig, ax1 = plt.subplots(figsize=(12, 8))

x = range(len(df_country_cit))
ax1.barh(x, df_country_cit['TC'], alpha=0.6, color='coral', label='Total Citations')
ax1.set_xlabel('Total Citations', fontsize=12, fontweight='bold')
ax1.set_yticks(x)
ax1.set_yticklabels(df_country_cit['Country'], fontsize=10)

ax2 = ax1.twiny()
ax2.plot(df_country_cit['Average Article Citations'], x, 'o-', color='darkblue', linewidth=2, markersize=6, label='Avg Citations')
ax2.set_xlabel('Average Citations per Article', fontsize=12, fontweight='bold', color='darkblue')

plt.title('Most Cited Countries', fontsize=14, fontweight='bold')
ax1.invert_yaxis()
plt.tight_layout()
plt.savefig('output/plots/08_Most_Cited_Countries.png', dpi=300, bbox_inches='tight')
plt.close()

# 9. Most Frequently Used Words
print("9. Most Frequently Used Words...")
df_words = pd.read_excel(xl, sheet_name='MostFreqWords').head(30)
plt.figure(figsize=(12, 10))
plt.barh(range(len(df_words)), df_words['Occurrences'], color='purple', alpha=0.7)
plt.yticks(range(len(df_words)), df_words['Words'], fontsize=9)
plt.xlabel('Occurrences', fontsize=12, fontweight='bold')
plt.title('Most Frequently Used Keywords', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('output/plots/09_Most_Frequent_Words.png', dpi=300, bbox_inches='tight')
plt.close()

# 10. Word Cloud
print("10. Word Cloud...")
df_wc = pd.read_excel(xl, sheet_name='WordCloud')
word_freq = dict(zip(df_wc.iloc[:, 0], df_wc.iloc[:, 1]))

wordcloud = WordCloud(width=1600, height=800, background_color='white', 
                      colormap='viridis', relative_scaling=0.5, min_font_size=10).generate_from_frequencies(word_freq)

plt.figure(figsize=(16, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Keyword Word Cloud', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('output/plots/10_Word_Cloud.png', dpi=300, bbox_inches='tight')
plt.close()

# 11. Trend Topics
print("11. Trend Topics...")
df_trend = pd.read_excel(xl, sheet_name='TrendTopics').head(20)
plt.figure(figsize=(14, 10))

for idx, row in df_trend.iterrows():
    y_pos = len(df_trend) - idx - 1
    plt.plot([row['Year (Q1)'], row['Year (Q3)']], [y_pos, y_pos], 'o-', linewidth=3, markersize=8, alpha=0.7)
    plt.plot(row['Year (Median)'], y_pos, 'D', color='red', markersize=10, alpha=0.9)

plt.yticks(range(len(df_trend)), df_trend['Term'].tolist()[::-1], fontsize=9)
plt.xlabel('Year', fontsize=12, fontweight='bold')
plt.title('Trending Topics Over Time (Q1-Median-Q3)', fontsize=14, fontweight='bold')
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('output/plots/11_Trend_Topics.png', dpi=300, bbox_inches='tight')
plt.close()

# 12. Most Globally Cited Documents
print("12. Most Globally Cited Documents...")
df_glob_cit = pd.read_excel(xl, sheet_name='MostGlobCitDocs').head(15)
plt.figure(figsize=(14, 8))
x = range(len(df_glob_cit))
plt.barh(x, df_glob_cit['Total Citations'], alpha=0.8, color='crimson')
plt.yticks(x, [p[:60] + '...' if len(p) > 60 else p for p in df_glob_cit['Paper']], fontsize=8)
plt.xlabel('Total Citations', fontsize=12, fontweight='bold')
plt.title('Most Globally Cited Documents', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('output/plots/12_Most_Globally_Cited_Documents.png', dpi=300, bbox_inches='tight')
plt.close()

# 13. Source Production Over Time
print("13. Source Production Over Time...")
df_source_time = pd.read_excel(xl, sheet_name='SourceProdOverTime')
plt.figure(figsize=(14, 7))

for col in df_source_time.columns[1:]:  # Skip 'Year' column
    plt.plot(df_source_time['Year'], df_source_time[col], 'o-', linewidth=2, markersize=6, label=col, alpha=0.8)

plt.xlabel('Year', fontsize=12, fontweight='bold')
plt.ylabel('Number of Articles', fontsize=12, fontweight='bold')
plt.title('Top Sources Production Over Time', fontsize=14, fontweight='bold')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('output/plots/13_Source_Production_Over_Time.png', dpi=300, bbox_inches='tight')
plt.close()

# 14. Country Collaboration Map
print("14. Country Collaboration Map...")
df_collab = pd.read_excel(xl, sheet_name='CollabWorldMap').head(20)
plt.figure(figsize=(14, 10))
x = range(len(df_collab))
plt.barh(x, df_collab['Frequency'], color='mediumseagreen', alpha=0.8)
labels = [f"{row['From']} - {row['To']}" for idx, row in df_collab.iterrows()]
plt.yticks(x, labels, fontsize=9)
plt.xlabel('Collaboration Frequency', fontsize=12, fontweight='bold')
plt.title('International Country Collaborations', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('output/plots/14_Country_Collaboration_Map.png', dpi=300, bbox_inches='tight')
plt.close()

# 15. Corresponding Author's Countries
print("15. Corresponding Author's Countries...")
df_corr_countries = pd.read_excel(xl, sheet_name='CorrAuthCountries').head(15)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Left plot: Articles count
ax1.barh(range(len(df_corr_countries)), df_corr_countries['Articles'], color='royalblue', alpha=0.8)
ax1.set_yticks(range(len(df_corr_countries)))
ax1.set_yticklabels(df_corr_countries['Country'], fontsize=10)
ax1.set_xlabel('Number of Articles', fontsize=11, fontweight='bold')
ax1.set_title('Articles by Country', fontsize=12, fontweight='bold')
ax1.invert_yaxis()
ax1.grid(axis='x', alpha=0.3)

# Right plot: SCP vs MCP
x = range(len(df_corr_countries))
ax2.barh(x, df_corr_countries['SCP'], alpha=0.8, color='lightgreen', label='Single Country (SCP)')
ax2.barh(x, df_corr_countries['MCP'], left=df_corr_countries['SCP'], alpha=0.8, color='salmon', label='Multiple Country (MCP)')
ax2.set_yticks(x)
ax2.set_yticklabels(df_corr_countries['Country'], fontsize=10)
ax2.set_xlabel('Number of Publications', fontsize=11, fontweight='bold')
ax2.set_title('Single vs Multi-Country Publications', fontsize=12, fontweight='bold')
ax2.legend()
ax2.invert_yaxis()
ax2.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('output/plots/15_Corresponding_Author_Countries.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n" + "="*70)
print("ALL PLOTS GENERATED!")
print("Plots saved to: output/plots/")
print("="*70)

