import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime
def feed_scrapper(source, url):
    FEED_URL = url
    resp =  requests.get(FEED_URL, timeout=10)
    resp.raise_for_status()

    # parse as XML
    soup = BeautifulSoup(resp.content, "lxml-xml")
    items = soup.find_all("item")

    entries = []   
    for item in items:
        entry = {
            "title":       item.title.text,
            "link":        item.link.text,
            "pubDate":     item.pubDate.text,
            "description": item.description.text,
            "website":     source,
        }
        date_str = datetime.strptime(entry['pubDate'], '%a, %d %b %Y %H:%M:%S %z')
        entry['pubDate'] = date_str.strftime('%Y-%m-%d %H:%M:%S')
        entries.append(entry)
    return entries
