# scrape
web scraping
nus_courses_scrape.ipynb does a bing search for each of the courses and saves the first URL returned in a txt file
nus_course_scrape.py picks up each of the URLs from the text file and scrapes course information
-use command:scrapy runspider scrape_test.py -a dataFile='urls.txt' -o output.json
nus_course_track_scrape.py-under progress, to get track, level information of courses
