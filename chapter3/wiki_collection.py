from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import re

# https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error
ssl._create_default_https_context = ssl._create_unverified_context

pages = set()
# /wiki/<article_name> 형태인 위키백과 항목 URL을 받고 링크된 항목 URL 목록 전체를 반환하는 함수
def getLinks(pageUrl):
    global pages
    html = urlopen("http://en.wikipedia.org" + pageUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    try:
        # 제목은 항상 h1태그 안에 있고 h1태그는 페이지당 하나만 존재
        # 첫번째 문단 텍스트는 div#mw-conent-text > p 에 있음
        # 편집 링크는 항목페이지에만 존재 li#ca-edit > span > a
        print(bsObj.h1.get_text())
        print(bsObj.find(id="mw-content-text").findAll("p")[0])
        print(bsObj.find(id="ca-edit").find("span").find("a").attrs["href"])
    except AttributeError:
        print("This page is missing something! No worries through!")
    for link in bsObj.findAll("a", href=re.compile("^(/wiki/)")):
        if "href" in link.attrs:
            if link.attrs["href"] not in pages:
                # 새페이지 발견
                newPage = link.attrs["href"]
                print("-----------\n"+newPage)
                pages.add(newPage)
                getLinks(newPage)

getLinks("")