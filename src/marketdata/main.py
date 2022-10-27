from email.mime import base
import click
import os, time, humanize
from loguru import logger
from bs4 import BeautifulSoup as bs
import pandas as pd
import sqlalchemy as sa
import pymongo as mongo
from mysql.connector import connect, Error

# GET THE SECRETS THAT ARE NEEDED:
from config.secrets import TDA_APIKEY, REDDIT_APIKEY, REDDIT_USER_AGENT, REDDIT_CLIENT_ID
# Create the logger instance that will be used throughout
# this script. It will have to log to a file in the root
# directory
LOGFILE_PATH = "C:/Users/charl/Documents/python/projects/market-ai/tmp"
LOG_FILE = os.path.join(LOGFILE_PATH,"base.log")

logger.add(LOG_FILE, format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}", backtrace=True, diagnose=True)
base_logger = logger.bind()

# TODO: CREATE A SETTINGS FILE THAT CAN SET FILE PATHS
# FOR THINGS LIKE LOGGERS AND DATABASES.

from scripts.stockdata import Get
# ==================================================================== #
# Get Data:
# ==================================================================== #
get = Get(TDA_APIKEY)

company_df = get.companies()

print(company_df)
