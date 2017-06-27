from scrapy.spiders import CrawlSpider, Rule
from wikiSpider.items import Article
from scrapy.linkextractors import LinkExtractor

# SgmlLinkExtractor가 deprecated 되어 LinkExtractor로 대체
# https://github.com/scrapy/scrapy/issues/2254
class Article2Spider(CrawlSpider):
    name="article2"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["http://en.wikipedia.org/wiki/Python_%28programming_language%29"]
    rules = [Rule(LinkExtractor(allow=("(/wiki/)((?!:).)*$"),),
                  callback="parse_item", follow=True)]

    def parse_item(self, response):
        item = Article()
        title = response.xpath("//h1/text()")[0].extract()
        print("Title is: "+title)
        item["title"] = title
        return item