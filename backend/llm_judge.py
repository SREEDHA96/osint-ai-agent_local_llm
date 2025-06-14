from backend.utils.ollama_wrapper import call_local_model
import json
import re

def fix_invalid_json_keys(text: str) -> str:
    """
    Adds double quotes around unquoted keys to make it JSON-compatible.
    WARNING: This is a fallback and may not work for deeply nested JSON.
    """
    return re.sub(r'(?<!")(\b\w+\b)(?=\s*:)', r'"\1"', text)

async def call_claude_opus(report: str) -> dict:
    prompt = f"""
You are an evaluation agent.

Evaluate this OSINT report based on the following criteria:
- Accuracy (Is the report factually correct?)
- Coherence (Is it logically structured and easy to follow?)
- Completeness (Does it cover all important points?)
- Reliability (Are sources trustworthy and balanced?)

Return your evaluation strictly as a JSON object, with **all keys in double quotes**:

{{
  "accuracy": 1-10,
  "coherence": 1-10,
  "completeness": 1-10,
  "reliability": 1-10,
  "score": 1-10,
  "verdict": "..."
}}

Report to evaluate:
{report}
"""

    try:
        print("\n📝 Claude Judge Prompt:\n", prompt)
        result = call_local_model(prompt, model="phi3")

        # Auto-fix common LLM formatting issues
        result = fix_invalid_json_keys(result)

        print("\n📊 Claude Judge Fixed Response:\n", result)

        match = re.search(r"\{.*\}", result, re.DOTALL)
        return json.loads(match.group()) if match else {
            "score": 0,
            "verdict": "No valid JSON found in response"
        }

    except Exception as e:
        print("❌ Claude judge error:", e)
        return {
            "score": 0,
            "verdict": f"Evaluation failed: {str(e)}"
        }
