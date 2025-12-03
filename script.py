import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.google.com/sorry/index?continue=https://www.google.com/search%3Fclient%3Dfirefox-b-d%26q%3Dhtml%26sei%3DuSsvaaTyGeXPkPIPr7352A0&q=EgQvlBGSGLnXvMkGIjDtXIxbGM7vGkjBwZZt1D63IrDoMjLoKYo_RuaBsvOWWAsDlgYHfuwEGdGw-urxtzAyAVJaAUM")
    page.locator("iframe[name=\"a-418k6j1g9uxi\"]").content_frame.locator(".rc-anchor-center-item").first.click()
    page.locator("iframe[name=\"c-418k6j1g9uxi\"]").content_frame.locator("[id=\"0\"]").click()
    page.locator("iframe[name=\"c-418k6j1g9uxi\"]").content_frame.get_by_role("button", name="Verify").click()
    page.locator("iframe[name=\"c-418k6j1g9uxi\"]").content_frame.locator("[id=\"0\"]").click()
    page.locator("iframe[name=\"c-418k6j1g9uxi\"]").content_frame.locator("[id=\"6\"]").click()
    page.locator("iframe[name=\"c-418k6j1g9uxi\"]").content_frame.locator("div").filter(has_text=re.compile(r"^Verify$")).nth(2).click()
    page.locator("iframe[name=\"c-418k6j1g9uxi\"]").content_frame.locator("[id=\"0\"]").click()
    page.locator("iframe[name=\"c-418k6j1g9uxi\"]").content_frame.locator("[id=\"7\"]").click()
    page.locator("iframe[name=\"c-418k6j1g9uxi\"]").content_frame.locator("[id=\"6\"]").click()
    page.locator("iframe[name=\"c-418k6j1g9uxi\"]").content_frame.get_by_role("button", name="Verify").click()
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
