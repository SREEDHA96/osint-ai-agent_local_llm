QUERY_ANALYSIS_PROMPT_TEMPLATE = """
You are a query analysis agent.

Your job is to analyze OSINT investigation requests and extract the following:
- Target entity
- Investigation goals
- Relevant OSINT sources (e.g., LinkedIn, OpenCorporates, Twitter, Google News)

Format your output strictly as JSON:
{
  "entity": "...",
  "goals": "...",
  "sources": ["...", "...", "..."]
}

Here is the OSINT query:
\"\"\"{{query}}\"\"\"
"""
