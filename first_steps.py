from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    for browser_type in [p.chromium, p.firefox]:
        browser = browser_type.launch(headless=False)
        page = browser.new_page()
        page.goto("https://spa2.scrape.center/")
        page.screenshot(path=f'screenshot-{browser_type.name}.png')
        print(page.title())
        browser.close()