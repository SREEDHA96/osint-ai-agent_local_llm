import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.query_analysis import query_analysis_agent



if __name__ == "__main__":
    input_query = "Investigate Ali Khaledi Nasab’s public background, social media presence, and business affiliations."
    output = query_analysis_agent(input_query)
    print("Parsed Output:\n", output)
