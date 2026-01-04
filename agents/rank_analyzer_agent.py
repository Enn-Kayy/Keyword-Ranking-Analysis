from urllib.parse import urlparse


def normalize_url(url: str) -> str:
    """
    Normalizes a URL to a comparable format by removing protocol,
    'www', and trailing slashes. Used for page-level comparisons.
    """
    try:
        parsed = urlparse(url.lower())
        domain = parsed.netloc.replace("www.", "")
        path = parsed.path.rstrip("/")
        return f"{domain}{path}"
    except Exception:
        return ""


def normalize_domain(url: str) -> str:
    """
    Extracts and normalizes only the domain name from a URL.
    Used for domain-level ranking checks.
    """
    try:
        netloc = urlparse(url).netloc.lower()
        return netloc.replace("www.", "")
    except Exception:
        return ""


def analyze_organic_ranking(organic_results, target_url):
    """
    Determines the organic Google ranking of a target URL
    from the provided organic search results.
    """

    target_normalized = normalize_url(target_url)
    target_domain = normalize_domain(target_url)

    # First attempt: exact page-level URL match
    for index, result in enumerate(organic_results, start=1):
        link = result.get("link", "")
        if normalize_url(link) == target_normalized:
            page = (index - 1) // 10 + 1
            return index, f"Page {page}"

    # Fallback: domain-level match when exact page is not found
    for index, result in enumerate(organic_results, start=1):
        link = result.get("link", "")
        if normalize_domain(link) == target_domain:
            page = (index - 1) // 10 + 1
            return index, f"Page {page}"

    # Target URL not found in the checked results
    return "Not Found", "N/A"


def analyze_places_ranking(places_results, target_url):
    """
    Determines Google Places (Local Pack) ranking for the target URL
    when local results are available.
    """

    target_domain = normalize_domain(target_url)

    # Extract brand name safely from domain for name-based matching
    brand = target_domain.split(".")[0].replace("-", "").replace("_", "")

    for index, place in enumerate(places_results, start=1):

        # Skip invalid or unexpected data formats
        if not isinstance(place, dict):
            continue

        # Primary check: website domain match (most reliable)
        website = place.get("website")
        if website and normalize_domain(website) == target_domain:
            return index

        # Secondary check: normalized business name match
        title = place.get("title", "").lower()
        normalized_title = title.replace(" ", "").replace("-", "").replace("_", "")

        if brand and brand in normalized_title:
            return index

    # No matching place found
    return "Not Found"
