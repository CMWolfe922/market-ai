#!/usr/bin/venv python3

# This file will be used to extract stock tickers and symbols
# from the internet through webscraping and processing and
# cleaning the stocks symbols and names.
#
# The goal is to extract as many tickers as possible that
# are good and useful tickers to analyze. Some tickers have
# suffixes at the end that mean they are in some sort of trouble
#
# I will add ways to extract the good ticker and remove the ones
# with bad suffixes.

import requests, os
import string
import pandas as pd
from bs4 import BeautifulSoup as bs
import asyncio, aiohttp, httpx
