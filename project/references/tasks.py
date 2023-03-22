import random
import logging

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
def download_marine_traffic_vessel_id(imo: str):

    if not imo:
        return

    from project.locations.parsers.marine_traffic.get_marine_traffic_id import run_tasks
    asyncio.run(run_tasks([imo]))


@shared_task
def refresh_vessel_info_from_marine_traffic(marine_traffic_id: str):

    if not marine_traffic_id:
        return

    from project.locations.parsers.marine_traffic.refresh_vessel_data import run_tasks
    asyncio.run(run_tasks([marine_traffic_id]))

