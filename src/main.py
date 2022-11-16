from loguru import logger
import time



# first lets retrieve all the company symbols
from marketdata.models.sqlite_db import _query_symbols
# Get the stocks
stocks = _query_symbols()
# Now lets import the fundamental and quote objects to retrieve that data
# for each symbol
from marketdata.company_data import Quote, Fundamental

quote = Quote(stocks=stocks)
fundamental = Fundamental(stocks=stocks)

# Now lets start the main script:
if __name__ == '__main__':
    logger.info("[+] Main Script starting for quote and fundamental data: ")
    # Time the main script
    # =============================================================================== #
    # STEP 1: GET QUOTE AND FUNDAMENTAL DATA INTO THE DATABASE
    # =============================================================================== #
    # Since my mysql connection isn't working I am going to have to save the quote
    # and fundamental data into a variable and then pass it to the big insert method
    # insert_quote_and_fundamental_data
    logger.info('[-] Getting Quote Data...')
    qdata = quote.execute_main()
    logger.info('[+] Quote Data Received.')

    logger.info('[-] Geting Fundamental Data...')
    fdata = fundamental.execute_main()
    logger.success('[+] Fundamental Data Received.')

    from marketdata.models.sqlite_db import insert_quote_and_fundamental_data, market_db_path
    logger.info("Inserting quote and fundamental data into sqlite database..")
    insert_quote_and_fundamental_data(qdata, fdata)
    logger.success('[+] Inserted quote and fundamental data into {}', market_db_path)
