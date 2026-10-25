#RESPONSIBILITY: Fetch historical indicators
import httpx

def india():
    url = "https://api.worldbank.org/v2/country/ind/indicator/NY.GDP.PCAP.CD"

    response = httpx.get(
        url=url,
        params={
            "format":"json",
            "per_page":300
        }
    )
    response.raise_for_status()
    data = response.json()
    obs = data[1]
    result =[]
    for row in obs:
        year = row["date"]
        val = row["value"]
        result.append({"year":year,"value":val})
    return result
def fetch_country_pcap(country_id:str):
    url ="https://api.worldbank.org/v2/country/"+country_id+"/indicator/NY.GDP.PCAP.CD"
    response = httpx.get(
            url=url,
            params={
                "format":"json",
                "per_page":300
            },
            timeout=15.0
        )
    response.raise_for_status()
    data = response.json()
    obs = data[1]
    result =[]
    for row in obs:
        year =int(row["date"])
        val = row["value"]
        result.append({"year":year,"value":val})
    return result

INDICATORS = {
    "gdp_per_capita": {
        "code": "NY.GDP.PCAP.CD",
        "name": "GDP per capita",
        "unit": "Current US$",
        "direction": "higher_is_better"
    },
    "gdp_growth": {
        "code": "NY.GDP.MKTP.KD.ZG",
        "name": "GDP growth",
        "unit": "Annual %",
        "direction": "higher_is_better"
    },
    "life_expectancy": {
        "code": "SP.DYN.LE00.IN",
        "name": "Life expectancy at birth",
        "unit": "Years",
        "direction": "higher_is_better"
    },
    "education": {
        "code": "SE.SEC.ENRR",
        "name": "Secondary school enrollment",
        "unit": "Gross enrollment %",
        "direction": "higher_is_better"
    },
    "electricity_access": {
        "code": "EG.ELC.ACCS.ZS",
        "name": "Access to electricity",
        "unit": "% of population",
        "direction": "higher_is_better"
    },
    "infant_mortality": {
        "code": "SP.DYN.IMRT.IN",
        "name": "Infant mortality rate",
        "unit": "Deaths per 1,000 live births",
        "direction": "lower_is_better"
    },
    "unemployment": {
        "code": "SL.UEM.TOTL.ZS",
        "name": "Unemployment rate",
        "unit": "% of total labor force",
        "direction": "lower_is_better"
    }
}
def fetch_indicator(country_code:str, indicator_code:str):
    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}"
    response = httpx.get(
        url=url,
        params={
            "format":"json",
            "per_page":300
        },
        timeout=15.0
    )
    response.raise_for_status
    data = response.json()

    if not isinstance(data,list) or len(data)<2 or data[1] is None:
        return []
    return [
        {
            "year":int(row["date"]),
            "value":row["value"]
        }
        for row in data[1]
    ]
if(__name__=="__main__"):
    data = india()
    print(data)