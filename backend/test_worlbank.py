from worldbank import fetch_indicator,INDICATORS


ind_gdp = fetch_indicator("IND",INDICATORS["gdp_per_capita"])
ind_edu = fetch_indicator("IND",INDICATORS["education"])
print(f"India GDP per capita: \n{ind_gdp}")
print(f"\n")
print(f"India Education: \n{ind_edu}")
country = "JPN"
for name,code in INDICATORS.items():
    data = fetch_indicator(country_code=country,indicator_code=code)
    print(f"\n{name}")
    print(data[:3])
#print(data[1][1])