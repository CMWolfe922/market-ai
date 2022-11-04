#!/usr/bin/env python3

# Basic TestCase file for testing the financial data functions
# Basic imports
from unittest import TestCase
import os
from loguru import logger
# import the functions
from ..src.marketdata.financialdata.stock_prices import price_history


# Create the Logger for the test cases
tempdir = "~/dev/projects/finance/market-ai/tmp"
log_file = os.path.join(tempdir,__file__)
format = "{time:MM-DD-YYYY at HH:mm:ss}:{level} | {message}: "
logger.add(log_file, format=format, diagnose=True, backtrace=True, colorize=True)


class TestFinancialData(TestCase):

    def test_financial_price_history_data_is_df(self):
        """TestCase to see that this function returns a DataFrame each time"""
        logger.info("Starting the price_history test..")
        pass
