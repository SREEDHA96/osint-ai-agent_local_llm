# backend/test_query_debug.py

from agents.query_analysis import query_analysis_agent

query = "Investigate Ali Khaledi Nasab’s background"
result = query_analysis_agent(query)
print("Claude output:", result)
