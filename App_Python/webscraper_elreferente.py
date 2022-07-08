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
            article = requests.get(a)
            soup_content = bs4.BeautifulSoup(article.content)
            
            for i in soup_content.find_all('h5', class_='startup-item-title'):
                try:
                    self.c_urls.append(i.find('a')['href'])
                except:
                    self.c_urls.append(i.find('a')['href'])

    def get_startups(self):
        
        for c in self.c_urls:
            page = requests.get(c)
            page_content = bs4.BeautifulSoup(page.content)

            # name
            try:
                self.startup_list['comp_name'].append(page_content.find('h2', class_ = 'title').text.replace('\n', '').replace('  ', ''))
            except:
                self.startup_list['comp_name'].append('')

            # description
            try:
                self.startup_list['description'].append(page_content.find('div', class_ = 'description blue-links').text.replace('\n', '').replace('\xa0', ''))
            except:
                self.startup_list['description'].append('')

            # 'business_model'
            self.startup_list['business_model'].append('')

            # 'customer'
            try:
                self.startup_list['customer'].append(page_content.find('div', class_ = 'section section-info blue-links').find_all('div', class_= 'value')[-1].text.replace('\n', '').replace(' ', ''))
            except:
                self.startup_list['customer'].append('')

            # 'keywords'
            try:
                self.startup_list['keywords'].append(page_content.find('div', class_ = 'flex-row tags highlight').text.replace('\n', '').replace(' ', ''))
            except:
                self.startup_list['keywords'].append('')
            
            # 'stage'
            self.startup_list['stage'].append('')

            # 'total_funding'
            infos = []
            for i in page_content.find('div', class_='flex-row info-container').find_all('div', class_='value'):
                infos.append(i.text.replace(' ', '').replace('\n', ''))
            
            try:
                if infos[1] == 'N/D':
                    self.startup_list['total_funding'].append('')
                else:
                    self.startup_list['total_funding'].append(float(infos[1].replace(',', '.').replace('M€', '')))

            except:
                self.startup_list['total_funding'].append('')

            
            # 'num_investors'
            try:
                self.startup_list['num_investors'].append(infos[2])
            except:
                self.startup_list['num_investors'].append('')
        
            # 'date_founded'
            try:
                self.startup_list['date_founded'].append(infos[0])
            except:
                self.startup_list['date_founded'].append('')

            # 'location'
            try:
                self.startup_list['location'].append(page_content.find('div', class_ = 'value icon-location').text.replace('\n', '').replace('  ', ''))
            except:
                self.startup_list['location'].append('')

            # 'employees'
            try:    
                empl = page_content.find('div', class_ = 'value blur-no-auth').text.replace('\n', '').replace(' ', '')
                if len(empl)>1:
                    empl = empl
                else:
                    empl = ''
                self.startup_list['employees'].append(empl)
            except:
                self.startup_list['employees'].append('')

            # 'website'
            try:
                self.startup_list['website'].append(page_content.find('a', class_ = 'blue')['href'])
            except:
                self.startup_list['website'].append('')
    
    def clean_data(self):
        self.df = pd.DataFrame(self.startup_list)
        return self.df



