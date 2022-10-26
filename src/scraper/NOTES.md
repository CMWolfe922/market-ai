# Web Scraping Notes:

---

> I am going to be building multiple spiders and scrapers so I will need as much documentation as possible in the future.

## Places Spider:

---

> This is a spider that will be used to crawl web pages looking for locations. Things like all of the mcdonalds addresses. Or addresses for every lawyers office on google. As well as AA Meetings and NA Meetings.

- It is going to be saving these locations in the docker MongoDB database.
  - Since the docker container uses the same port as mongo locally, I may have to just use the local mongodb version unless I can change Dockers MongoDB port.
