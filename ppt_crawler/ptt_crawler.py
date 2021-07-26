import requests
from bs4 import BeautifulSoup
from get_ptt_article import GetArticle


root_url = "https://disp.cc/b/"
target_url = root_url + "sex"
# print(target_url)
# headers = {
#     "cookie": "over18=1",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4",
# }

re = requests.get(target_url)

soup = BeautifulSoup(re.text, "html.parser")
titles = soup.find_all("span",class_="listTitle")


for title in titles:
    if title.a != None:  # 如果標題包含 a 標籤(沒有被刪除)，則印出來
        article_url = root_url + title.a["href"]
        title = GetArticle(article_url, title.text)
        title.get_article()
        # print(title.text + "\n" + article_url)
