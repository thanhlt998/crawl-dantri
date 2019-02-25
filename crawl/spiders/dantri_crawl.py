import scrapy


class NewsSpider(scrapy.Spider):
    name = "dantri_crawl"
    noNews = 0
    MAX_NO_NEWS = 1000

    start_urls = [
        'https://dantri.com.vn/kinh-doanh.htm'
    ]

    def parse(self, response):
        urls = response.css("div[data-boxtype=timelineposition] .mr1 h2 a::attr(href)").getall()
        next_page = response.css(".container .clearfix .clearfix.mt1 .fr a::attr(href)").get()
        for url in urls:
            if self.noNews < self.MAX_NO_NEWS:
                news_content_url = response.urljoin(url)
                yield response.follow(news_content_url, self.parse_content)
            else:
                break

        if next_page is not None and self.noNews < self.MAX_NO_NEWS:
            next_page_url = response.urljoin(next_page)
            yield response.follow(next_page_url, self.parse)

    def parse_content(self, response):
        self.noNews += 1
        title = response.css("h1.fon31.mgb15::text").get()
        span = response.css("h2.fon33.mt1.sapo::text").get()
        contents = response.css("#divNewsContent p::text").getall()

        f = open("%s/%s.txt" % (self.start_urls[0].split('/')[3].split('.')[0], self.noNews), mode="a", encoding="UTF8")
        f.write(title.strip() + ' ')
        f.write(span.strip() + ' ')
        for content in contents:
            f.write(content.strip())
        f.close()
