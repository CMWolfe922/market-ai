import mysql.connector as mysql
from mysql.connector import connect, Error
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
import sqlite3 as sql
import os
from loguru import logger

# import MySQL environment variables from utils.retrieve file
from utils.retrieve import MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_HOST
from utils.retrieve import MYSQL_PRICEHISTORY_DB, MYSQL_MARKET_DB
from utils.retrieve import MYSQL_CXN_URI

PATH = "../tmp/"
FILE = "scraper.log"
LOG_FILE = os.path.join(PATH, FILE)
logger.add(LOG_FILE, format="{time:MM/DD/YYYY at HH:mm:ss} | {level} | {name} | {message}", diagnose=True, backtrace=True)


db_path = "/home/blackwolf/dev/projects/finance/market-ai/"
db = os.path.join(db_path, "marketdata.db")

def get_sqlite_database_uri(database=db):
    """Function that returns the URI to the sqlite database for testing"""
    sqlite_db = {'drivername': 'sqlite', 'database': db}
    sqlite_db_uri = URL(**sqlite_db)
    return sqlite_db_uri

# ----------------------------------------------------------- #
# CREATE FUNCTION TO INSERT COMPANY DATA FROM STOCKDATA
# ----------------------------------------------------------- #
def _insert_companies(company_df, table_name="companies"):
    """
    :param company_df: pandas DataFrame of list of companies

    :param table_name: name of table to save data to in database
    """

    table = table_name
    db = get_sqlite_database_uri()
    df = company_df

    logger.info("Create sqlalchemy engine object..")
    engine = create_engine(db)
    logger.info("[+] Create connection using engine to database {}.. ", db)
    conn = engine.connect() # create database
    df.to_sql(name=table, con=conn, if_exists="replace", index=True)
    conn.close()
    logger.success("[+] Insert data to {} table in {}. Then close engine connection ", table, db)


def get_mysql_database_uri():
    """This function returns the URI to connect to a MySQL database"""
    mysql_db = {
        'drivername': 'mysql',
        'username': MYSQL_USERNAME,
        'password': MYSQL_PASSWORD,
        'host': MYSQL_HOST,
        'port': MYSQL_PORT,
    }
    mysql_db_uri = URL(**mysql_db)
    return mysql_db_uri


class DB:
    """Database class that holds information about whichever database
    gets instantiated. There will only be a few possible options for
    instantiating this class."""

    def __init__(self, db_type:str, database:str=None):
        if db_type == 'mysql':
            if database is None:
                logger.error("database arg required to create a MySQL database connection...")
            else:
                self.mysql_uri=get_sqlite_database_uri()
