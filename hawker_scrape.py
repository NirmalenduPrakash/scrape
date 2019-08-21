import scrapy
from scrapy.spiders import XMLFeedSpider

class ScrapeUtil(XMLFeedSpider):
    name = 'MySpider'
    namespaces = [
    ('x', 'http://www.w3.org/2001/XMLSchema'),
    ('x', 'http://www.google.com/kml/ext/2.2'),
    ('x', 'http://www.w3.org/2005/Atom'),
    ('x','http://www.opengis.net/kml/2.2')
    ]
    iterator = 'xml'
    start_urls = ['file:/Users/nirmalenduprakash/Documents/ML/scrape/hawker-centres-kml.kml']
        # self.urls = open(dataFile, "r").readlines()
    
    def parse(self, response,node):
        XPATH = '//ExtendedData/SimpleData[@name="ADDRESSBLOCKHOUSENUMBER"]/text()'        
        items = node.xpath(XPATH).extract()        
        return {'block number':items}

    # def start_requests(self):
    #     headers = {
    #         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #         'cache-control': 'no-cache',
    #         'User-Agent': 'Mozilla/5.0'
    #     }
    #     yield scrapy.Request('file:/Users/nirmalenduprakash/Documents/ML/scrape/hawker-centres-kml.kml', self.parse,headers=headers)
