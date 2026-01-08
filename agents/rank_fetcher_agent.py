from tools.serpapi_tool import fetch_google_results_page
from tools.places_scraper_tool import scrape_google_places
from agents.rank_analyzer_agent import (
    analyze_organic_ranking,
    analyze_places_ranking
)

DEBUG_RANK_FETCHER = True


def fetch_rank_for_keyword(keyword, url, max_pages=3):
    """
    Fetches Google ranking information for a single keyword–URL pair.
    Uses:
    - Google Maps scraping for Places rank
    - SerpAPI for Organic rank (with early stopping)
    """

    if DEBUG_RANK_FETCHER:
        print("\n🏢 DEBUG → Scraping Google Places for ranking")

    scraped_places = scrape_google_places(keyword)
    places_rank = analyze_places_ranking(scraped_places, url)

    all_organic_results = []
    organic_rank = "Not Found"
    organic_page = "N/A"

    for page in range(max_pages):

        if DEBUG_RANK_FETCHER:
            print(f"\n🚀 DEBUG → Fetching organic results page {page + 1}")

        results = fetch_google_results_page(keyword, page)

        organic_results = results.get("organic", [])
        if not organic_results:
            if DEBUG_RANK_FETCHER:
                print("⚠️ DEBUG → No organic results, stopping")
            break

        all_organic_results.extend(organic_results)

        organic_rank, organic_page = analyze_organic_ranking(
            all_organic_results, url
        )

        # 🔴 EARLY STOP FOR ORGANIC
        if organic_rank != "Not Found":
            if DEBUG_RANK_FETCHER:
                print(
                    f"✅ DEBUG → Organic rank found at {organic_rank} "
                    f"({organic_page}), stopping further fetch"
                )
            break

    return {
        "google places": places_rank,
        "google links": organic_rank,
        "page number": organic_page
    }
