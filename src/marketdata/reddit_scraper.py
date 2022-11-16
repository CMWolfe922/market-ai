#!/usr/bin/env python3

# ==================================================================== #
# This is a reddit scraper. This file is for extracting data from reddit
# subreccits and store the data into mongodb. Once in mongodb I will be
# able to use it for sentiment analysis.


import praw
import pandas as pd
from itertools import chain, product, groupby,cycle
import logging

logger = logging.getLogger(__name__.__module__)
