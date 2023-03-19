import asyncio
import json
from json import JSONDecodeError
from typing import List, Union

import aiohttp
from celery.utils.log import get_task_logger

from project.database import db_context
from project.references.schemas import Vessel
from project.references.models import Vessel as VesselModel

from .schemas import SearchResult, Error
from .headers import MARINE_TRAFFIC_HEADERS

SEARCH_STRING = "https://www.marinetraffic.com/en/global_search/search?term=%imo%&types=1,3,7,9"
logger = get_task_logger(__name__)


def get_json_from_search_string(body: str) -> Union[SearchResult, Error]:

    try:
        data = json.loads(body)

    except JSONDecodeError as error:
        return Error(error=True, error_text=error.msg)

    result = SearchResult(**data)
    return result


class MarineTrafficIdScrapper:

    vessel: Vessel
    url: str
    result: SearchResult

    def __init__(self, imo, search_string="shipid:"):

        self.search_string = search_string
        self.imo = imo
        self.url = SEARCH_STRING.replace("%imo%", imo)
        self.__load_vessel()

    def __load_vessel(self):

        with db_context() as session:
            self.vessel = session.query(VesselModel).filter(VesselModel.imo == self.imo).first()

    async def __save(self):

        if self.result.error:
            logger.info(f"vessel with imo:{self.imo} has error: {self.result.error_text}")
            return
        if not self.vessel:
            logger.info(f"vessel with imo:{self.imo} does not exists")
            return

        with db_context() as session:
            session.add(self.vessel)
            session.commit()
            session.refresh(self.vessel)

    async def __set_marine_traffic_id_from_result(self):

        for search_result in self.result.results:
            if search_result.typeId == 3:
                index = search_result.url.find(self.search_string)
                self.vessel.marine_traffic_id = search_result.url[index+len(self.search_string):]
                await self.__save()
                return

        logger.info(f"vessel with imo:{self.imo} not found")

    async def scrape(self):

        if not self.vessel:
            logger.info(f"vessel with imo:{self.imo} does not exists")
            return

        async with aiohttp.ClientSession(headers=MARINE_TRAFFIC_HEADERS) as session:
            async with session.get(self.url) as resp:
                self.result = get_json_from_search_string(await resp.text())
                await self.__set_marine_traffic_id_from_result()


async def run_tasks(vessels: List[str]):

    tasks = []

    for imo in vessels:
        vessel_id_scrapper = MarineTrafficIdScrapper(imo)
        task = asyncio.create_task(vessel_id_scrapper.scrape())
        tasks.append(task)

    await asyncio.gather(*tasks)


#loop = asyncio.get_event_loop()
#loop.run_until_complete(run_tasks(["9380075"]))
