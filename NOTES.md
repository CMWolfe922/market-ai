# Web Scraping Notes:

---

> I am going to be building multiple spiders and scrapers so I will need as much documentation as possible in the future.

## Places Spider:

---

> This is a spider that will be used to crawl web pages looking for locations. Things like all of the mcdonalds addresses. Or addresses for every lawyers office on google. As well as AA Meetings and NA Meetings.

- It is going to be saving these locations in the docker MongoDB database.
  - Since the docker container uses the same port as mongo locally, I may have to just use the local mongodb version unless I can change Dockers MongoDB port.


## Project Structure:
---

src
|___financial
      |
      |___marketdata
      |      |
      |      |___config
      |      |      |__`__init__.py`
      |      |      |__config.cfg
      |      |      |__config.ini
      |      |      |__example_config.ini
      |      |      |__secrets.py
      |      |
      |      |____db
      |      |      |__`__init__.py`
      |      |      |__db.py
      |      |      |__models.py
      |      |      |__peewee.py
      |      |
             |__`__init__.py`
             |__funcs.py
             |__MarketDatabase.db
             |__scratch.py
             |__settings_marketdata.py
             |__stockdata.py
             |__urls.py
