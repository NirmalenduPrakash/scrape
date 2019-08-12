import scrapy
import time
import json
from googleapiclient.discovery import build

my_api_key = "AIzaSyCYdGnPE4Y0tJqysdJShEW5vTBcuuPjwVM"
my_cse_id = "012273702812221375936:rwpa8cf5t-e"

class Course:
    def __init__(self,inputFile):
        self.courses=open(inputFile, "r").readlines()
        self.urls=[]
    def getUrls(self):    
        for course in self.courses:
            url=self.google_search(course,my_api_key,my_cse_id,num=5)
            self.urls.append(url)
        f=open('urls.txt','w')
        f.write(self.urls)        
    def google_search(self,search_term, api_key, cse_id, **kwargs):
        service = build("customsearch", "v1", developerKey=api_key,cache_discovery=False)
        res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
        if('items' in res.keys()):
            return res['items'][0]['link']
        return ''   

class ScrapeUtil(scrapy.Spider):
    name = 'MySpider'

    def __init__(self, dataFile):
        #Course(dataFile).getUrls()
        #time.sleep(5)
        self.download_delay=2
        self.max_concurrent_requests=1
        self.urls = [x.strip() for x in open('trackpaths.txt', "r").readlines()]

    def parse(self, response):
        TRACK_ROOT_PATH='//div[contains(@class,table-responsive table-roadmap)]/table/tbody/tr[/td[contains(@class,"table-roadmap--mainlabel")]]'
        # TRACK='//div[contains(@id,"accordion-roadmap")]/table/td[contains(@class,"table-roadmap--mainlabel")]/span/text()'
        # LEVEL= '//div[contains(@id,"overview")]'
        # COURSE = '//div[contains(@id,"instructors")]/div[contains(@class,"row")]/div[2]/h3/text()'
        tracks=response.xpath(TRACK_ROOT_PATH).extract()
        tracks=json.loads(tracks)
        for track in tracks:
            
        COURSE=response.xpath(TITLE_PATH).extract_first()
        REFERENCE_No=response.xpath(XPATH_Overview+'/table/tbody/tr[1]/td/text()').extract()    
        PART_OF=response.xpath(XPATH_Overview+'/table/tbody/tr[2]/td/text()').extract() 
        DURATION=response.xpath(XPATH_Overview+'/table/tbody/tr[3]/td/text()').extract()
        COURSE_TIME=response.xpath(XPATH_Overview+'/table/tbody/tr[4]/td/text()').extract()  
        ENQUIRY=response.xpath(XPATH_Overview+'/table/tbody/tr[5]/td/text()').extract()

        INSTRUCTORS=response.xpath(XPATH_Lecturer).extract()    
        
        yield {'title':COURSE,'Reference No':REFERENCE_No,'Part of':PART_OF,'Duration':DURATION,
        'Course time':COURSE_TIME,'Enquiry':ENQUIRY,'Instructors':[instructor for instructor in INSTRUCTORS]}

    def start_requests(self):
        # headers = {
        #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        #     'cache-control': 'no-cache',
        #     'User-Agent': 'Mozilla/5.0'
        # }
        
        for url in self.urls:
            if(url!='Not Available'):
                yield scrapy.Request(url, self.parse)
            else:
                yield url    
