import asyncio
import json
from json import JSONDecodeError
from typing import List, Union

import aiohttp
from celery.utils.log import get_task_logger

from project.database import db_context
from project.references.schemas import Vessel
from project.references.models import Vessel as VesselModel

from .schemas import VesselInfo, Error
from .headers import MARINE_TRAFFIC_HEADERS

SEARCH_STRING = "https://www.marinetraffic.com/en/vesselDetails/vesselInfo/shipid:"
logger = get_task_logger(__name__)


def get_json_from_string(body: str) -> Union[VesselInfo, Error]:
    try:
        data = json.loads(body)

    except JSONDecodeError as error:
        return Error(error=True, error_text=error.msg)

    result = VesselInfo(**data)
    return result


class MarineTrafficDataScrapper:
    vessel: Vessel
    url: str
    result: VesselInfo

    def __init__(self, marine_traffic_id: str):

        self.marine_traffic_id = marine_traffic_id
        self.url = f"{SEARCH_STRING}{self.marine_traffic_id}"
        self.__load_vessel()

    def __load_vessel(self):

        with db_context() as session:
            self.vessel = session.query(VesselModel). \
                filter(VesselModel.marine_traffic_id == self.marine_traffic_id).first()

    async def __save(self):

        if self.result.error:
            logger.info(f"vessel with marine_traffic_id:{self.marine_traffic_id} has error: {self.result.error_text}")
            return
        if not self.vessel:
            logger.info(f"vessel with marine_traffic_id:{self.marine_traffic_id} does not exists")
            return

        from project.locations.services import get_or_create_country
        from project.locations.schemas import CountryCreate

        with db_context() as session:

            country = get_or_create_country(session, country=CountryCreate(name=self.result.country,
                                                                           code=self.result.countryCode))

            if self.vessel.mmsi != self.result.mmsi or self.vessel.country_id != country.id:
                self.vessel.mmsi = self.result.mmsi
                self.vessel.country_id = country.id

                with db_context() as session:
                    self.vessel.save(db=session)

    async def scrape(self):

        if not self.vessel:
            logger.info(f"vessel with marine_traffic_id:{self.marine_traffic_id} does not exists")
            return

        async with aiohttp.ClientSession(headers=MARINE_TRAFFIC_HEADERS) as session:
            async with session.get(self.url) as resp:
                body = await resp.text()
                self.result = get_json_from_string(body)
                await self.__save()


async def run_tasks(vessels: List[str]):
    tasks = []

    for imo in vessels:
        vessel_id_scrapper = MarineTrafficDataScrapper(imo)
        task = asyncio.create_task(vessel_id_scrapper.scrape())
        tasks.append(task)

    await asyncio.gather(*tasks)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(run_tasks(["9380075"]))
