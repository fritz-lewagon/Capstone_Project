import numpy
import requests
import pandas as pd
import bs4


class ScraperElReferente():
    
    def __init__(self):
        self.base_url = 'https://elreferente.es/'
        self.articles = []
        self.a_urls = []
        self.c_urls = []
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

    def get_articles(self):
        '''This function gets all article objects on the page and joins them into one list of beautiful soup objects'''
        result = requests.get(self.base_url)
        soup = bs4.BeautifulSoup(result.text, 'html.parser')
        # different article elements (a1 = top article, a2 = sub articles, a3 = related articles)
        a1 = soup.find_all("h2", class_="news-item-title")
        a2 = soup.find_all("h4", class_="news-item-title")
        a3 = soup.find_all("div", class_="rel-news-title")

        #articles = a1 + a2 + a3
        self.articles = a1 + a2 + a3
        
        #return articles

    def get_article_url(self):

        for a in self.articles:
            try:
                self.a_urls.append(a.find('a')['href'])
            except:
                self.a_urls.append(None)
    
    def get_comp_url(self):
        for a in self.a_urls:
            article = requests.get(a))
            soup_content = bs4.BeautifulSoup(article.content)
            
            for i in soup_content.find_all('h5', class_='startup-item-title'):
                try:
                    self.c_urls.append(i.find('a')['href'])
                except:
                    self.c_urls.append(i.find('a')['href'])

if __name__ == "__main__":
    scraper = ScraperElReferente()
    scraper.get_articles()
    scraper.get_article_url()
    scraper.articles
    scraper.a_urls

        # 1) create function that gets comp urls
        # 2) create function for one startup (get_startup) that gets all the info below for that startup


        # 2) create function (get_startups) that gets all the info for each element in the comp_url


        # get all comp urls
        # for each comp url, get the:
            # name
            # description
            # 'business_model'
            # 'customer'
            # 'keywords'
            # 'stage'
            # 'total_funding'
            # 'num_investors'
            # 'date_founded'
            # 'location'
            # 'employees'
            # 'website'
