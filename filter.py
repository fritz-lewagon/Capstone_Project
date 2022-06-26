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

if __name__ == "__main__":
    unf = pd.read_csv("final_list.csv")


    filter1 = filter_df()
    filter.get_lists()
    filter1.des


