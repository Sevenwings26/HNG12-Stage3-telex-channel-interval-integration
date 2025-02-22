from fastapi import FastAPI, Request
from scraper import scrape_eventbrite_events, logging
# from . import integration.json
import requests

app = FastAPI()

@app.get("/integration.json")
def get_integration_json(request: Request):
    base_url = str(request.base_url).rstrip("/")
    return {
        "data": {
            "descriptions": {
                "app_name": "Tech Event Announcer",
                "app_description": "Fetches tech events from Eventbrite and posts updates to a Telex channel.",
                "app_url": base_url,
                "app_logo": "https://iili.io/39p8VoJ.jpg",
                "background_color": "#HEXCODE"
            },
            "integration_type": "messaging",
            "is_active": True,
            "settings": [
                {"label": "interval", "type": "text", "required": True, "default": "0 * * * *"},
                {"label": "Eventbrite Location", "type": "text", "required": True, "default": "online--tech"}
            ],
            "tick_url": f"{base_url}/tick"
        }
    }

@app.get("/tick")
def tick():
    logging.info("Telex triggered /tick. Fetching events...")
    events = scrape_eventbrite_events("nigeria--lagos/tech-events-in-lagos-2025")

    # Simulate posting to Telex channel
    for event in events:
        post_to_telex(event)

    return {"status": "success", "message": f"Scraped {len(events)} events"}


def post_to_telex(event):
    """
    Simulates sending an event to a Telex channel.
    """
    telex_webhook = "https://ping.telex.im/v1/webhooks/01952892-fa2d-7d0f-9522-1135c1afd2b6"
    payload = {
        "title": event["title"],
        "date": event["date"],
        "location": event["location"],
        "link": event["link"]
    }

    try:
        response = requests.post(telex_webhook, json=payload)
        if response.status_code == 200:
            logging.info(f"Successfully posted event: {event['title']}")
        else:
            logging.error(f"Failed to post event: {response.text}")
    except Exception as e:
        logging.error(f"Error posting to Telex: {e}")
