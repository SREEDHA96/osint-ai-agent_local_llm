from backend.prompts.evaluation_prompt import EVALUATION_PROMPT_TEMPLATE
import json
from backend.llm_judge import call_claude_opus  # Corrected path

async def evaluate_report(query: str, report: str) -> dict:
    prompt = EVALUATION_PROMPT_TEMPLATE.format(query=query, report=report)

    try:
        response = await call_claude_opus(prompt)  # Await the async call
        return json.loads(response)
    except Exception as e:
        print("❌ Evaluation error:", str(e))
        return {
            "score": 0,
            "accuracy": 0,
            "coherence": 0,
            "completeness": 0,
            "reliability": 0,
            "verdict": "Evaluation failed",
        }

