import requests
from bs4 import BeautifulSoup
import time
import logging


HEADERS = {"User-Agent": "Mozilla/5.0"}

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def scrape_eventbrite_events(eventbrite_endpoint: str):
    url = f"https://www.eventbrite.com/d/{eventbrite_endpoint}"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    events = []
    for item in soup.find_all("div", class_="SearchResultPanelContentEventCardList-module__map_experiment_event_card___vyRC3"):
        title_tag = item.find("h3")
        link_tag = item.find("a")

        title = title_tag.text.strip() if title_tag else "No title"
        link = link_tag["href"] if link_tag else "No link"

        events.append({"title": title, "link": link})

    for event in events:
        event_url = event["link"]
        try:
            event_response = requests.get(event_url, headers=HEADERS)
            event_soup = BeautifulSoup(event_response.text, "html.parser")

            date_tag = event_soup.find("time")
            event["date"] = date_tag.text.strip() if date_tag else "No date found"

            location_tag = event_soup.find("div", class_="location-info__address")
            event["location"] = location_tag.text.strip() if location_tag else "No location found"

            logging.info(f"Scraped event: {event['title']}")
            time.sleep(12)  # Delay to avoid bot detection
        except Exception as e:
            logging.error(f"Failed to fetch event details: {e}")

    return events

