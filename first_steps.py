from playwright.sync_api import sync_playwright

# with sync_playwright() as p:
#     for browser_type in [p.chromium, p.firefox]:
#         browser = browser_type.launch(headless=False)
#         page = browser.new_page()
#         page.goto("https://spa2.scrape.center/")
#         page.screenshot(path=f'screenshot-{browser_type.name}.png')
#         print(page.title())
#         browser.close()

import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        for browser_type in [p.chromium, p.firefox]:
            browser = await browser_type.launch(headless=False)
            page = await browser.new_page()
            await page.goto("https://spa2.scrape.center/")
            await page.screenshot(path=f'screenshot-{browser_type.name}.png')
            print(await page.title())
            await browser.close()

asyncio.run(main())