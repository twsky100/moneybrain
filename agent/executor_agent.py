from dotenv import load_dotenv
import os
from playwright.sync_api import sync_playwright
import time

load_dotenv()
EMAIL = os.getenv("GUMROAD_EMAIL")
PASSWORD = os.getenv("GUMROAD_PASSWORD")

def simulate_execution(idea):
    print(f"Executing real-world test for: {idea['name']}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            # 1. Log in
            page.goto("https://gumroad.com/login")
            # Wait for iframe to load and grab it
            page.wait_for_selector("iframe")
            iframe = page.frame_locator("iframe").first
            
            # Fill login form inside iframe
            iframe.locator("input[name='user[email]']").fill(EMAIL)
            iframe.locator("input[name='user[password]']").fill(PASSWORD)
            iframe.locator("button[type='submit']").click()
            page.fill("input[name='user[password]']", PASSWORD)
            page.click("button[type='submit']")
            page.wait_for_timeout(4000)

            # 2. Go to New Product page
            page.goto("https://gumroad.com/products/new")
            page.wait_for_timeout(3000)

            # 3. Fill in dummy product
            page.click("text=Classic")
            page.fill("input[name='product[name]']", idea['name'][:50])
            page.fill("input[name='product[description]']", idea['concept'][:200])
            page.fill("input[name='product[price_string]']", "0")
            page.set_input_files("input[type='file']", "./prompts/idea_generation_prompt.txt")

            # 4. Publish
            page.click("button:has-text('Publish')")
            page.wait_for_timeout(5000)

            # 5. Get product URL
            product_url = page.url
            print(f"[+] Product published: {product_url}")

        except Exception as e:
            print(f"[!] Execution failed: {e}")
            page.screenshot(path="error_screenshot.png", full_page=True)
            product_url = "ERROR"

        browser.close()

    return {
        "revenue": 0.00,
        "visits": 0,
        "leads": 0,
        "notes": f"Gumroad test executed. Link: {product_url}"
    }
