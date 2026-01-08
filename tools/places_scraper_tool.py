from playwright.sync_api import sync_playwright
import time

DEBUG_PLACES_SCRAPER = True


def scrape_google_places(keyword, max_results=30):
    """
    Scrapes Google Maps Places results by dynamically scrolling
    the results panel to load more businesses.
    """

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # keep False for testing
        page = browser.new_page()

        search_url = f"https://www.google.com/maps/search/{keyword.replace(' ', '+')}"
        page.goto(search_url, timeout=60000)

        if DEBUG_PLACES_SCRAPER:
            print(f"\n🗺️ DEBUG → Opening Google Maps for keyword: {keyword}")

        time.sleep(5)

        # Google Maps left panel
        results_panel = page.locator('div[role="feed"]')

        previous_count = 0
        scroll_attempts = 0
        max_scroll_attempts = 12  # safety cap

        while scroll_attempts < max_scroll_attempts:
            business_elements = page.locator('div[role="article"]')
            current_count = business_elements.count()

            if DEBUG_PLACES_SCRAPER:
                print(f"🔄 DEBUG → Loaded Places count: {current_count}")

            # Stop if no new businesses are loading
            if current_count == previous_count:
                if DEBUG_PLACES_SCRAPER:
                    print("⏹️ DEBUG → No new Places loaded, stopping scroll")
                break

            previous_count = current_count

            # Scroll down the panel
            results_panel.evaluate("el => el.scrollBy(0, el.scrollHeight)")
            time.sleep(2)

            scroll_attempts += 1

        final_count = min(previous_count, max_results)

        if DEBUG_PLACES_SCRAPER:
            print(f"✅ DEBUG → Final Places collected: {final_count}")

        # Extract business names
        for i in range(final_count):
            name = business_elements.nth(i).inner_text().split("\n")[0]
            results.append({
                "title": name
            })

        browser.close()

    return results
