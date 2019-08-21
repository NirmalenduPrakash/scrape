import scrapy

class ScrapeUtil(scrapy.Spider):
    name = 'MySpider'

    def __init__(self, dataFile):
        self.urls = open(dataFile, "r").readlines()
    
    def parse(self, response):
        XPATH = '//span[//span[@class="glyphicon glyphicon-star"]]/@style'
        # XPATH = '//meta[@itemprop="ratingValue"]/@content'
        # XPATH='//div[@class="reviewer-info"]//span[//span[@class="glyphicon glyphicon-star"]]/@style' 
        
        items = response.xpath(XPATH).extract()
        # count=response.xpath(XPATH).extract_first()
        # count not reset because of yield , so this workaround
        count=response.meta.get('count')
        for item in items:
            try:
                perc=item.split(';')[-2]
                if(perc=='width:100%'):
                    count+=1
                else:
                    count+=((float)(perc.split(':')[1].split('%')[0]))/100 
            except:
                continue
        return {'rating':items}


    def start_requests(self):
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'cache-control': 'no-cache',
            'User-Agent': 'Mozilla/5.0'
        }
        for url in self.urls:
            yield scrapy.Request(url, self.parse,headers=headers,meta={'count':0})
