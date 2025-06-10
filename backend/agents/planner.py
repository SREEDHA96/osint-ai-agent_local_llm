from backend.utils.ollama_wrapper import call_local_model
import json
from backend.prompts.planner import PLANNER_SYSTEM_PROMPT

def osint_planning_agent(parsed_json: dict) -> str:
    prompt = f"{PLANNER_SYSTEM_PROMPT.strip()}\n\nParsed Query:\n{json.dumps(parsed_json, indent=2)}"
    return call_local_model(prompt, model="mistral")
