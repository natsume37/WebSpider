import scrapy
from ..items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        quotes = response.css(".quote")
        for quote in quotes:
            item = QuoteItem()
            item['text'] = quote.css('.text::text').extract_first()
            item['author'] = quote.css('.author::text').extract_first()
            item['tags'] = quote.css('.tags .tag::text').extract()
            yield item
        # 获取下一页连接
        next = response.css('.pager .next a::attr(href)').extract_first()
        # urljoin 将相对URL拼接为绝对URL   /page/2   ---> https://quotes.toscrape.com/page/2/
        url = response.urljoin(next)
        yield scrapy.Request(url=url, callback=self.parse)
