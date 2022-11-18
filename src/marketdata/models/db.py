from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from mysql.connector import connect, Error
from loguru import logger
import os.path

# ENVIRONMENT VARIABLES
MYSQL_USER = os.environ.get('MYSQL_DOCKER_USER')
MYSQL_PASSWORD = os.environ.get('MYSQL_DOCKER_PASSWORD')
MYSQL_HOST = os.environ.get('MYSQL_DOCKER_HOST')
MYSQL_PORT = os.environ.get('MYSQL_DOCKER_PORT')
# DATABASES:
# pricehistory
MYSQL_PRICEHISTORY_DB = os.environ.get('MYSQL_DOCKER_PRICEHISTORY_DB')
MYSQL_MARKETDATA_DB = os.environ.get('MYSQL_DOCKER_MARKETDATA_DB')
# CREATE THE LOGGER FOR THIS SCRIPT:
log_path = str(os.path.pardir) + '/logs/'
base_fmt = "[{time:YYYY-MM-DD at HH:mm:ss}]|[{name}-<lvl>{message}</lvl>]"
logger.add(log_path+"main.log", rotation="2 MB",
           colorize=True, enqueue=True, catch=True)

h, u, pw = MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD

# DATABASES FOR INSERTING AND QUERYING DATA FROM:
marketdata_db = MYSQL_MARKETDATA_DB
pricehistory_db = MYSQL_PRICEHISTORY_DB

# CREATE A FUNCTION FOR CONNECTING TO EACH DATABASE:
def create_marketdata_engine(connection_uri):
    DB = MYSQL_MARKETDATA_DB
    connection_uri = connection_uri + "/" + DB
    # connection_uri = create_mysql_uri('mysql', MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST)
    _engine = create_engine(connection_uri, echo=True)
    logger.info("[+] marketdata database engine created successfully")
    return _engine


def create_pricehistory_engine(connection_uri):
    DB = MYSQL_PRICEHISTORY_DB
    connection_uri = connection_uri + "/" + DB
    _engine = create_engine(connection_uri, echo=True)
    logger.info("[+] pricehistory database engine created successfully")
    return _engine



# CREATE A FUNCTION TO SELECT SYMBOLS FROM MYSQL DATABASE
def _select_symbols():
    """Selects rows from table. Give DB name, table name, and
    num of rows to select and display"""
    db = marketdata_db
    table = 'companies'
    query_symbols = f"SELECT symbol FROM {table}"
    try:
        symbols = []
        with connect(host=h, user=u, password=pw, database=db) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query_symbols)
                result = cursor.fetchall()
                for row in result:
                    symbols.append(row[0])
        return symbols
    except Error as e:
        logger.error("[-] Error {} occured", e)


# CREATE A GENERATOR FUNCTION TO SELECT SYMBOLS FROM MYSQL ONE AT A TIME
def generate_symbols():
    data = _select_symbols()
    symbols = [stock for stock in data]
    for symbol in symbols:
        yield symbol


# ========================================================================================== #
# FUNCTIONS TO INSERT QUOTE AND FUNDAMENTAL DATA INTO THE MARKETDATA DATABASE
# ========================================================================================== #

# FUNCTION TO INSERT QUOTE DATA INTO DATABASE


def insert_quote_data_mysql(quote_df, engine):
    """
    :param quote_df: Quote Data Dataframe
    :param engine: database connection variable for mysql
    """
    try:
        quote_df.to_sql(name="quote_data", con=engine,
                        if_exists="append", index=False)
        logger.info("[+] Quote data inserted successfully")
    except:
        logger.error("[-] Quote data not inserted correctly")
        raise ValueError(
            "[-] Data not inserted correctly. Make sure datatype is correct"
        )


# FUNCTION TO INSERT FUNDAMENTAL DATA INTO DATABASE
def insert_fundamental_data_mysql(fun_df, engine):
    """
    :param fun_df: Quote Data Dataframe
    :param db: database connection variable
    """
    try:
        fun_df.to_sql(name="fundamental_data", con=engine,
                      if_exists="append", index=False)
        logger.info("[+] Fundamental Data Inserted")
    except:
        logger.error("[-] Fundamental data not inserted correctly")
        raise ValueError(
            "[-] Data not inserted correctly. Make sure it was a string object."
        )


# FUNCTION TO INSERT THE IMPORTED QUOTE AND FUNDAMENTAL DATA INTO THE DATABASE
def insert_quote_and_fundamental_data_mysql(quote_data, fundamental_data, engine):
    """
    :param quote_data: the quote data from the tdameritrade api
    :param fundamental_data: the fundamental data from the tdameritrade api
    """
    # [1] use the insert_quote_data function imported from models.py
    # to insert quote data into the database.
    insert_quote_data_mysql(quote_data, engine)

    # [2] use the insert_fundamental_data function imported from models.py
    # to insert fundamental data into the database.
    insert_fundamental_data_mysql(fundamental_data, engine)


# ----------------------------------------------------------- #
# CREATE FUNCTION TO INSERT COMPANY DATA FROM STOCKDATA
# ----------------------------------------------------------- #
def _insert_companies(df, table_name="companies"):
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
    engine = create_marketdata_engine()

    df.to_sql(name=table, con=engine, if_exists="replace", index=True)
    # basically this should only work the very first time
    # the program is run and no database exists yet.
