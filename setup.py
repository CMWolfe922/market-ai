from setuptools import setup, find_packages

setup(
	name='marketdata',
	version='0.2.0',
    packages=find_packages(),
	include_package_data=True,
	install_requires=[
		'Click',
		'praw',
		'mysql-connector-python',
		'pandas',
		'sqlalchemy',
		'nltk',
        'scrapy',
        'scrapy-redis',
        'bs4',
        'pandas-ta',
        'redis',
        'pymongo',
        'selenium',
        'requests',
        'yfinance',
        'humanize',
        'loguru',
        'newspaper3k',
	],
 entry_points={
        'console_scripts': [
            'stockdata = marketdata.scripts.stockdata:cli',
        ],
    },
)
