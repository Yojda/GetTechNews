import asyncio
import json
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://news.adobe.com/news")
        await page.wait_for_selector("main")
        content = await page.content()
        await browser.close()

    soup = BeautifulSoup(content, 'html.parser')
    articles = []
    for item in soup.find_all('div', class_='article'):
        title = item.find('h2').get_text(strip=True)
        link = item.find('a')['href']
        if not link.startswith('http'):
            link = f"https://news.adobe.com{link}"
        date = item.find('time').get_text(strip=True) if item.find('time') else None
        articles.append({'title': title, 'link': link, 'date': date})

    print(json.dumps(articles, indent=2))

asyncio.run(run())