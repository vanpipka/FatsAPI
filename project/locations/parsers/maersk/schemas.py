from typing import List, Optional

from pydantic import BaseModel


class Error(BaseModel):
    error: Optional[str]


class SearchResult(Error):

    isContainerSearch: Optional[bool]

    {"isContainerSearch": True,
     "origin": {"terminal": "", "geo_site": "Unknown", "city": "Bunuel", "state": "", "country": "Spain",
                "country_code": "ES", "geoid_city": "3CZXYPC36FFJY", "site_type": ""},
     "destination": {"terminal": "Busan new port terminal Co.ltd", "geo_site": "146PS27H0RZMO", "city": "Busan",
                     "state": "", "country": "Korea, South", "country_code": "KR", "geoid_city": "2XOHKM8FX8VI7",
                     "site_type": "TERMINAL"}, "containers": [
        {"container_num": "MSKU9070323", "container_size": "40", "container_type": "Dry", "iso_code": "42G0",
         "operator": "MAEU", "locations": [
            {"terminal": "Tmz Rail Ramp", "geo_site": "0HSQ57LPIWSWL", "city": "Zaragoza", "state": "",
             "country": "Spain", "country_code": "ES", "geoid_city": "1YCRKDIDJZ5OE", "site_type": "RAIL TERMINAL",
             "events": [{"activity": "GATE-OUT", "stempty": False, "actfor": "EXP", "vessel_name": "MSC MIA",
                         "voyage_num": "247E", "vessel_num": "P6S", "actual_time": "2022-11-11T13:20:00.000",
                         "rkem_move": "GATE-OUT", "is_cancelled": False, "is_current": False}]},
            {"terminal": "BEST Terminal Catalunya", "geo_site": "K8TAIS4Q1YQBU", "city": "Barcelona", "state": "",
             "country": "Spain", "country_code": "ES", "geoid_city": "1FQMCYMU9XLZ2", "site_type": "TERMINAL",
             "events": [{"activity": "GATE-IN", "stempty": False, "actfor": "EXP", "vessel_name": "MSC MIA",
                         "voyage_num": "247E", "vessel_num": "P6S", "actual_time": "2022-11-14T07:43:00.000",
                         "rkem_move": "GATE-IN", "is_cancelled": False, "is_current": False},
                        {"activity": "LOAD", "stempty": False, "actfor": "", "vessel_name": "MSC MIA",
                         "voyage_num": "247E", "vessel_num": "P6S", "expected_time": "2022-11-24T09:00:00.000",
                         "actual_time": "2022-11-22T16:57:00.000", "rkem_move": "LOAD", "is_cancelled": False,
                         "is_current": False}]},
            {"terminal": "Busan new port terminal Co.ltd", "geo_site": "146PS27H0RZMO", "city": "Busan", "state": "",
             "country": "Korea, South", "country_code": "KR", "geoid_city": "2XOHKM8FX8VI7", "site_type": "TERMINAL",
             "events": [{"activity": "DISCHARG", "stempty": False, "actfor": "", "vessel_name": "MSC MIA",
                         "voyage_num": "247E", "vessel_num": "P6S", "expected_time": "2023-01-12T05:00:00.000",
                         "actual_time": "2023-01-13T05:30:00.000", "rkem_move": "DISCHARG", "is_cancelled": False,
                         "is_current": False},
                        {"activity": "GATE-OUT", "stempty": False, "actfor": "DEL", "vessel_name": "MSC MIA",
                         "voyage_num": "247E", "vessel_num": "P6S", "expected_time": "2023-01-12T05:00:00.000",
                         "actual_time": "2023-01-27T10:48:00.000", "rkem_move": "GATE-OUT", "is_cancelled": False,
                         "is_current": True}]}], "eta_final_delivery": "2023-01-13T05:30:00.000",
         "latest": {"actual_time": "2023-01-27T10:48:00.000", "activity": "GATE-OUT", "stempty": False, "actfor": "DEL",
                    "geo_site": "146PS27H0RZMO", "city": "Busan", "state": "", "country": "Korea, South",
                    "country_code": "KR"}, "status": "COMPLETE"}]}