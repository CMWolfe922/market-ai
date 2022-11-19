#!/usr/bin/env python3

# ================================================================ #
# Create commands for calling functions that will get the data
# required. Eventually I need to create a Dockerfile that I can
# create to run this app.
# ================================================================ #

from marketdata.financialdata.tickers import companies
from marketdata.models.db import _query_symbols
from utils.db import db, _insert_companies
import optparse
import os, sys
from loguru import logger

PATH = "/tmp/"
FILE = "main.log"
LOG_FILE = os.path.join(PATH, FILE)
logger.add(LOG_FILE, format="{time:MM/DD/YYYY at HH:mm:ss} | {level} | {name} | {message}", diagnose=True, backtrace=True)


if __name__ == "__main__":
    logger.info("[+] Starting Main Script:...")
    if not os.path.exists(db):
        companies_df = companies()
        _insert_companies(companies_df)
    else:
        symbols = _query_symbols(db)
        print(symbols)
