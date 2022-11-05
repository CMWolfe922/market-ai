import mysql.connector as mysql
from sqlalchemy import create_engine
import sqlite3 as sql
import os

db_path = "/home/blackwolf/dev/projects/finance/market-ai/"
db = os.path.join(db_path, "marketdata.db")
