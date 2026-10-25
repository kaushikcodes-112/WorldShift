from analysis import compare_countries
from gap_analysis import calculate_gaps

comparison = compare_countries(
    country_codes=["IND", "JPN", "BRA"],
    indicator_name="gdp_per_capita",
    start_year=2010,
    end_year=2023
)

gaps = calculate_gaps(comparison, main_country="IND")

for row in gaps:
    print(
        row["year"],
        "India:", row["main_value"],
        "Peer median:", row["peer_value"],
        "Gap:", row["gap"]
    )