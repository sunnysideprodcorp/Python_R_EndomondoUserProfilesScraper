import scrapy
import time
import random
import re
import os

#scrape first parts of 2015
#API call uses European date format
month = ["%02d" %(i,) for i in range(7)[1:]]
date_list = ["2015-%s-01"%m for m in month]

#need a browser header or API does not deliver content
UA = 'Mozilla/5.0 (X11; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0'

#API id's seem dense near this starting value
api_id_start = 20546248
num_ids_to_try = 100000

#directory to store user data
user_data_directory = #PUT YOUR DIRECTORY HERE

class DmozSpider(scrapy.Spider):
    '''This spider pairs with all default Scrapy project settings. Spider starts with 
    a likely API id number and progresses up through all id numbers from that number to 
    that number plus num_ids_to_try
    '''
    name = "dmoz"
    allowed_domains = ["endomondo.com"]
    def start_requests(selfSelf):
        for i in range(num_ids_to_try):
            if (i+1)%1000==0:
                time.sleep(600)
            for (before_date, after_date) in zip(date_list[1:], date_list[:-1]):
                timesleep = random.uniform(.1, .4)
                time.sleep( timesleep)
                yield scrapy.Request('https://www.endomondo.com/rest/v1/users/%d/workouts?before=%s&after=%s' % ((ap_id_start + i), before_date, after_date), headers = {'User-Agent':UA})


    def parse(self, response):
        '''Parse takes results of API call and makes a directory for a user if that 
        user does not have a directory. Then parse generates a file for the relevant
        date range and saves the API's response, as text in JSON format, in the file'''
        time.sleep(2)
        dirname = response.url.split("/")[-2]
        filename = re.split(r"[\&\?]", response.url.split("/")[-1])[1]
        filename_string = "%S\\%s\\%s.json"%(user_data_directory, dirname, filename)
        if(len(str(response.body))>2):
            if not os.path.exists(os.path.dirname(filename_string)):
                os.makedirs(os.path.dirname(filename_string))
            with open(filename_string, 'w') as f:
                f.write(('{"endo":%s, "array":'%dirname)+response.body+"}")


