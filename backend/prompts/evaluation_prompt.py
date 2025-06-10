EVALUATION_PROMPT_TEMPLATE = """
You are an expert OSINT report evaluator.

Evaluate the following OSINT report based on:
- Accuracy of information
- Logical coherence
- Completeness (all tasks covered)
- Relevance to the initial query
- Use of reliable sources

Respond with a JSON in this format:
{{
  "score": <integer score from 0 to 10>,
  "strengths": "<key strengths>",
  "weaknesses": "<key weaknesses>",
  "verdict": "<brief verdict summary>"
}}

---

Query:
{query}

Report:
{report}
"""
