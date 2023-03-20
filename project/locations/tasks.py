import random
import logging
from typing import List

from celery import shared_task
from celery.utils.log import get_task_logger
from project.database import db_context
import asyncio

logger = get_task_logger(__name__)


@shared_task
def test_task():
    import time
    time.sleep(5)
    return __name__


@shared_task
def download_vessel_coordinate(marine_traffic_id: str):

    if not marine_traffic_id:
        return

    from project.locations.parsers.marine_traffic.get_last_coordinate import run_tasks
    asyncio.run(run_tasks([marine_traffic_id]))


@shared_task
def download_vessels_coordinate() -> dict:

    from project.locations.parsers.marine_traffic.get_last_coordinate import run_tasks
    from project.references.services import get_vessels_on_tracking

    with db_context() as session:
        vessels = get_vessels_on_tracking(session)
        if not vessels:
            return {"result": "no objects to process"}

    marine_traffic_ids = []

    for vessel in vessels:

        marine_traffic_ids.append(vessel.marine_traffic_id)

        if len(marine_traffic_ids) == 50:
            asyncio.run(run_tasks(marine_traffic_ids))
            marine_traffic_ids = []

    if len(marine_traffic_ids) > 0:
        asyncio.run(run_tasks(marine_traffic_ids))

    return {"result": f"started for {len(vessels)} objects"}
