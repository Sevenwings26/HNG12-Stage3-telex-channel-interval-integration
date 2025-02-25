from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from typing import List
import httpx
import asyncio
from scraper import scrape_eventbrite_events, logging

app = FastAPI()

# Pydantic model for the payload sent to /tick
class Setting(BaseModel):
    label: str
    type: str
    required: bool
    default: str

class TickPayload(BaseModel):
    channel_id: str
    return_url: str
    settings: List[Setting]

# Endpoint to return the integration schema
@app.get("/integration.json")
def get_integration_json(request: Request):
    base_url = str(request.base_url).rstrip("/")
    return {
        "data": {
            "date": {
                "created_at": "2025-02-22",
                "updated_at": "2025-02-22"
            },
            "descriptions": {
                "app_description": "Fetches tech events from Eventbrite and posts updates to a Telex channel.",
                "app_logo": "https://iili.io/39p8VoJ.jpg",
                "app_name": "Tech Event Announcer",
                "app_url": base_url,
                "background_color": "#4A90E2"
            },
            "integration_category": "Email & Messaging",
            "integration_type": "interval",
            "is_active": True,
            "output": [
                {
                    "label": "Telex Channel",
                    "value": True
                }
            ],
            "key_features": [
                "Scrapes Eventbrite for tech events.",
                "Posts formatted messages with event details."
            ],
            "permissions": {
                "monitoring_user": {
                    "always_online": True,
                    "display_name": "Tech Event Monitor"
                }
            },
            "settings": [
                {
                    "label": "interval",
                    "type": "text",
                    "required": True,
                    "default": "0 * * * *" 
                },
                {
                    "label": "Eventbrite Location",
                    "type": "text",
                    "required": True,
                    "default": "nigeria--lagos/tech-events-in-lagos-2025"
                }
            ],
            "target_url": "https://ping.telex.im/v1/webhooks/01953bed-1c28-7197-9774-4babc14d6268",
            "tick_url": f"{base_url}/tick"
        }
    }


# Background task to scrape events and post to Telex
async def post_events_to_telex(payload: TickPayload):
    # Extract Eventbrite location from settings
    eventbrite_location = next(
        (s.default for s in payload.settings if s.label == "Eventbrite Location"),
        "nigeria--lagos/tech-events-in-lagos-2025"
    )

    # Scrape events
    events = scrape_eventbrite_events(eventbrite_location)

    # Format and post each event to Telex
    for event in events:
        message = (
            f"**{event['title']}**\n"
            f"Date: {event['date']}\n"
            f"Location: {event['location']}\n"
            f"Link: {event['link']}"
        )

        data = {
            "message": message,
            "username": "Iyanu",
            "event_name": "Tech Event Update",
            "status": "info"
        }

        async with httpx.AsyncClient() as http_client:
            try:
                response = await http_client.post(
                    "https://ping.telex.im/v1/webhooks/01953bed-1c28-7197-9774-4babc14d6268", #change to channel_url
                    json=payload.model_dump(),
                    headers={
                        "Accept" : "application/json",
                        "Content-Type": "application/json"}
                )
                return response.json()
            except:
                return JSONResponse({"error": "Error communicating with telex"})


        # # Post to Telex using the return_url
        # async with httpx.AsyncClient() as client:
        #     try:
        #         response = await client.post("https://ping.telex.im/v1/webhooks/01953bed-1c28-7197-9774-4babc14d6268", json=payload,
        #         headers={
        #             "Accept": "application/json",
        #             "Content-Type": "application/json"
        #         })
        #         if response.status_code == 200:
        #             logging.info(f"Posted event to Telex: {event['title']}")
        #         else:
        #             logging.error(f"Failed to post event: {response.text}")
        #     except Exception as e:
        #         logging.error(f"Error posting to Telex: {e}")


@app.post("/tick", status_code=202)
def tick(payload: TickPayload, background_tasks: BackgroundTasks):
    background_tasks.add_task(post_events_to_telex, payload)
    return {"status": "accepted"}


