import praw
import pandas as pd
import click
from loguru import logger
import scrapy
from bs4 import BeautifulSoup as bs

subreddit = {'news': ['r/worldnews','r/news','r/europe','r/GlobalTalk','r/Finance','r/Financial Planning','r/Economics', 'r/Finance News',],
	'tech':['r/Futurology','r/technology','r/gadgets','r/CryptoTechnology','r/virtualreality','r/hardware','r/apple','r/google','r/pcgaming'],
	'retail':['r/gaming','r/pcmasterrace','r/GamePhysics','r/gamernews'],
	'investing':['r/finance','r/stocks','r/Economics','r/pennystocks','r/Shortsqueeze','r/RobinHoodPennyStocks','r/investing',
	'r/wallstreetbets', 'r/Wallstreetbetsnew', 'r/Wallstreetsilver','r/conspiracy','r/wallstreetbets2','r/GME','r/WallStreetbetsELITE',
	'r/wallstreet','r/occupywallstreet','r/Daytrading','r/RealDayTrading','r/options','r/StockMarket','r/DayTradingSignals',
	'r/stocks','r/IndianStreetBets','r/Forex','r/ASX_Bets','r/Trading'],
	'crypto': ['r/CryptoCurrency', 'r/SatoshiStreetBets','r/Bitcoin','r/dogecoin','r/ethtrader','r/CryptoMarkets'],
	'pennystocks': ['r/pennystocks','r/Shortsqueeze','r/RobinHoodPennyStocks']}


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
