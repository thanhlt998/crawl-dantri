import scrapy
from scrapy import Request


class NewsSpider(scrapy.Spider):
    name = "thanhnien_crawl"
    noNews = 0
    MAX_NO_NEWS = 2000

    start_urls = [
        'https://thanhnien.vn/van-hoa/'
    ]

    def parse(self, response):
        # response.meta['depth'] = 0
        urls = response.css(".cate-content .zone--timeline article.story h2 a::attr(href)").getall()
        next_page = response.css("nav#paging ul li.active + li a::attr(href)").get()
        for url in urls:
            if self.noNews < self.MAX_NO_NEWS:
                news_content_url = response.urljoin(url)
                # yield response.follow(news_content_url, self.parse_content)
                yield Request(news_content_url, self.parse_content)
            else:
                break

        if next_page is not None and self.noNews < self.MAX_NO_NEWS:
            next_page_url = response.urljoin(next_page)
            # yield response.follow(next_page_url, self.parse)
            yield Request(next_page_url, self.parse)

    def parse_content(self, response):
        self.noNews += 1
        title = response.css("#storybox h1.details__headline::text").get()
        contents = response.css(
            "div#storybox.details div#main_detail.clearfix div#abody div:not(.details__morenews)::text").getall()

        # f = open("%s/%s.txt" % (
        # self.start_urls[0].split('/')[3].split('.')[0],
        # self.noNews), mode="a", encoding="UTF8")
        f = open("data.txt", mode="a", encoding="UTF8")
        f.write(title.strip() + '. ')
        for content in contents:
            f.write(content.strip())
        f.write('\n')
        f.close()
