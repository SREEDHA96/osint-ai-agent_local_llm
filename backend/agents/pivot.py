from backend.utils.ollama_wrapper import call_local_model
import json
from backend.prompts.pivot import PIVOT_AGENT_PROMPT_TEMPLATE

def pivot_agent(articles: list, current_entity: str) -> str:
    if not articles:
        return json.dumps({
            "related_entities": [],
            "new_queries": [],
            "inconsistencies": ["No articles provided."],
            "notes": "No data to pivot on."
        }, indent=2)

    prompt = PIVOT_AGENT_PROMPT_TEMPLATE.format(entity=current_entity) + "\n\nArticles:\n" + json.dumps(articles, indent=2)
    try:
        return call_local_model(prompt, model="qwen:7b")
    except Exception as e:
        return json.dumps({
            "related_entities": [],
            "new_queries": [],
            "inconsistencies": ["Pivot agent failed to generate valid output."],
            "notes": f"Error: {str(e)}"
        }, indent=2)
