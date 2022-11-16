#!/usr/bin/env python3

# this class is used to build the market data functionality. Using the scripts dir and
# the other files in this directory I will build a fully functioning data aggregation
# tool

import pandas as pd
from sqlalchemy import create_engine
import mysql.connector as mysql
import os
from loguru import logger

# ENVIRONMENT VARIABLES
MYSQL_USER = os.environ.get('MYSQL_DOCKER_USER')
MYSQL_PASSWORD = os.environ.get('MYSQL_DOCKER_PASSWORD')
MYSQL_HOST = os.environ.get('MYSQL_DOCKER_HOST')
MYSQL_PORT = os.environ.get('MYSQL_DOCKER_PORT')
# DATABASES:
# pricehistory
MYSQL_PRICEHISTORY_DB = os.environ.get('MYSQL_DOCKER_PRICEHISTORY_DB')
MYSQL_MARKETDATA_DB = os.environ.get('MYSQL_DOCKER_MARKETDATA_DB')


def get_marketdata_cursor(**config):
    """Connect to mysql marketdata database and return the cursor or connection object"""
    try:
        cnx = mysql.connect(**config)
        cur = cnx.cursor()
        return cur
    except Exception as e:
        logger.error("Unable to connect to marketdata database:")

def get_pricehistory_cursor(**config):
    """Connect to mysql pricehistory database and return the cursor or connection object"""
    try:
        cnx = mysql.connect(**config)
        cur = cnx.cursor()
        return cur
    except Exception as e:
        logger.error("Unable to connect to marketdata database:")




class DataModelBuilder(object):

    def __init__(self, database, *args, **kwargs):
        self.database = database
        self.args = args
        self.kwargs = kwargs

def create_table(self, engine, table_name, df, columns):
    """This will dynamically create a table using a pandas dataframe and a sqlalchemy engine object."""
    pass
