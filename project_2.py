import asyncio
from playwright.async_api import async_playwright
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")

BASE_URL = 'https://books.toscrape.com/catalogue/page-{page}.html'
TOTAL_PAGE = 1

STAR_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

async def scrape_index(page, page_num):
    url = BASE_URL.format(page=page_num)
    logging.info(f"Scraping index: {url}")
    await page.goto(url)
    await page.wait_for_selector('article .image_container a')
    elements = await page.query_selector_all('article .image_container a')
    urls = [await el.get_attribute('href') for el in elements]
    return urls

async def scrape_detail(page, url):
    logging.info(f"Scraping detail: {url}")
    await page.goto(url)
    await page.wait_for_selector('h1')
    
    name = await page.text_content('h1')
    price = await page.text_content('.price_color')
    
    star_p = await page.query_selector('.star-rating')
    classes = await star_p.get_attribute('class')
    star_value = classes.replace('star-rating', '').strip()
    star_number = STAR_MAP.get(star_value, 0)
    
    # Product description: the 4th <p> under <article>
    p_elements = await page.query_selector_all('article p')
    product_description = await p_elements[3].text_content() if len(p_elements) > 3 else ''
    
    return {
        'Name': name,
        'Score': star_number,
        'Price': price,
        'Product Description': product_description,
        'URL': url
    }

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        for page_num in range(1, TOTAL_PAGE + 1):
            detail_urls = await scrape_index(page, page_num)
            
            # 因为 href 是相对路径，需要加上主站域名
            detail_urls_full = ['https://books.toscrape.com/catalogue/' + u.split('/')[-2] + '/' + u.split('/')[-1] if not u.startswith('http') else u for u in detail_urls]
            
            for detail_url in detail_urls_full:
                detail_data = await scrape_detail(page, detail_url)
                logging.info(f"Detail data: {detail_data}")
        
        await browser.close()

asyncio.run(main())
