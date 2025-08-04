from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def scrape_gumroad_trends():
    trends = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto("https://gumroad.com/discover", timeout=60000, wait_until="domcontentloaded")
            page.wait_for_timeout(2000)  # Short buffer
            html = page.content()
        except Exception as e:
            print(f"[!] Gumroad failed to load: {e}")
            browser.close()
            return trends  # Return empty list on failure

        soup = BeautifulSoup(html, "html.parser")
        products = soup.select("a.product-card")[:10]
        for product in products:
            name = product.select_one("h3").get_text(strip=True)
            price = product.select_one(".price").get_text(strip=True)
            trends.append({"name": name, "price": price})

        browser.close()
    return trends

def scrape_upwork_jobs():
    jobs = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.upwork.com/nx/jobs/search/?q=AI&sort=recency")
        page.wait_for_timeout(3000)
        soup = BeautifulSoup(page.content(), "html.parser")
        postings = soup.select(".job-tile")[:10]
        for post in postings:
            title = post.select_one("h4.job-tile-title").get_text(strip=True)
            budget = post.select_one(".js-budget").get_text(strip=True) if post.select_one(".js-budget") else "Hourly"
            jobs.append({"title": title, "budget": budget})
        browser.close()
    return jobs

def get_market_signals():
    gumroad = scrape_gumroad_trends()
    upwork = scrape_upwork_jobs()
    return {
        "gumroad_top_products": gumroad,
        "upwork_recent_jobs": upwork
    }
