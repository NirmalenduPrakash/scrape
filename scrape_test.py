import scrapy
class AmazonItem(scrapy.Item):
  # define the fields for your item here like:
  product_name = scrapy.Field()
  product_sale_price = scrapy.Field()
  product_category = scrapy.Field()
  product_original_price = scrapy.Field()
  product_availability = scrapy.Field()

class ScrapeUtil(scrapy.Spider):
    name = 'MySpider'

    def __init__(self, dataFile):
        self.urls = open(dataFile, "r").readlines()
    def getXpathOriginalPrice(self,sale_price):
        return '//span[contains(@class,"a-price") and not(@data-a-strike)]//span[contains(@class,"a-offscreen") and text()="'+sale_price+'"]/../parent::a//following-sibling::span[@data-a-strike]//span[contains(@class,"a-offscreen")]/text()'

    def parse(self, response):
        XPATH_NAME = '//span[contains(@class,"a-size-base-plus a-color-base a-text-normal")]/text()'
        XPATH_SALE_PRICE = '//span[contains(@class,"a-price") and not(@data-a-strike)]//span[contains(@class,"a-offscreen")]/text()'
        #XPATH_ORIGINAL_PRICE = '//span[contains(@class,"a-price") and not(@data-a-strike)]//span[contains(@class,"a-offscreen") and contains(text(),"\u20b9'+data+'")]/text()'
        
            #XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
            #XPATH_AVAILABILITY = '//div[@id="availability"]//text()'

            
        RAW_NAME = response.xpath(XPATH_NAME).extract()
        RAW_SALE_PRICE = response.xpath(
            XPATH_SALE_PRICE).extract()
            #RAW_CATEGORY = response.xpath(XPATH_CATEGORY).getall()
        #try:  
        ORIGINAL_PRICE=[]  
        for sale_price in RAW_SALE_PRICE:
            RAW_ORIGINAL_PRICE = response.xpath(
                self.getXpathOriginalPrice(sale_price)).extract_first() or "NA"
            ORIGINAL_PRICE.append(RAW_ORIGINAL_PRICE)    
        #except:
            #pass        
            #RAw_AVAILABILITY = response.xpath(
                    #XPATH_AVAILABILITY).getall()

            # NAME = ' '.join(''.join(RAW_NAME).split()
            #                      ) if RAW_NAME else None
            # SALE_PRICE = ' '.join(
            #         ''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
            #CATEGORY = ' > '.join(
                    #[i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
            # ORIGINAL_PRICE = ''.join(
            #         RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
            #AVAILABILITY = ''.join(
                    #RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None

            # if not ORIGINAL_PRICE:
            #         ORIGINAL_PRICE = SALE_PRICE
            #items['product_category'] = ','.join(map(lambda x: x.strip(), category)).strip()
            #items['product_availability'] = ''.join(availability).strip()
            # names=[]
            # for name in RAW_NAME:
            #     names.append({'name':name})
        for name,sale_preice,original_price in zip(RAW_NAME,RAW_SALE_PRICE,ORIGINAL_PRICE):
        #for original_price in ORIGINAL_PRICE:
            yield {'name':name,'sale price':sale_preice,
            'original price':original_price}

    def start_requests(self):
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'cache-control': 'no-cache',
            'User-Agent': 'Mozilla/5.0'
        }
        for url in self.urls:
            yield scrapy.Request(url, self.parse,headers=headers)
