from urllib.parse import urlparse
import re

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


def normalize(text: str) -> str:
    """Normalize text for comparison."""
    return re.sub(r"[^a-z0-9]", "", text.lower())

DEBUG_PLACES = True

def extract_business_name(url: str):
    """
    Extract multiple business name variants from domain.
    """
    domain = urlparse(url).netloc.lower().replace("www.", "")
    base = domain.split(".")[0]

    variants = set()
    variants.add(base)
    variants.add(base.replace("-", "").replace("_", ""))

    if "organic" in base:
        variants.add(base.replace("organic", ""))
        variants.add(base.replace("organic", "").replace("-", "").replace("_", ""))

    normalized_variants = {normalize(v) for v in variants if v}

    if DEBUG_PLACES:
        print(f"\n🔎 DEBUG → Target URL: {url}")
        print(f"🔎 DEBUG → Domain base: {base}")
        print(f"🔎 DEBUG → Generated business name variants:")
        for v in normalized_variants:
            print(f"   - {v}")

    return normalized_variants



def analyze_places_ranking(local_results, target_url):
    """
    Determines Google Local Pack rank using SerpAPI local_results only.
    """

    business_names = extract_business_name(target_url)

    if DEBUG_PLACES:
        print(f"🔎 DEBUG → Local Pack Entries Found: {len(local_results)}")

    for index, place in enumerate(local_results):

        if not isinstance(place, dict):
            continue

        heading = (
            place.get("title")
            or place.get("name")
            or place.get("business_name")
            or ""
        )

        normalized_heading = normalize(heading)

        if DEBUG_PLACES:
            print(f"\n📍 DEBUG → Local Pack Rank Candidate: {index + 1}")
            print(f"📍 DEBUG → Raw heading: {heading}")
            print(f"📍 DEBUG → Normalized heading: {normalized_heading}")

        for name in business_names:
            if DEBUG_PLACES:
                print(f"   🔁 Comparing business token '{name}'")

            if name in normalized_heading:
                if DEBUG_PLACES:
                    print(f"✅ MATCH FOUND → Places Rank = {index + 1}")
                return index + 1

    if DEBUG_PLACES:
        print("❌ DEBUG → No Local Pack match found")

    return "Not Found"
