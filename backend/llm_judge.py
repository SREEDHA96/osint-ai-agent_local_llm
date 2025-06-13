from backend.utils.ollama_wrapper import call_local_model
import json
import re

async def call_claude_opus(report: str) -> dict:
    prompt = f"""
Evaluate this OSINT report based on:
- Accuracy
- Coherence
- Completeness
- Reliability

Return strict JSON:
{{
  "accuracy": 1-10,
  "coherence": 1-10,
  "completeness": 1-10,
  "reliability": 1-10,
  "score": 1-10,
  "verdict": "..."
}}

Report:
{report}
"""

    try:
        print("\n📝 Claude Judge Prompt:\n", prompt)
        result = call_local_model(prompt, model="phi3")
        print("\n📊 Claude Judge Raw Response:\n", result)
        match = re.search(r"\{.*\}", result, re.DOTALL)
        return json.loads(match.group()) if match else {"score": 0, "verdict": "Invalid response"}
    except Exception as e:
        print("❌ Claude judge error:", e)
        return {"score": 0, "verdict": str(e)}
