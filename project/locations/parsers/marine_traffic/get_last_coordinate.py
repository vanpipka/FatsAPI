import asyncio
import json
from json import JSONDecodeError
from typing import List, Union

import aiohttp
from datetime import datetime

from celery.utils.log import get_task_logger

from project.database import db_context
from project.references.schemas import Vessel
from project.references.models import Vessel as VesselModel
from .schemas import Position, Error
from .headers import MARINE_TRAFFIC_HEADERS

SEARCH_STRING = "https://www.marinetraffic.com/vesselDetails/latestPosition/shipid:"
logger = get_task_logger(__name__)


def get_json_from_string(body: str) -> Union[Position, Error]:
    try:
        data = json.loads(body)
    except JSONDecodeError as error:
        return Error(error=True, error_text=error.msg)

    result = Position(**data)
    return result


class MarineTrafficCoordinateScrapper:
    vessel: Vessel
    url: str
    result: Position

    def __init__(self, marine_traffic_id: str):

        self.marine_traffic_id = marine_traffic_id
        self.url = f"{SEARCH_STRING}{self.marine_traffic_id}"
        self.__load_vessel()

    def __load_vessel(self):

        with db_context() as session:
            self.vessel = session.query(VesselModel). \
                filter(VesselModel.marine_traffic_id == self.marine_traffic_id).first()

    async def __save(self):

        from project.locations.schemas import CoordinateCreate
        from project.locations.services import create_coordinate

        if self.result.error:
            logger.info(f"vessel with marine_traffic_id:{self.marine_traffic_id} has error: {self.result.error_text}")
            return
        if not self.vessel:
            logger.info(f"vessel with marine_traffic_id:{self.marine_traffic_id} does not exists")
            return

        with db_context() as session:

            coordinate = CoordinateCreate(latitude=self.result.lat,
                                          longitude=self.result.lon,
                                          date=datetime.utcfromtimestamp(self.result.lastPos),
                                          vessel_id=self.vessel.id)

            create_coordinate(db=session, coordinate=coordinate)

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

    for marine_traffic_id in vessels:
        vessel_id_scrapper = MarineTrafficCoordinateScrapper(marine_traffic_id)
        task = asyncio.create_task(vessel_id_scrapper.scrape())
        tasks.append(task)

    logger.info(f"run_tasks {(',').join(vessels)}")
    await asyncio.gather(*tasks)


# loop = asyncio.get_event_loop()
# loop.run_until_complete(run_tasks(["459282"]))
