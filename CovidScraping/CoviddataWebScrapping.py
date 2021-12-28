# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 20:17:07 2021

@author: arkan
"""


import pandas as pd
import requests

url = 'https://en.wikipedia.org/wiki/Template:COVID-19_pandemic_data'
req = requests.get(url)    
target = pd.read_html(req.text)
corona_df = target[0]
#corona_df.drop([0,5],axis=1)

#Assignning column names to the dataframe 
corona_df.columns = ['Col1','Country','Cases','Death','Recoveries','ref']
#Removed the unrequired column
corona_df = corona_df.drop(['Col1','ref'],axis=1)

#Deleted the last two rows 
last_index = corona_df.index[-1]

corona_df = corona_df.drop(corona_df.index[[last_index,(last_index-1)]])

#reframing the countries by removing the bracket texts

corona_df['Country'] = corona_df['Country'].apply(lambda x: x.split("[")[0])

###REplacing No data value with zero

corona_df= corona_df.replace('No data',0)
##Replacing + with blanks
corona_df= corona_df.replace('60+','60')

corona_df['Recoveries'] = pd.to_numeric(corona_df['Recoveries'])
corona_df['Cases'] = pd.to_numeric(corona_df['Cases'])
corona_df['Death'] = pd.to_numeric(corona_df['Death'])

###### exporting the dataframe to an excel file
corona_df.to_excel(r'C:\Users\arkan\Desktop\CoronaData.xlsx',index = False)






