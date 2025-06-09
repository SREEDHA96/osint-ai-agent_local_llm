import os
import requests
from dotenv import load_dotenv

load_dotenv()

def google_news_retrieval(entity: str, num_results=5):
    api_key = os.getenv("SERPAPI_KEY")
    search_url = "https://serpapi.com/search"
    
    params = {
        "q": f"{entity}",
        "tbm": "nws",  # Google News
        "api_key": api_key,
        "num": num_results
    }

    response = requests.get(search_url, params=params)

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
        return {"error": response.text}
