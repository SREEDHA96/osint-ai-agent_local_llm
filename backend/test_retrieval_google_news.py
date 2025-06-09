# backend/test_retrieval_google_news.py

import sys
import os

# Add the parent directory (project root) to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.retrieval.google_news import google_news_retrieval

if __name__ == "__main__":
    entity = "Ali Khaledi Nasab"
    results = google_news_retrieval(entity)

    if isinstance(results, dict) and "error" in results:
        print("❌ Retrieval Error:", results["error"])
    else:
        for r in results:
            print("\n📰", r["title"])
            print("🔗", r["link"])
            print("📅", r["published"])
            print("📝", r["snippet"])
