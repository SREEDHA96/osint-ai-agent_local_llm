# backend/llm_judge.py

import os
import json
import re
from dotenv import load_dotenv
from anthropic import AsyncAnthropic

# Load .env variables
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# Instantiate Anthropic client with API key
client = AsyncAnthropic(api_key=api_key)

async def call_claude_opus(report: str) -> dict:
    prompt = f"""
You are an expert evaluator of intelligence reports.

Evaluate the following OSINT report based on four criteria: 
1. Accuracy (Is it factually correct?)
2. Coherence (Is the structure and logic consistent?)
3. Completeness (Are the expected elements covered?)
4. Reliability (Does it cite sources or indicate uncertainty?)

Rate each on a scale of 0 to 10. Then, give an overall score (0–10) and a short final verdict sentence.

### OSINT REPORT START ###
{report}
### OSINT REPORT END ###

Return your answer in this exact JSON format:
{{
  "accuracy": <0-10>,
  "coherence": <0-10>,
  "completeness": <0-10>,
  "reliability": <0-10>,
  "score": <0-10>,
  "verdict": "<short summary verdict>"
}}
"""

    try:
        response = await client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=500,
            temperature=0,
            messages=[{"role": "user", "content": prompt.strip()}]
        )

        # Extract JSON from response text
        match = re.search(r"\{.*\}", response.content[0].text, re.DOTALL)
        return json.loads(match.group()) if match else {"score": 0, "verdict": "Invalid response"}
        
    except Exception as e:
        print("❌ Evaluation Error:", str(e))
        return {"score": 0, "verdict": "Evaluation failed"}
