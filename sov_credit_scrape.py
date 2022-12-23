import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import datetime

from datetime import datetime #need it exactly like this

#You are calling this
def credit_get(country_list):

    df = pd.DataFrame()

    for x in country_list:
        print(x)
        df[x] = sov_cred(x)

    return df

def sov_cred(country):

    #Source of the data. 
    source = 'snp'

    URL = "http://www.worldgovernmentbonds.com/credit-rating/"+country+"/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
        

    # Generate a range of dates
    dates = pd.date_range(start='1990-01-01', end=datetime.today())

    # Create an empty DataFrame with the dates as the index to fill it in later
    df = pd.DataFrame(index=dates)
    df[source] = ""
    df[source+'_num'] = ""


    result_table = soup.find_all("div", class_="w3-responsive")[2:3]

    #Multiple tables with same identification.. Mad anyoying!!! so i put arrary in the end to deal with it.
    result_table = soup.find_all("table", class_="w3-table w3-white table-padding-xsmall w3-small font-family-arial table-valign-middle", style = "border:0;white-space:nowrap;margin-bottom:0px;")[1]

    rows = result_table.find_all('tbody')[0].find_all("tr")

    dict_rate_convert = {
        "snp":{
            'AAA':21,
            'AA+':20,
            'AA':19,
            'AA-':18,
            'A+':17,
            'A':16,
            'A-':15,
            'BBB+':14,
            'BBB':13,
            'BBB-':12,
            'BB+':11,
            'BB':10,
            'BB-':9,
            'B+':8,
            'B':7,
            'B-':6,
            'CCC+':5,
            'CCC':4,
            'CCC-':3,
            'CC':2,
            'C':1,
            'RD':-1,
            'SD':-2,
            'D•NR':-3,        
            '':''
        },
        "mood":{
            'Aaa':21,
            'Aa1':20,
            'Aa2':19,
            'Aa3':18,
            'A1':17,
            'A2':16,
            'A3':15,
            'Baa1':14,
            'Baa2':13,
            'Baa3':12,
            'Ba1':11,
            'Ba2':10,
            'Ba3':9,
            'B1':8,
            'B2':7,
            'B3':6,
            'Caa1':5,
            'Caa2':4,
            'Caa3':3,
            'Ca':2,
            'C':1,
            '/':-1,
            'D•NR':-3,    
            '':''

        },
    "fit":{
        'AAA':21,
        'AA+':20,
        'AA':19,
        'AA-':18,
        'A+':17,
        'A':16,
        'A-':15,
        'BBB+':14,
        'BBB':13,
        'BBB-':12,
        'BB+':11,
        'BB':10,
        'BB-':9,
        'B+':8,
        'B':7,
        'B-':6,
        'CCC+':5,
        'CCC':4,
        'CCC-':3,
        'CC':2,
        'C':1,
        'RD':-1,
        'SD':-2,
        'D•NR':-3, 
        '':''
        }

    }

    for elem in rows[0:]:
        
        date = date_convert(elem.find_all("td")[0].text.strip()) #Calling the function to recorrect the format of the date.
        snp = elem.find_all("td")[1].text.strip()
        mood = elem.find_all("td")[2].text.strip()
        fitch = elem.find_all("td")[3].text.strip()

        count = 1 #Count has to be one.
        while count != len(df):

            #Changing the format of the date
            date_format_2=datetime.fromtimestamp(int(str(df.index[len(df)-count].value)[0:10])).replace(hour=0, minute=00)
    
            #Note that the date stars of latest so we are filling the df from the last data point
            if date == date_format_2:
                df[source][len(df)-count] = snp
                df[source+'_num'][len(df)-count] = dict_rate_convert[source][snp]

            count+=1    

    for i in range(1,len(df)):
        for col in df.columns.values:
            if df[col][i] == "":
                df[col][i] = df[col][i-1]


    return df[source+'_num']

#to convert the dates
def date_convert(date_input):
    date_input_arr = date_input.split()

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_index = months.index(date_input_arr[1]) + 1
    day = int(date_input_arr[0])
    year = int(date_input_arr[2])

    date_format = datetime(year,month_index, day, 0, 0)
    
    return date_format

