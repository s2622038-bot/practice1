import requests
from bs4 import BeautifulSoup

url ='https://www.musashino-u.ac.jp'
res = requests.get(url)

print(f"ステータスコード:{res.status_code}")
print(f"ステータスメッセージ:{res.reason}")

# HTMLのソースコードをBeautifulSoupオブジェクトに変換する処理

html_soup = BeautifulSoup(res.content,'html.parser')
print(f"html_soupの型:{type(html_soup)}")

# 4-1. ソースコード全体から<a>を抽出する
print("----- 4-1. ソースコード全体から<a>を抽出する -----")
soup_a = html_soup.a
print(soup_a)
print(f"{type(soup_a)}")

# 4-2. ソースコード全体から<p>タグが使われている部分を抽出する
print("----- 4-2. ソースコード全体から<p>を抽出する -----")
soup_p = html_soup.p
print(soup_p)
print(f"{type(soup_p)}")

# 4-3. ソースコード全体から<div>タグが使われている部分を抽出する
print("----- 4-3. ソースコード全体から<div>を抽出する -----")
soup_div = html_soup.div

soup_div_div = soup_div.div
print(soup_div_div)
print(f"{type(soup_div_div)}")

# 4-4. BeautifulSoupオブジェクトとTagオブジェクトは，"."でHTMLタグを連結することでより深いタグにアクセスすることができる．
print("----- 4-4. HTML連結 -----")
soup_div_div = html_soup.div.div
print(soup_div_div)
print(f"{type(soup_div_div)}")

# 4-5. Tagオブジェクト.stringでコンテンツ（ブラウザに表示される部分）を取得できる
print("----- 4-5. stringでコンテンツ取得 -----")
print(f"{soup_a.string}")

# コンテンツがない場合は，None が返ってくるので注意
print("----- コンテンツがない場合は,None が返ってくるので注意 -----")
print(f"{soup_div_div.string}")