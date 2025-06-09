# backend/agents/synthesis.py

import os
import json
from dotenv import load_dotenv
from openai import OpenAI  # Replace with Gemini SDK if needed

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("GEMINI_API_KEY"))  # Swap with Gemini client if using Vertex AI, etc.

def synthesis_agent(entity: str, plan: dict, articles: list, pivots: dict) -> str:
    """
    Synthesize a full OSINT report using all previous agent outputs.
    """

    prompt = f"""
You are an OSINT Synthesis Agent.

Your job is to generate a comprehensive, structured OSINT intelligence report based on multi-agent investigation data.
You will receive:
1. The entity and investigation goal
2. A prioritized OSINT collection plan
3. A list of retrieved articles or content chunks
4. Pivot analysis insights (related entities, new queries, inconsistencies, notes)

Return the final intelligence report as structured Markdown with sections:

# OSINT Intelligence Report: {entity}

## Executive Summary
Summarize key findings in 3–5 bullet points.

## Investigation Objectives
Clearly list the investigation goals.

## Information Sources & Retrieval Log
Categorize sources used (web, social, academic, public records) and how many results per source.

## Key Findings
- Social & Professional Background
- Business or Academic Affiliations
- Public Appearances & Events
- Related People/Orgs
- Potential Risks

## Inconsistencies or Gaps
List contradictions, red flags, and missing data.

## Follow-Up Queries
List suggested directions for further investigation.

## Appendix: Retrieved Snippets
Include titles, sources, and summary of each retrieved item.

## Confidence & Attribution
For each section, rate confidence (High/Medium/Low) and mention source reliability.

---

OSINT Collection Plan:
{json.dumps(plan, indent=2)}

Retrieved Articles:
{json.dumps(articles, indent=2)}

Pivot Insights:
{json.dumps(pivots, indent=2)}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Replace with Gemini 1.5 Pro call if available
            messages=[{"role": "user", "content": prompt.strip()}],
            temperature=0.3,
            max_tokens=3000
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ Error during synthesis: {e}"
