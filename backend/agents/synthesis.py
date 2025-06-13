from backend.utils.ollama_wrapper import call_local_model
import json

def synthesis_agent(entity: str, plan: dict, articles: list, pivots: dict) -> str:
    prompt = f"""You are an OSINT Synthesis Agent. Write a structured Markdown report for: {entity}
Plan: {json.dumps(plan, indent=2)}
Articles: {json.dumps(articles, indent=2)}
Pivot Insights: {json.dumps(pivots, indent=2)}
"""
    print("\n📝 Synthesis Prompt:\n", prompt)
    return call_local_model(prompt, model="zephyr")
