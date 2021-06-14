import scrapy
from ..items import SpidersHomeworkItem
 
class MovieSpider(scrapy.Spider):
    name = 'movie'
    start_urls = ['https://www.4567tv.tv/frim/index1.html']

    page = 1
    pages_limit = 5
    page_url = "https://www.4567tv.tv/frim/index1-%s.html" # 设定爬取位置和页数

    def parse(self, response): # 第一层

        li_list = response.xpath('//li[@class="col-md-6 col-sm-4 col-xs-3"]')

        for li in li_list:
            item = SpidersHomeworkItem()    
            name = li.xpath('./div/a/@title').extract_first()
            detail_url = 'https://www.4567tv.tv'+li.xpath('./div/a/@href').extract_first() # 第二层详细信息页面位置
            item['name'] = name
            yield scrapy.Request(url=detail_url,callback=self.parse_detail,meta={'item':item})

        if self.page <= self.pages_limit:
            self.page += 1
            new_page_url = self.page_url % self.page # 翻页设置
            yield scrapy.Request(url=new_page_url,callback=self.parse)

    def parse_detail(self, response): # 第二层

        item = response.meta['item']

        director = response.xpath('/html/body/div[1]/div/div/div/div[2]/p[3]/a/text()').extract_first()
        actor = response.xpath('/html/body/div[1]/div/div/div/div[2]/p[2]/a/text()').extract_first()
        year = response.xpath('/html/body/div[1]/div/div/div/div[2]/p[1]/a[4]/text()').extract_first()
        area = response.xpath('/html/body/div[1]/div/div/div/div[2]/p[1]/a[3]/text()').extract_first()
        movietype = response.xpath('/html/body/div[1]/div/div/div/div[2]/p[1]/a[1]/text()').extract_first()
        infos = response.xpath('/html/body/div[1]/div/div/div/div[2]/p[5]/span[3]/text()').extract_first()

        if year == None:
            year = area
            area = None

        item['director'] = director
        item['actor'] = actor
        item['year'] = year
        item['area'] = area
        item['movietype'] = movietype
        item['infos'] = infos

        yield item
