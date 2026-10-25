#RESPONSIBILITY: Calculate trends and development gaps
from worldbank import fetch_indicator, INDICATORS

def compare_countries(country_codes,indicator_name,start_year,end_year):
    indicator_code = INDICATORS[indicator_name]["code"]
    comparisions = {}
    start_year = int(start_year)
    end_year = int(end_year)
    
    for code in country_codes:
        observation = fetch_indicator(country_code=code,indicator_code=indicator_code)
        filtered_data =[]
        for row in observation:
            if start_year<=row["year"]<=end_year:
                filtered_data.append(row)
        comparisions[code] = filtered_data
    return {
        "indicator": indicator_name,
        "start_year":start_year,
        "end_year": end_year,
        "countries":comparisions
    }