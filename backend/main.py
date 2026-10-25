#RESPONSIBILITY: FastAPI application and endpoints
from fastapi import FastAPI,HTTPException
from analysis import compare_countries
from gap_analysis import calculate_gaps,analyze_progress
from countries import fetch_countries
from worldbank import INDICATORS
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="WorldShift API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/compare")
def compare(country:str,peers:str,indicator:str,start_year:str,end_year:str):
    if start_year>=end_year:
        raise HTTPException(status_code=400, detail="start_year greater than end_year")
    country_codes = [country.upper()] + [code.strip().upper() for code in peers.split(",") if code.strip()]
    if len(country_codes)!=len(set(country_codes)):
        raise HTTPException(status_code=400, detail="Duplicate entries not allowed")
    try:
        comparision = compare_countries(country_codes=country_codes,indicator_name=indicator,start_year=start_year,end_year=end_year)
        gaps = calculate_gaps(comparision=comparision,main_country=country.upper())
        progress = analyze_progress(comparision=comparision,main_country=country.upper())

        return {
            "comparison":comparision,
            "gaps":gaps,
            "progress_analysis":progress
        }
    except KeyError:
        raise HTTPException(status_code=400,detail="Unknown Indicator. Check indicator name")
    except ValueError as exc:
        raise HTTPException(status_code=400,detail=str(exc))


@app.get("/countries")
def get_countries():
    return fetch_countries()

@app.get("/indicators")
def get_indicators():
    return [
        {
            "id": indicator_id,
            **details
        }
        for indicator_id, details in INDICATORS.items()
    ]