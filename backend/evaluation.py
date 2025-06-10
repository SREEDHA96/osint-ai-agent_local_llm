import anthropic
import os
import json
import re

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def call_claude_opus(report: str, query: str) -> dict:
    prompt = f"""
You are an expert OSINT evaluation agent. Given the following original query and the AI-generated report, evaluate the report on:

1. **Accuracy** (Are the facts correct?)
2. **Coherence** (Is the report logically structured and readable?)
3. **Completeness** (Are all parts of the query addressed?)
4. **Reliability** (Does the report cite verifiable and trustworthy sources?)

Give each score from 1 to 10. Also provide a short summary verdict.

---

**QUERY**:
{query}

---

**REPORT**:
{report}

---

Respond strictly in this JSON format:
{{
  "accuracy": int,
  "coherence": int,
  "completeness": int,
  "reliability": int,
  "verdict": "string"
}}
"""

    try:
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            temperature=0,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        content = response.content[0].text.strip()
        json_block = re.search(r"\{.*\}", content, re.DOTALL)
        return json.loads(json_block.group()) if json_block else {
            "accuracy": 0,
            "coherence": 0,
            "completeness": 0,
            "reliability": 0,
            "verdict": "Evaluation format error."
        }

    except Exception as e:
        print("❌ Claude Opus evaluation failed:", e)
        return {
            "accuracy": 0,
            "coherence": 0,
            "completeness": 0,
            "reliability": 0,
            "verdict": f"Evaluation failed: {str(e)}"
        }
