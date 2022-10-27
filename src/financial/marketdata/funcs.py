#!/usr/bin/env python3

from stockdata import Get
import sqlite3 as sql
from stockdata import companies
import os.path
import pandas as pd


# ----------------------------------------------------------- #
# CREATE FUNCTION TO CHECK IF A DATABASE EXISTS
# ----------------------------------------------------------- #
# name of database will be created in the main file
def check_for_database(db_name):
    """
    :param db_name: name of the database to check for existence
    :return: True if the database exists, False if not
    """
    db = db_name
    if not os.path.exists(db): return False
    else: return True

# ----------------------------------------------------------- #
# CREATE FUNCTION TO QUERY SYMBOLS FROM DB IF IT EXISTS
# ----------------------------------------------------------- #
def query_symbols(db_name, table_name):
    """
    :param db_name: name of database to retrieve symbols from
    :param table_name: name of table symbols are saved in

    :return: all the stock symbols in a list to be chunked
    """
    table = table_name
    db = db_name
    symbols = []
    try:
        if os.path.exists(db):
            query_symbols = f"SELECT symbol FROM {table} "
            conn = sql.connect(db)
            cur = conn.cursor()
            for row in cur.execute(query_symbols):
                symbols.append(row)

        elif not os.path.exists(db):
            pass

    finally:
        if len(symbols) > 2:
            return symbols


# ----------------------------------------------------------- #
# CREATE FUNCTION TO INSERT COMPANY DATA FROM STOCKDATA
# ----------------------------------------------------------- #

def insert_companies(company_df, db_name, table_name):
    """
    :param company_df: pandas DataFrame of list of companies
    :param db_name: name of database to insert data into
    :param table_name: name of table to save data to in database

    :return: Message stating companies were inserted correctly
    or a message saying database and table already exists. If
    table and database already exists, then the query_symbols
    function will be called
    """

    table = table_name
    db = db_name
    df = company_df
    try:
        if not os.path.exists(db):  # if path to database doesn't exist
            conn = sql.connect(db)  # create database
            print(f"[+] {db} database created!.. ")
            df.to_sql(name=table, con=conn, if_exists="replace", index=True)
            conn.close()
            print(
                f"[+] Company data inserted into {db} and saved in {table} table... ")
            # basically this should only work the very first time
            # the program is run and no database exists yet.

    finally:
        if os.path.exists(db):
            print(
                f"[-] Company data already exists in the {table} table in {db} database... ")

# create a Get object
get = Get()

# ----------------------------------------------------------- #
# CREATE FUNCTION TO CHECK FOR DATABASE EXISTENCE, IF NO DATABASE
# EXISTS, CREATE ONE AND INSERT COMPANY DATA IN DATABASE
# ----------------------------------------------------------- #

def get_symbol(db_name, table_name):
    """
    :description: Check if the database exists, if not call the
    get.companies() method, create the database and insert the
    company data. Else if the database already exists, query the
    database and retrieve the symbols.
    """
    db = db_name
    table = table_name

    # database check
    confirmed = check_for_database(db)
    if not confirmed:
        # print message saying db doesn't exist
        print(f"{db} not found...")
        # retrieve the company data from get.companies() method
        companies_df =  get.companies()
        # create the database
        conn = sql.connect(db)
        print(f"[+] {db} created!..")
        companies_df.to_sql(name=table, con=conn, if_exists="replace", index=True)
