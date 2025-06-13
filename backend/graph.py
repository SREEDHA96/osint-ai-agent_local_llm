# backend/graph.py

from langgraph.graph import StateGraph
from typing import TypedDict
import json

from .utils.json_utils import extract_json

from .agents.query_analysis import query_analysis_agent
from .agents.planner import osint_planning_agent
from .agents.retrieval.google_news import google_news_retrieval
from .agents.pivot import pivot_agent
from .agents.synthesis import synthesis_agent
from .database import save_investigation


# Define the shared state schema for LangGraph
class GraphState(TypedDict):
    input: str
    parsed_query: dict
    task_plan: dict
    retrieved_chunks: list
    pivot_insights: dict
    retrieval_log: list
    final_report: str

# Node 1: Query Analysis

def query_node(state: GraphState) -> dict:
    raw = query_analysis_agent(state["input"])
    print("\n📤 DEBUG: Raw Claude response:", raw)

    try:
        parsed = extract_json(raw)
    except ValueError as e:
        raise ValueError("query_analysis_agent returned invalid JSON") from e

    print("🧪 Cleaned Claude response:\n", json.dumps(parsed, indent=2))

    return {"parsed_query": parsed}

# Node 2: Planning

def planner_node(state: GraphState) -> dict:
    parsed_query = state["parsed_query"]
    raw = osint_planning_agent(parsed_query)
    print("🧭 DEBUG: Raw Plan Output:", repr(raw))

    try:
        plan = extract_json(raw)
    except ValueError as e:
        raise ValueError("osint_planning_agent returned invalid JSON") from e

    print("🧪 Cleaned Plan Output:\n", json.dumps(plan, indent=2))

    return {"task_plan": plan}

# Node 3: Retrieval

def retriever_node(state: GraphState) -> dict:
    entity = state["parsed_query"]["entity"]
    results = google_news_retrieval(entity)
    print("\n🔎 Retrieved", len(results), "articles from Google News")

    retrieval_log = [
        {
            "source": "Google News",
            "query": entity,
            "num_results": len(results)
        }
    ]
    return {
        "retrieved_chunks": results,
        "retrieval_log": retrieval_log
    }

# Node 4: Pivoting

def pivot_node(state: GraphState) -> dict:
    raw = pivot_agent(state["retrieved_chunks"], state["parsed_query"]["entity"])
    print("\n🧠 Pivot Agent Output:\n", raw)

    try:
        parsed = extract_json(raw)
    except ValueError as e:
        print("❌ Failed to parse pivot agent output:", e)
        parsed = {
            "related_entities": [],
            "new_queries": [],
            "inconsistencies": ["Failed to parse pivot output"],
            "notes": raw,
        }
    print("🧠 Parsed Pivot Insights:\n", json.dumps(parsed, indent=2))

    return {"pivot_insights": parsed}

# Node 5: Synthesis

def synthesis_node(state: GraphState) -> dict:
    print("\n🧩 Using Pivot Insights:\n", json.dumps(state["pivot_insights"], indent=2))
    report = synthesis_agent(
        entity=state["parsed_query"]["entity"],
        plan=state["task_plan"],
        articles=state["retrieved_chunks"],
        pivots=state["pivot_insights"]
    )
    print("\n📄 Final Report Generated.\n")

    # ✅ Save results to DB
    save_investigation({
        **state,
        "final_report": report
    })

    return {"final_report": report}

# Build LangGraph pipeline

def build_langgraph() -> StateGraph:
    """Compile and return the LangGraph pipeline."""
    builder = StateGraph(GraphState)

    builder.add_node("QueryAnalysis", query_node)
    builder.add_node("Planner", planner_node)
    builder.add_node("Retriever", retriever_node)
    builder.add_node("Pivot", pivot_node)
    builder.add_node("Synthesis", synthesis_node)

    builder.set_entry_point("QueryAnalysis")
    builder.add_edge("QueryAnalysis", "Planner")
    builder.add_edge("Planner", "Retriever")
    builder.add_edge("Retriever", "Pivot")
    builder.add_edge("Pivot", "Synthesis")

    builder.set_finish_point("Synthesis")

    graph = builder.compile()
    return graph


async def run_langgraph(query: str):
    """Convenience helper to run the pipeline for a single query."""
    graph = build_langgraph()
    return await graph.ainvoke({"input": query})


# Run if executed directly
if __name__ == "__main__":
    import asyncio

    query = "Investigate Ali Khaledi Nasab’s social and professional background across public records."
    result = asyncio.run(run_langgraph(query))

    print("\n🎯 Final Graph State:\n")
    for key, val in result.items():
        print(f"--- {key.upper()} ---")
        if isinstance(val, (dict, list)):
            print(json.dumps(val, indent=2), "\n")
        else:
            print(val, "\n")

