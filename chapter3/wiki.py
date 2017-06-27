from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import datetime
import random
import re

# https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error
ssl._create_default_https_context = ssl._create_unverified_context

random.seed(datetime.datetime.now())

# /wiki/<article_name> 형태인 위키백과 항목 URL을 받고 링크된 항목 URL 목록 전체를 반환하는 함수
def getLinks(articleUrl):
    html = urlopen("http://en.wikipedia.org" + articleUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    # id가 bodyContent인 div안에 있음
    # URL에 세미콜론이 포함되어 있지 않음
    # URL은 /wiki/로 시작
    return bsObj.find("div", {"id":"bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))

# 무작위로 항목 링크를 선택하여 getLinks를 다시 호출
# 프로그램을 끝내거나 새 페이지에 항목 링크가 없을때까지 반복
links = getLinks("/wiki/Kevin_Bacon")
while len(links) > 0:
    newArticle = links[random.randint(0, len(links) - 1)].attrs["href"]
    print(newArticle)
    links = getLinks(newArticle)
