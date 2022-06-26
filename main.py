import webscraper_startuphubcat
from webscraper_startuphubcat import ScraperStartupHubCatalonia
import webscraper_elreferente
from webscraper_elreferente import ScraperElReferente
import pandas as pd
import numpy as np

 
if __name__ == "__main__":

    # Run Startuphub Catalunia scraper
    scraper_shc = ScraperStartupHubCatalonia()
    scraper_shc.set_driver()
    scraper_shc.get_startups()

    df_shc = scraper_shc.df

    # Run ElReferente scraper
    scraper_ref = ScraperElReferente()
    scraper_ref.get_articles()
    scraper_ref.get_article_url()
    scraper_ref.get_comp_url()
    scraper_ref.get_startups()

    df_referente = scraper_ref.clean_data()

    # Run Levin scraper


    # Merge output from all scrapers to a single dataframe
    df = df_shc.append(df_referente, ignore_index=True)
    #df = df.append(df_[Levin], ignore_index=True)


    # Group dataframe by comp_name
    df_grouped = df
    df_grouped["comp_name"] = df["comp_name"].str.lower()
    df_grouped = df_grouped.groupby("comp_name").count()

    # Go through every column in the dataframe and look for duplicates
    columns = list(df_grouped.columns)
    for column in columns:
        df_grouped[column + "_duplicate"] = df_grouped[column].apply(lambda x: x>1)

    # Identify duplicates and store them in a list
    df_duplicate = df_grouped.drop(columns, axis = 1)
    columns = list(df_duplicate.columns)
    df_duplicate["duplicate"] = df_duplicate.sum(axis=1)>=1
    df_duplicate.drop(columns, axis=1, inplace=True)
    df_duplicate = df_duplicate[df_duplicate["duplicate"] == True]
    df_duplicate.reset_index(inplace=True)

    l_duplicates = list(df_duplicate["comp_name"])

    # Create key to identify sartups
    df["key"] = df["comp_name"].str.lower()


    #print(df.shape)
    # Create dictionary to store merged duplicates
    columns = list(df.columns)
    new_rows = dict.fromkeys(columns, [])
    l_indexes = []

    # Create merged entries from duplicates and store them in new dictionary
    for duplicate in l_duplicates:
        indexes = np.where(np.array(df["key"]) == duplicate)[0]
        l_indexes += list(indexes)
        
        for column in columns:
            temp = []
            
            for i in indexes:
                temp.append((df.loc[i][column]))
            temp = new_rows[column] + [temp[0]]
            new_rows[column] = temp

    # Remove duplicates from original dataframe        
    df.drop(l_indexes, inplace = True)
        
    #print(df.shape)

    # Convert dictionary of merged startups to dataframe
    df_new_rows = pd.DataFrame(new_rows)

    # Add dataframe of merged startups to original dataframe    
    df = df.append(df_new_rows, ignore_index=True)
    df.drop(["key"], axis = 1, inplace = True)
    df.reset_index()
    #print(df.shape)

    # Load previous startups
    df_previous = pd.read_csv('final_list.csv').drop(columns = 'Unnamed: 0')

    # Create lists of new and previous scraped startups and compare them
    previous_startups = list(df_previous['comp_name'].str.lower())
    current_startups = list(df['comp_name'].str.lower())
    comparison = set(current_startups).difference(set(previous_startups))

    # Create a dataframe only containing the new startups
    df_new_startups = df[df['comp_name'].isin(list(comparison))]
    
    # Store final dataframe as csv
    df.to_csv('final_list.csv')
    # Store new startups as csv
    df_new_startups.to_csv('new_startups.csv')

        
