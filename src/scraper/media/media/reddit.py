import praw
import pandas as pd
import click
from loguru import logger
import scrapy
from bs4 import BeautifulSoup as bs


reddit = praw.Reddit(
    client_id="XxR1O7-paGVn9Q01C2xR4A",
    client_secret="KYtutIx54IRJxb_Chc8IUu1ekA-TyQ",
    user_agent="Trends",
)


class RedditScraper(scrapy.Spider):
    name = 'reddit'

    def start_requests(self):
        subreddits = [
            'wallstreetbets',

        ]
        return super().start_requests()
