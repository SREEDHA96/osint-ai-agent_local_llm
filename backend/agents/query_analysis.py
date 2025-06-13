from backend.utils.ollama_wrapper import call_local_model
from backend.prompts.query_analysis import QUERY_ANALYSIS_PROMPT_TEMPLATE

def query_analysis_agent(user_query: str) -> str:
    prompt = QUERY_ANALYSIS_PROMPT_TEMPLATE.replace("{{query}}", user_query)
    print("\n📝 Query Analysis Prompt:\n", prompt)
    return call_local_model(prompt, model="mistral")
