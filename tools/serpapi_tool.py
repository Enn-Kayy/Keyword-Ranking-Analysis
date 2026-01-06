from serpapi import GoogleSearch
from config.settings import SERPAPI_API_KEY, LOCATION, GOOGLE_DOMAIN, GL, HL
import time


def fetch_google_results(keyword: str, max_pages=3):
    """
    Fetches Google organic search results and Google Places (Local Pack)
    data for a given keyword using the SerpAPI service.
    """
    
    print(f"\n SEARCHING KEYWORD → {keyword}")

    organic_results = []
    places_results = []



    for page in range(max_pages):
        params = {
            "engine": "google",
            "q": keyword,
            "google_domain": GOOGLE_DOMAIN,
            "location": LOCATION,
            "start": page * 10,
            "num": 10,
            "gl": GL,
            "hl": HL,
            "pws": 0,
            "api_key": SERPAPI_API_KEY,
        }

        search = GoogleSearch(params)
        data = search.get_dict()

        print("DEBUG → API STATUS:", data.get("search_metadata", {}).get("status"))
        print("DEBUG → Organic count:", len(data.get("organic_results", [])))
        print("DEBUG → Local count:", len(data.get("local_results", [])))

        # Capture Google Places results only from the first page
        if page == 0:
            places_results = data.get("local_results", [])
            
        # Retrieve organic search results for the current page
        organic = data.get("organic_results", [])
        if not organic:
            break

        organic_results.extend(organic)

        # Delay added to respect API rate limits
        time.sleep(2)

    return {
        "places": places_results,
        "organic": organic_results
    }
