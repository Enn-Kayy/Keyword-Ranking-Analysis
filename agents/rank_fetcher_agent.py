from tools.serpapi_tool import fetch_google_results
from agents.rank_analyzer_agent import analyze_organic_ranking, analyze_places_ranking


def fetch_rank_for_keyword(keyword, url):
    """
    Fetches Google ranking information for a single keyword–URL pair.
    Returns both organic ranking and Google Places visibility.
    """

    # Retrieve search results from the Google Search API
    results = fetch_google_results(keyword)

    # Analyze Google Places (Local Pack) ranking if available
    places_rank = analyze_places_ranking(results["places"], url)

    # Analyze organic search ranking and page number
    organic_rank, organic_page = analyze_organic_ranking(results["organic"], url)

    return {
        "google places": places_rank,
        "google links": organic_rank,
        "page number": organic_page
    }
