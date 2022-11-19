import sqlite3 as sql
from sqlalchemy import create_engine

# Grab all the symbols from the database:
def _query_symbols(db):
    """
    :param db: The database to query symbols from.
    """
    conn = sql.connect(db)
    cur = conn.cursor()
    symbols = cur.execute("SELECT symbol FROM companies;")
    return symbols
