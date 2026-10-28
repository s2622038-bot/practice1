import csv
import time
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

# ドメインとスタートURLの設定
START_URL = "https://www.musashino-u.ac.jp/"
TARGET_DOMAIN = urlparse(START_URL).netloc

# ヘッダーの設定
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 取得したデータを保持する辞書 {URL: タイトル}
site_map = {}
# 訪問済みURLのセット
visited_urls = set()


def crawl(url):
    # すでに訪問済み、または別ドメインの場合はスキップ
    if url in visited_urls or urlparse(url).netloc != TARGET_DOMAIN:
        return

    visited_urls.add(url)
    print(f"Crawling: {url}")

    # サーバー負荷軽減（1秒停止）
    time.sleep(1)

    try:
        res = requests.get(url, headers=headers, timeout=10)
        # HTML以外のコンテンツ（PDFや画像など）はスキップ
        if "text/html" not in res.headers.get("Content-Type", ""):
            return

        soup = BeautifulSoup(res.text, "html.parser")

        # <title>タグの取得
        title = soup.title.string.strip() if soup.title and soup.title.string else "No Title"
        site_map[url] = title

        # ページ内のすべてのリンクを抽出して再帰的に巡回
        for a_tag in soup.find_all("a", href=True):
            next_url = urljoin(url, a_tag["href"])
            # フラグメント（#...）を取り除く
            next_url = next_url.split("#")[0]

            # 同一ドメインかつ未訪問なら次のページへ
            if urlparse(next_url).netloc == TARGET_DOMAIN and next_url not in visited_urls:
                crawl(next_url)

    except Exception as e:
        print(f"Error fetching {url}: {e}")


# 1. スクレイピング実行
crawl(START_URL)

# 2. 結果をCSVファイルに保存
csv_filename = "sitemap.csv"
with open(csv_filename, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["URL", "Title"])  # ヘッダー行
    for url, title in site_map.items():
        writer.writerow([url, title])

print(f"完了: {len(site_map)} ページのサイトマップを {csv_filename} に保存しました。")