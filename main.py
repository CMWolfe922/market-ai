# This script will be where all the main logic is run for data gathering.
# I also want to incorporate some simple trade picker logic that I can
# then use the symbols from to run more comprehensive tests on.

import requests, os, sys
import string
import pandas as pd
from bs4 import BeautifulSoup as bs
from loguru import logger
from sqlalchemy import create_engine
import sqlite3 as sql
import mysql.connector



path = os.getcwd()

try:
    if sys.platform == "linux":
        db_path = "/home/blackwolf/dev/projects/finance/market-ai/marketdata/data"
        sqlite_db = os.path.join(db_path, "marketdata.db")

        try:
            # [step 1] Get the companies from the database:
            from src.marketdata.models.sqlite_db import _query_symbols
            stocks = _query_symbols(sqlite_db)

            if stocks is None:
                # [step1.1 Get the companies from the function then store them in the database ]
                from src.marketdata.tickers import companies
                company_df = companies()

                from src.marketdata.models.sqlite_db import _insert_companies
                _insert_companies(company_df)

        except Exception as e:
            logger.error(" Error querying symbols and Error inserting companies: {}", e)

    elif sys.platform.contains('win'):
        mysql_uri = "mysql+mysqlconnector://root:root@localhost:3306/marketdata"

        try:
            from src.marketdata.models.db import create_marketdata_engine, insert_quote_data_mysql, insert_fundamental_data_mysql
            from src.marketdata.models.db import _insert_companies

        except:

            pass

except:

    pass
