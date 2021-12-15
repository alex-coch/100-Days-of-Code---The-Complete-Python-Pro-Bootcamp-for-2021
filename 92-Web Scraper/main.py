import requests
from csv import writer
from bs4 import BeautifulSoup

BASE_URL = "https://mbp.opole.pl/wydarzenia/?pno_past="
page = 1


all_events = []
next_page = True

while next_page:
    response = requests.get(f'{BASE_URL}{page}')
    soup = BeautifulSoup(response.text, "html.parser")
    archive = soup.find(id="panel-4-1-0-1")
    events = archive.find_all(class_="event-meta-data")
    if events == []:
        next_page = False
        break
    for event in events:
        name = event.find("a").get_text()
        location = event.find(class_="meta-location").get_text()
        date = event.find(class_="meta-date").get_text()
        all_events.append([name, location, date])
        print(name, location, date)
    page += 1

with open("events_mbp.csv", "w", encoding="utf-16", newline='') as csv_file:
    csv_writer = writer(csv_file)
    csv_writer.writerow(["name", "location", "date"])
    csv_writer.writerows(all_events)