import csv
import time
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

START_URL = "https://www.musashino-u.ac.jp/"
TARGET_DOMAIN = urlparse(START_URL).netloc
MAX_PAGES = 100  # ★上限を設定（100ページ取得したら終了）

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

site_map = {}
visited_urls = set()

def crawl(url):
    # ★上限件数に達していたら処理を終了
    if len(site_map) >= MAX_PAGES:
        return

    if url in visited_urls or urlparse(url).netloc != TARGET_DOMAIN:
        return

    visited_urls.add(url)
    print(f"[{len(site_map) + 1}/{MAX_PAGES}] Crawling: {url}")

    time.sleep(1)

    try:
        res = requests.get(url, headers=headers, timeout=10)
        if "text/html" not in res.headers.get("Content-Type", ""):
            return

        soup = BeautifulSoup(res.text, "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else "No Title"
        site_map[url] = title

        for a_tag in soup.find_all("a", href=True):
            if len(site_map) >= MAX_PAGES:
                break
            next_url = urljoin(url, a_tag["href"]).split("#")[0]
            if urlparse(next_url).netloc == TARGET_DOMAIN and next_url not in visited_urls:
                crawl(next_url)

    except Exception as e:
        print(f"Error fetching {url}: {e}")

# スクレイピング実行
crawl(START_URL)

# CSV保存
csv_filename = "sitemap.csv"
with open(csv_filename, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["URL", "Title"])
    for url, title in site_map.items():
        writer.writerow([url, title])

print(f"完了: {len(site_map)} ページのサイトマップを {csv_filename} に保存しました。")