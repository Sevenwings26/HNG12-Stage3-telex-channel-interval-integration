# **Tech Event Announcer**

The **Tech Event Announcer** is a FastAPI-based integration that automatically scrapes tech events from Eventbrite and posts summaries or links to a Telex channel at specified intervals.

---

## **Features**
- **Automated Scraping**: Fetches tech events from Eventbrite based on a specified location.
- **Interval Integration**: Posts event updates to a Telex channel at regular intervals (configurable using crontab syntax).
- **Customizable Settings**: Allows users to configure the Eventbrite location and posting interval.
- **Background Processing**: Uses FastAPI's `BackgroundTasks` to handle scraping and posting asynchronously.

---

## **Prerequisites**
Before running the application, ensure you have the following installed:
- Python 3.8 or higher
- FastAPI
- Uvicorn (for running the FastAPI server)
- Requests (for HTTP requests)
- BeautifulSoup4 (for web scraping)

You can install the required dependencies using:

```bash
pip install fastapi uvicorn requests beautifulsoup4
```

---

## **Setup**

### 1. Clone the Repository
Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/tech-event-announcer.git
cd tech-event-announcer
```

### 2. Run the Application
Start the FastAPI server using Uvicorn:

```bash
uvicorn main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

---

## **Usage**

### 1. Integration Configuration
To configure the integration in Telex:
1. Navigate to the `/integration.json` endpoint:
   ```
   http://127.0.0.1:8000/integration.json
   ```
2. Use the returned JSON schema to set up the integration in Telex.

### 2. Telex Integration
- **Interval**: Set the interval for scraping and posting events (e.g., `0 * * * *` for hourly updates).
- **Eventbrite Location**: Specify the Eventbrite location to scrape (e.g., `nigeria--lagos/tech-events-in-lagos-2025`).

### 3. Testing with Postman
You can test the `/tick` endpoint using Postman:
1. Set the request type to **POST**.
2. Enter the URL:
   ```
   http://127.0.0.1:8000/tick
   ```
3. Add the following JSON payload to the request body:
   ```json
   {
       "channel_id": "01952892-fa2d-7d0f-9522-1135c1afd2b6",
       "return_url": "https://ping.telex.im/v1/webhooks",
       "settings": [
           {
               "label": "interval",
               "type": "text",
               "required": true,
               "default": "0 * * * *"
           },
           {
               "label": "Eventbrite Location",
               "type": "text",
               "required": true,
               "default": "nigeria--lagos/tech-events-in-lagos-2025"
           }
       ]
   }
   ```
4. Send the request. You should receive a `202 Accepted` response.

---

## **Endpoints**

### 1. **GET `/integration.json`**
Returns the integration schema for Telex.

**Example Response**:
```json
{
    "data": {
        "date": {
            "created_at": "2025-02-22",
            "updated_at": "2025-02-22"
        },
        "descriptions": {
            "app_description": "Fetches tech events from Eventbrite and posts updates to a Telex channel.",
            "app_logo": "https://iili.io/39p8VoJ.jpg",
            "app_name": "Tech Event Announcer",
            "app_url": "http://127.0.0.1:8000",
            "background_color": "#4A90E2"
        },
        "integration_category": "Integration",
        "integration_type": "interval",
        "is_active": true,
        "output": [
            {
                "label": "Telex Channel",
                "value": true
            }
        ],
        "key_features": [
            "Scrapes Eventbrite for tech events.",
            "Summarizes and posts updates to a Telex channel.",
            "Posts formatted messages with event details."
        ],
        "permissions": {
            "monitoring_user": {
                "always_online": true,
                "display_name": "Tech Event Monitor"
            }
        },
        "settings": [
            {
                "label": "interval",
                "type": "text",
                "required": true,
                "default": "0 * * * *"
            },
            {
                "label": "Eventbrite Location",
                "type": "text",
                "required": true,
                "default": "nigeria--lagos/tech-events-in-lagos-2025"
            }
        ],
        "tick_url": "http://127.0.0.1:8000/tick"
    }
}
```

### 2. **POST `/tick`**
Called by Telex at the specified interval to fetch and post events.

**Example Payload**:
```json
{
    "channel_id": "01952892-fa2d-7d0f-9522-1135c1afd2b6",
    "return_url": "https://ping.telex.im/v1/webhooks",
    "settings": [
        {
            "label": "interval",
            "type": "text",
            "required": true,
            "default": "0 * * * *"
        },
        {
            "label": "Eventbrite Location",
            "type": "text",
            "required": true,
            "default": "nigeria--lagos/tech-events-in-lagos-2025"
        }
    ]
}
```

**Example Response**:
```json
{
    "status": "accepted"
}
```

---

## **Project Structure**
```
tech-event-announcer/
├── main.py               # FastAPI application and endpoints
├── scraper.py            # Web scraping logic for Eventbrite
├── README.md             # Project documentation
└── requirements.txt      # Python dependencies
```

---

## **Contributing**
Contributions are welcome! If you'd like to contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Submit a pull request.

---

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Support**
For questions or issues, please open an issue on the [GitHub repository](https://github.com/your-username/tech-event-announcer/issues).

---

This `README` provides a clear overview of your project, how to set it up, and how to use it. Let me know if you'd like to add or modify anything!