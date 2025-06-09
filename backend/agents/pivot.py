from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def pivot_agent(articles: list, current_entity: str) -> str:
    if not articles:
        return json.dumps({
            "related_entities": [],
            "new_queries": [],
            "inconsistencies": ["No articles provided."],
            "notes": "No data to pivot on."
        }, indent=2)

    prompt = f"""
You are an OSINT Pivot Agent.

Your job is to analyze open-source intelligence retrieved for the entity: **{current_entity}**.

Below is a list of news articles or content chunks in JSON format:

{json.dumps(articles, indent=2)}

Extract the following strictly in JSON format:
{{
  "related_entities": [{{"name": "...", "relation": "...", "event": "..."}}, ...],
  "new_queries": ["...", "...", "..."],
  "inconsistencies": ["...", "..."],
  "notes": "Summarize key points or unresolved leads."
}}

ONLY output pure JSON. No explanation. No markdown. No commentary.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt.strip()}],
            temperature=0.2,
            max_tokens=1000
        )
        content = response.choices[0].message.content.strip()

        # 💡 Force strip Markdown formatting
        if content.startswith("```json"):
            content = content[7:].strip()
        if content.endswith("```"):
            content = content[:-3].strip()

        # Try parsing here to catch issues earlier
        json.loads(content)
        return content

    except Exception as e:
        return json.dumps({
            "related_entities": [],
            "new_queries": [],
            "inconsistencies": ["Pivot agent failed to generate valid output."],
            "notes": f"Error: {str(e)}"
        }, indent=2)
