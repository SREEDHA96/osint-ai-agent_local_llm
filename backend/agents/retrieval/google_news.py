import os
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

def google_news_retrieval(entity: str, num_results=5):
    api_key = os.getenv("SERPAPI_KEY")
    search_url = "https://serpapi.com/search"
    
    params = {
        "q": f"{entity}",
        "tbm": "nws",  # Google News
        "api_key": api_key,
        "num": num_results
    }

    try:
        response = requests.get(search_url, params=params)
    except requests.RequestException as e:
        logger.error("Google News retrieval failed: %s", e)
        return []

    if response.status_code == 200:
        results = response.json().get("news_results", [])
        formatted = [{
            "title": item.get("title"),
            "link": item.get("link"),
            "published": item.get("date"),
            "snippet": item.get("snippet")
        } for item in results]
        return formatted
    else:
        logger.error(
            "Google News API returned %s: %s",
            response.status_code,
            response.text,
        )
        return []
