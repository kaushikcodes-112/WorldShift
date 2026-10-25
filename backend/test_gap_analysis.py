from gap_analysis import analyze_progress
from analysis import compare_countries

comparisons = compare_countries(country_codes=["IND","JPN","BRA"],indicator_name="gdp_per_capita",start_year="2010",end_year="2024")
result = analyze_progress(comparision=comparisons,main_country="IND")

print(result)