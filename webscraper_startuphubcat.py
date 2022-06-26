import requests
import time
import pandas as pd
import numpy as np

import bs4

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class ScraperStartupHubCatalonia():
    
    
    def __init__(self):
        self.base_url = 'http://startupshub.catalonia.com'
        self.startup_list = {'comp_name':[],
                            'description':[],
                            'business_model':[], 
                            'customer':[],
                            'keywords':[],
                            'stage':[],
                            'total_funding': [],
                            'num_investors':[],
                            'date_founded':[],
                            'location':[],
                            'employees':[],
                            'website':[]}


        
    def set_driver(self):
        driver_path = 'Chromedriver.exe'
        chrome_options = Options()
        #chrome_options.add_argument("--disable-extensions")
        #chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        # chrome_options.headless = True # also works
        driver = webdriver.Chrome(options=chrome_options)       
        
        self.driver = webdriver.Chrome()
        self.driver.get('http://startupshub.catalonia.com/list-of-startups')
       
        
    def get_startups(self):
        self.startups = bs4.BeautifulSoup(self.driver.page_source).find_all(class_ = 'activitat')
        
        while(True):
            time.sleep(6)
            try:
                for startup in self.startups:
                    self.get_startup(startup)

                self.driver.find_elements_by_class_name('next-1')[0].click()
                self.startups = bs4.BeautifulSoup(self.driver.page_source).find_all(class_ = 'activitat')

            except:
                break
            
        self.driver.close()
        self.clean_data()


    
    def get_startup(self, startup):
        '''This function extract all relevant information from the respective startup'''
    
        try:
            self.startup_list['comp_name'].append(startup.find(class_ = 'titol').get_text().strip())            
        except:
            self.startup_list['comp_name'].append('')    
        try:
            self.startup_list['description'].append(startup.find(class_ = 'description').get_text().strip())
        except:
            self.startup_list['description'].append('')   
        try:
            self.startup_list['business_model'].append(startup.find(class_ = 'b-model').get_text().strip())
        except:
            self.startup_list['business_model'].append('')    
        try:
            self.startup_list['customer'].append(startup.find(class_ = 'target information-item').get_text().replace('\t','').replace('\n','').replace('\r','').strip())
        except:
            self.startup_list['customer'].append('')   
        try:
            self.startup_list['keywords'].append(startup.find(class_ = 'cats').get_text().replace('\t','').replace('\n','').replace('\r','').strip())
        except:
            self.startup_list['keywords'].append('')

        self.get_details(startup)

        return None


    def get_details(self, startup):
        '''This function extracts the url of the detailed start-up page and fetches additional information into the dictionary'''

        # get url and save content in bs4 object
        page = requests.get(self.base_url + startup.find(class_ = 'text-comp').find('a').get('href'))
        detail = bs4.BeautifulSoup(page.text, "html.parser")

        try:
            self.startup_list['stage'].append(detail.find(class_ = 'stage information-item').find('strong').attrs['value'])
        except:
            self.startup_list['stage'].append('')
        try:
            self.startup_list['date_founded'].append(detail.find(class_ = 'founded information-item').get_text().strip())
        except:
             self.startup_list['date_founded'].append('')
        try:
            self.startup_list['employees'].append(detail.find(class_ = 'employers information-item').find('strong').attrs['value'])
        except:
            self.startup_list['employees'].append('')

        self.startup_list['total_funding'].append('')
        self.startup_list['num_investors'].append('')
        self.startup_list['location'].append('')
        self.startup_list['website'].append('')

        return None
    

    def clean_data(self):
        self.df = pd.DataFrame(self.startup_list)
        
        # Transform values in stage column to Strings
        x = np.array(self.df["stage"])
        condlist = [x == "-1", x == "1", x == "2", x == "3", x == "4", x == "5"]
        choicelist = ["-", "Pre-seed", "Seed", "Series A", "Series B", "Series C"]
        self.df["stage"] = np.select(condlist, choicelist)


        self.df["website"] = "http://startupshub.catalonia.com"

        # Split date value to only keep year
        self.df["date_founded"].replace("",":", inplace =True)
        self.df["date_founded"] = self.df["date_founded"].apply(lambda x: x.split(":")[1])
        
        return None

