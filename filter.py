import pandas as pd


class filter_df():
    
    def __init__(self):
        self.keywords = ['energy', 'sustainable', 'green', 'climate','sustainability', 'greenhouse', 'waste', 'clean', 'renewable',
        'renovable', 'solar', 'wind', 'eólica', 'recycle', 'recylcing', 'reciclar', 'reciclado', 'ecología', 
        'ecológico', 'ecologic', 'ecology', 'pollution', 'contaminación', 'carbon-neutral', 'carbono-neutral',
        'energía', 'sostenible', 'verde', 'clima', 'sostenibilidad', 'invernadero', 'desperdicio', 'limpia']
    
    def get_lists(self, df):
        self.des = list(df['description'])
        self.key = list(df['keywords'])
        self.bus = list(df['business_model'])

    def filter_data(self, df):
        '''This function takes as argument an unfiltered dataframe and returns a filtered dataframe acccording to keywords'''
        ind = []
        # check for entries in description
        for d in self.des:
            for k in self.keywords:
                try:
                    if k in d.lower():
                        ind.append(self.des.index(d))
                except:
                    None

        # check for entries in keywords
        for c in self.key:
            for k in self.keywords:
                try:
                    if k in c.lower():
                        ind.append(self.key.index(c))
                except:
                    None

        # check for entries in business_model
        for b in self.bus:
            for k in self.keywords:
                try:
                    if k in b.lower():
                        ind.append(self.key.index(c))
                except:
                    None

        # remove duplicate indices from ind
        ind = list(dict.fromkeys(ind))

        # create dataframe with all companies based on their index
        filtered = df.iloc[ind,:]
        filtered.reset_index(inplace = True)
        
        return filtered

if __name__ == "__main__":
    unf = pd.read_csv("/Users/philippbaumanns/Documents/Main Drive (18:19:20:21)/04_ESADE/04_Capstone/Capstone_Project/final_list.csv")
    filter1 = filter_df()
    filter1.get_lists(unf)
    filter1.filter_data(unf)


    



