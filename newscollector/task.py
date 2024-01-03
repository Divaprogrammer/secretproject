from celery import shared_task
from .scripts.newsapi import DataCollector
from .scripts.newsapi_nytimes import getdata_nytimes

@shared_task(bind=True)
def news_scrapper(self):
    getdata_nytimes()
    DataCollector().main()
    return "done"

