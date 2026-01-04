from langgraph.graph import StateGraph, END
from agents.keyword_reader_agent import read_keywords
from agents.rank_fetcher_agent import fetch_rank_for_keyword
from agents.report_agent import generate_excel_report


def keyword_reader_node(state):
    """
    Reads the input Excel file and loads keyword–URL pairs
    into the shared graph state.
    """
    state["keywords"] = read_keywords(state["input_file"])
    return state


def rank_checker_node(state):
    """
    Iterates through each keyword–URL pair and fetches
    Google Places and organic ranking data.
    """
    results = []

    for item in state["keywords"]:
        keyword = item["keyword"]
        url = item["url"]

        rank_data = fetch_rank_for_keyword(keyword, url)

        results.append({
            "keyword": keyword,
            "url": url,
            "google places": rank_data["google places"],
            "google links": rank_data["google links"],
            "page number": rank_data["page number"]
        })

    state["final_results"] = results
    return state


def report_node(state):
    """
    Generates the final Excel report from the aggregated
    keyword ranking results.
    """
    generate_excel_report(state["final_results"])
    return state


def build_graph():
    """
    Defines and compiles the LangGraph workflow for the
    keyword ranking analysis pipeline.
    """
    graph = StateGraph(dict)

    graph.add_node("reader", keyword_reader_node)
    graph.add_node("rank_checker", rank_checker_node)
    graph.add_node("report", report_node)

    graph.set_entry_point("reader")
    graph.add_edge("reader", "rank_checker")
    graph.add_edge("rank_checker", "report")
    graph.add_edge("report", END)

    return graph.compile()
