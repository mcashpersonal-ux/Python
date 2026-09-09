# Playwright — browser automation and end-to-end testing

> Playwright drives real Chromium, Firefox, and WebKit browsers from
> Python — for end-to-end UI tests, scraping JavaScript-heavy sites, or
> scripting anything a human would otherwise click through by hand.

## Install and set up browsers

```bash
python -m pip install playwright
playwright install        # downloads the browser binaries
```

## navigate and read the page

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")
    print(page.title())
    browser.close()
```

The sync API (used here) is the simplest entry point; an async API
(`playwright.async_api`) exists for use inside `asyncio` applications.

## interact with elements

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com/login")
    page.fill("#username", "demo-user")
    page.fill("#password", "demo-pass")
    page.click("button[type=submit]")
    page.wait_for_selector(".dashboard")
    browser.close()
```

Playwright auto-waits for elements to be visible and actionable before
interacting with them — you rarely need manual `sleep()` calls the way
older scraping tools required.

## use it in pytest

```python
def test_homepage_title(page):
    page.goto("https://example.com")
    assert "Example" in page.title()
```

```bash
python -m pip install pytest-playwright
python -m pytest --headed   # or omit --headed to run without a visible window
```

The `pytest-playwright` plugin provides the `page` fixture (and browser
context isolation between tests) for free.

## Scraping etiquette and legal safety

Check the target site's `robots.txt` and terms of service before
scraping it, add delays between requests so you do not overload the
server, identify your bot honestly if the site expects that, and never
attempt to bypass login walls or paywalls you are not authorized to
access.

Next door: [requests](051-requests.md) and [beautifulsoup4](055-beautifulsoup4.md)
for static pages that do not need a real browser, and [pytest](095-pytest.md)
for the test runner Playwright plugs into.
