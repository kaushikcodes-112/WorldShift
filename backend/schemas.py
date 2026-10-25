#RESPONSIBILITY: Define the structure of API responses
from pydantic import BaseModel
from typing import Optional,Literal

class Observation(BaseModel):
    year:int
    value:Optional[float]

class CountryHistory(BaseModel):
    country_code:str
    observations:list[Observation]

class GapRecord(BaseModel):
    year:int
    main_value: float
    peer_median:float
    gap:float
    relative_gap: Optional[float] = None

class ProgressAnalysis(BaseModel):
    status: Optional[str] = None
    message: Optional[str] = None

    indicator:Optional[str] = None
    start_year:Optional[int] = None
    end_year:Optional[int] = None
    main_country:Optional[str] = None

    main_change_pct:Optional[float] = None
    peer_change_pct: Optional[dict[str,float]] = None
    peer_median_change_pct:Optional[float] = None
    difference_percentage_points:Optional[float] = None

    interpretation:Optional[
        Literal[
            "progress_faster",
            "progress_slower",
            "progress_equal"
        ]
    ]

class ComparisionResponse(BaseModel):
    comparision: dict
    gaps: list[GapRecord]
    progress_analysis:ProgressAnalysis