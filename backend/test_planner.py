import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.planner import osint_planning_agent


if __name__ == "__main__":
    parsed_query = {
      "entity": "Ali Khaledi Nasab",
      "goals": "Investigate public background, social media presence, and business affiliations",
      "sources": ["LinkedIn", "Twitter", "Facebook", "Instagram", "Google Search", "OpenCorporates", "Companies House", "Google News", "Professional networking sites", "Business directories"]
    }

    output = osint_planning_agent(parsed_query)
    print("OSINT Plan:\n", output)
