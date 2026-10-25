from analysis import compare_countries

result = compare_countries(
    country_codes=["IND", "JPN", "BRA"],
    indicator_name="gdp_per_capita",
    start_year=2010,
    end_year=2023
)

for code, observations in result["countries"].items():
    print(f"\n{code}")
    print(observations[:])