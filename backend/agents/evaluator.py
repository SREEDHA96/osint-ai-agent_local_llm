from backend.prompts.evaluation_prompt import EVALUATION_PROMPT_TEMPLATE
import json
from backend.utils.ollama_wrapper import call_local_model

async def evaluate_report(query: str, report: str) -> dict:
    prompt = EVALUATION_PROMPT_TEMPLATE.format(query=query, report=report)
    print("\n📝 Evaluation Prompt:\n", prompt)

    try:
        response = call_local_model(prompt, model="phi3")
        print("\n📊 Evaluation Raw Response:\n", response)
        return json.loads(response)
    except Exception as e:
        print("❌ Evaluation error:", str(e))
        return {
            "score": 0,
            "accuracy": 0,
            "coherence": 0,
            "completeness": 0,
            "reliability": 0,
            "verdict": "Evaluation failed"
        }
