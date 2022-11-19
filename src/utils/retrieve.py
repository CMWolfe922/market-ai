#!/usr/bin/env python3

# ================================================================ #
# This file is for retrieving data from other files, databases,
# functions or API connectors. I will build all the retrieval
# methods in this file.
#
# I need to treat each retrieval source as an object. TD Ameritrade,
# Yahoo Finance, FRED API, Reddit, Twitter, etc..
#
# I need an AbstractBaseClass for some of these objects. Since
#
# This file will also retrieve environment variables that can be
# loaded into the project in other places.

import os

MYSQL_USERNAME = os.environ.get('MYSQL_USERNAME')
MYSQL_CXN_URI = os.environ.get('MYSQL_CXN_URI')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_PORT = os.environ.get('MYSQL_PORT')
MYSQL_MARKET_DB = os.environ.get('MYSQL_MARKET_DB')
MYSQL_PRICEHISTORY_DB = os.environ.get('MYSQL_PRICEHISTORY_DB')

TDA_APIKEY = os.environ.get('TDA_APIKEY')
TDA_CONSUMER_ID = os.environ.get('TDA_CONSUMER_ID')

REDDIT_APIKEY = os.environ.get('REDDIT_APIKEY')
REDDIT_USER_AGENT = os.environ.get('REDDIT_USER_AGENT')
REDDIT_CLIENT_ID = os.environ.get('REDDIT_CLIENT_ID')
