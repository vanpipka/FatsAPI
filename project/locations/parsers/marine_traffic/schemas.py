from typing import List, Optional

from pydantic import BaseModel


class Error(BaseModel):
    error: Optional[bool]
    error_text: Optional[str]


class SearchResultString(BaseModel):
    desc: str
    type: str
    typeId: int
    url: str


class SearchResult(Error):
    results: List[SearchResultString]


class Port(BaseModel):
    id: str
    name: str
    countryCode: str


class Position(Error):

    lon: float
    lat: float
    areaName: str
    lastPos: int
    departurePort: Port
    arrivalPort: Port



