# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 21:07:56 2021

@author: arkan
"""

import pandas as pd

import requests

url ='https://en.wikipedia.org/wiki/COVID-19_pandemic_in_India#covid19-container'

req = requests.get(url)
target = pd.read_html(req.text )
#web_content= req.content

coronaIndia = target[4]

######Data cleaning
# Remove date duplicate column
#Remove the blank column
# clean the case column & death column

coronaIndia.columns = ['Date','Date2','nn','Cases','Death']

coronaIndia = coronaIndia.drop(['Date2','nn'], axis = 1)

coronaIndia = coronaIndia.iloc[1:]

coronaIndia.set_index  = coronaIndia.reset_index(drop=True, inplace=True)

#Coverting the garbage dates
coronaIndia.iloc[1]['Date'] = '2020-02-01'
coronaIndia.iloc[4]['Date'] = '2020-02-15'
coronaIndia.iloc[6]['Date'] = '2020-02-28'

lastindex=coronaIndia.index[-1]

#Droppong the last idex
coronaIndia = coronaIndia.iloc[0:lastindex]


#x =coronaIndia[(coronaIndia['Date'] == '⋮')]

coronaIndia['Cases % change'] = coronaIndia['Cases'].apply(lambda x: x.split("(")[1].split(")")[0])

coronaIndia['Cases'] = coronaIndia['Cases'].apply(lambda x: x.split("(")[0])

coronaIndia=coronaIndia.replace('=',0)

coronaIndia['Cases % change'].iloc[0] = 0
######Filling the null values with zero

coronaIndia['Death'] = coronaIndia['Death'].fillna(0)

coronaIndia['Death'] = coronaIndia['Death'].apply(lambda x: str(x).split("(")[0])

coronaIndia['Cases % change'] = coronaIndia['Cases % change'].replace(0,"0")

list=[]
for words in coronaIndia['Cases % change']:
    ls = (words[1:-1])
    list.append(ls)

coronaIndia['Cases % change'] = list

### Removing commas

coronaIndia['Cases']  = coronaIndia['Cases'].str.replace(",","")
coronaIndia['Death']  = coronaIndia['Death'].str.replace(",","")
coronaIndia['Date']  = coronaIndia['Date'].str.replace("⋮","nan")
###### Converting data types

coronaIndia['Cases'] = pd.to_numeric(coronaIndia['Cases'])
coronaIndia['Death'] = pd.to_numeric(coronaIndia['Death'])

coronaIndia['Cases % change'] = pd.to_numeric(coronaIndia['Cases % change'])

coronaIndia['Date'] = pd.to_datetime(coronaIndia['Date'])

coronaIndia.dropna(inplace=True)

coronaIndia.to_excel(r'C:\Users\arkan\Desktop\CovidIndiaData.xlsx',index = False)






