import webscraper_elreferente
 
if __name__ == "__main__":
    scraper = ScraperElReferente()
    scraper.get_articles()
    scraper.get_article_url()
    scraper.get_comp_url()
    scraper.get_startups()
    scraper.clean_data()

print(scraper.df)