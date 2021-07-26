import requests
from bs4 import BeautifulSoup


class GetArticle:
    def __init__(self, url, title):
        self.url = url
        self.title = title
        self.re = requests.get(self.url)
        self.soup = BeautifulSoup(self.re.text, "html.parser")

    def get_article(self):
        doc = self.soup.find("div", class_="text_css").get_text()
        filename = self.title.split()[-1].replace("/", "")
        # print(filename)
        with open(filename+".txt", "w", encoding="utf-8") as f:
            f.write(self.title+"\n")
            f.write(doc)
