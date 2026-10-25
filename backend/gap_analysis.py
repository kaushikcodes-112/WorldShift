#RESPONSIBILTY: gap analysis of each year of a study country and a peer group
from operator import itemgetter
from statistics import median

def calculate_gaps(comparision, main_country):
    countries = comparision["countries"]
    if main_country not in countries:
        raise ValueError("Main country not found in comparision data")

    yearly_data={}
    for code,observation in countries.items():
        yearly_data[code] ={row['year'] : row['value'] for row in observation if row['value'] is not None}

    peers = [ code for code in countries if code != main_country]

    results = []

    for year,main_val in yearly_data[main_country].items():
        peer_values = [
            yearly_data[code][year]
            for code in peers
            if year in yearly_data[code]
        ]
        if not peer_values:
            continue
        peer_median = median(peer_values)
        gap = main_val-peer_median
        relative_gap = (((gap/peer_median)*100) if peer_median!=0 else None)

        results.append({
            "year":year,
            "main_value":main_val,
            "peer_value":peer_median,
            "gap":gap,
            "relative_gap":relative_gap
        })
    
    return sorted(results,key=itemgetter("year"))

def analyze_progress(comparision, main_country):
    countries = comparision["countries"]
    if main_country not in countries:
        raise ValueError("Main country not found")
    start_year = comparision["start_year"]
    end_year = comparision["end_year"]

    def percentage_change(observations):
        values = {
            row['year']:row['value']
            for row in observations
        }
        star_val = values.get(start_year)
        end_val = values.get(end_year)
        return ((end_val - star_val)/star_val)*100
    main_change = percentage_change(countries[main_country])

    if main_change is None:
        return{
            "status":"insufficient_data",
            "message": "Main country lacks valid end point"
        }
    peer_changes={}
    for code, observations in countries.items():
        if code == main_country:
            continue
        change = percentage_change(observations=observations)
        if change is not None:
            peer_changes[code] = change
    if not peer_changes:
        return{
            "status":"insufficient_data",
            "message":"No peers have valid endpoint data"
        }
    peer_median_change = median(peer_changes.values())
    difference = main_change - peer_median_change
    if difference<0:
        interpretation = "progress_slower"
    elif difference>0:
        interpretation = "progress_faster"
    else:
        interpretation = "progress_equal"
    return {
        "indicator": comparision["indicator"],
        "start_year": start_year,
        "end_year": end_year,
        "main_country": main_country,
        "main_change_pct": main_change,
        "peer_changes_pct": peer_changes,
        "peer_median_change_pct": peer_median_change,
        "difference_percentage_points": difference,
        "interpretation": interpretation
    }