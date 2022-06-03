#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd

data = [[0,"Auara","Beschreibung 3","x","test","test","test","test",1.0,2015.0,"Comunidad de Madrid, España","test","https://auara.org"],
		[1,"Test","Beschreibung 1","x","test","test","test","test",1.0,2015.0,"Comunidad de Madrid, España","test","https://auara.org"],
		[2,"Test2","Beschreibung 5","x","test","test","test","test",1.0,2015.0,"Comunidad de Madrid, España","test","https://auara.org"]
		]
df = pd.DataFrame(data, columns = ["x","comp_name","description","business_model","customer","keywords","stage","total_funding","num_investors","date_founded","location","employees","website"])


df.to_csv (r'./data/test.csv', index = False, header=True)

