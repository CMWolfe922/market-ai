#!/usr/bin/env python3

# This script is strictly for retrieving the quote and fundamental data of all the stocks in the
# sqlite database and storing the data into that same database. I will eventually create a
# screener to screen the data stored in the fundamentals and quotes.


from loguru import logger
import time


# Now lets start the main script:
if __name__ == '__main__':
    _start = time.time()
    logger.info("[+] Quote and Fundamental Data Script starting: ")
    # Time the main script
    # =============================================================================== #
    # STEP 1: GET QUOTE AND FUNDAMENTAL DATA INTO A DATABASE:
    # -------------------------------------------------------
    # Right now I can't get it to insert into the docker mysql database. I am going to
    # just import the data into a sqlite database for now as far as fundamentals and
    # quote data. Right now it takes about 1 min 40 secs to get quote data and 1 min
    # 50 secs to get the fundamental data. I need to cut that down significantly.
    # =============================================================================== #

    # [1] Lets retrieve the symbols from the sqlite database:
    from marketdata.models.sqlite_db import _query_symbols
    stocks = _query_symbols()

    # [2] Lets get the Quote and Fundamental data API functions
    from marketdata.company_data import Quote, Fundamental
    quote = Quote(stocks=stocks)
    fundamental = Fundamental(stocks=stocks)

    logger.info('[-] Getting Quote Data...')
    qdata = quote.execute_main()
    logger.success('[+] Quote Data Received.')

    logger.info('[-] Geting Fundamental Data...')
    fdata = fundamental.execute_main()
    _end_quote_data = time.time()
    qdata_runtime = (_end_quote_data - _start) / 60
    logger.success('[+] Fundamental Data Received in {}', qdata_runtime)

    from marketdata.models.sqlite_db import insert_quote_and_fundamental_data, market_db_path
    logger.info("Inserting quote and fundamental data into sqlite database..")
    insert_quote_and_fundamental_data(qdata, fdata)
    logger.success('[+] Inserted quote and fundamental data into {}', market_db_path)


    _end = time.time()
    runtime = (_end - _start) / 60
    logger.success("[ Program Run Time {} ]", runtime)
