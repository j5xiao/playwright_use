import asyncio
import logging
from playwright.async_api import async_playwright

logging.basicConfig(level=logging.INFO, format="%(message)s")

BASE_URL = "https://spa2.scrape.center/"
INDEX_URL = "https://spa2.scrape.center/page/{page}"
total_page = 10


async def scrape_page(page, url, selector):
    logging.info(f"scraping {url}")
    try:
        await page.goto(url)
        await page.wait_for_selector(selector)
    except Exception as e:
        logging.error(f"error while scraping {url}: {e}")


async def scrape_index(page, page_number):
    url = INDEX_URL.format(page=page_number)
    await scrape_page(page, url, ".item")


async def parse_index(page):
    elements = await page.query_selector_all("#index .item .name")
    urls = []
    for el in elements:
        href = await el.get_attribute("href")
        urls.append(href)
    return urls


async def scrape_detail(page, url):
    await scrape_page(page, url, "h2")


async def parse_detail(page):
    name = await page.text_content("h2")
    category_container = await page.query_selector(".categories")
    category_elements = await category_container.query_selector_all("button span")
    categories = [(await c.text_content()).strip() for c in category_elements]
    score = await page.text_content(".score")
    return name, categories, score


async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            for p in range(1, total_page + 1):
                await scrape_index(page, p)
                detail_urls = await parse_index(page)

                for detail_url in detail_urls:
                    logging.info(f"get detail url {detail_url}")
                    await scrape_detail(page, detail_url)
                    detail_data = await parse_detail(page)
                    logging.info(f"detail data: {detail_data}")

        finally:
            await browser.close()


asyncio.run(main())
