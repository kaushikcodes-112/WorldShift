const API_BASE_URL = "http://127.0.0.1:8000";

export async function getCountries() {
    const response = await fetch(`${API_BASE_URL}/countries`);

    if (!response.ok) {
        throw new Error("Failed to fetch countries");
    }

    return response.json();
}

export async function getIndicators() {
    const response = await fetch(`${API_BASE_URL}/indicators`);

    if (!response.ok) {
        throw new Error("Failed to fetch indicators");
    }

    return response.json();
}
export async function compareCountries({country,peers,indicator,startYear,endYear}) {
    const params = new URLSearchParams({
        country,
        peers:peers.join(","),
        indicator,
        start_year:String(startYear),
        end_year:String(endYear)
    });
    const response = await fetch(`${API_BASE_URL}/compare?${params}`);
    if (!response.ok){
        const error = await response.json();
        throw new Error(error.detail||"Comparision Failed");
    }
    return response.json();
}