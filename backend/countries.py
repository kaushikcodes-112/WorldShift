#RESPONSIBILITY: Fetch country metadata from REST Countries
import httpx

def fetch_countries():
    url = "https://api.worldbank.org/v2/country"

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

    print("API metadata:", data[0])
    print("Countries received:", len(data[1]) if len(data) > 1 and data[1] else 0)


    if not isinstance(data,list) or len(data)<2 or data[1] is None:
        return []
    countries = []

    for country in data[1]:
        if country["region"]["value"] == "Aggregates":
            continue
        countries.append(
            {
                "name":country["name"],
                "code": country["id"],
                "region":country["region"]["value"],
                "income_level": country["incomeLevel"]["value"]
            }
        )
    return sorted(countries,key=lambda c:c["name"])