import random
import logging

from celery import shared_task
from celery.utils.log import get_task_logger
from project.database import db_context


logger = get_task_logger(__name__)


@shared_task
def divide(x, y):
    # from celery.contrib import rdb
    # rdb.set_trace()

    import time
    time.sleep(5)
    return x / y


