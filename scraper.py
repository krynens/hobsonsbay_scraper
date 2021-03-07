import os
os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"

from bs4 import BeautifulSoup
from datetime import datetime
import requests
import scraperwiki

today = datetime.today()

for i in range(1, 10):
    url = f'https://hobsonsbay.greenlightopm.com/search-advertising?page={i}&appTypeID=1'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')

    table = soup.find('tbody')
    rows = table.find_all('tr')

    for row in rows:
        record = {}
        record['address'] = row.find_all('td')[3].text.strip().replace('\r\n', ', ')
        date_received_raw = row.find_all('td')[1].text.strip()
        record['date_received'] = datetime.strptime(
            date_received_raw, "%d/%m/%Y").strftime('%Y-%m-%d')
        record['date_scraped'] = today.strftime("%Y-%m-%d")
        record['description'] = row.find_all('td')[2].text.strip()
        record['council_reference'] = row.find_all('td')[0].text.strip()
        record['info_url'] = 'https://hobsonsbay.greenlightopm.com' + \
            str(row.find_all('td')[0]).split('"')[7]

        scraperwiki.sqlite.save(
            unique_keys=['council_reference'], data=record, table_name="data")
