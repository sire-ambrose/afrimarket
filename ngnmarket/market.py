import requests
import pandas as pd
from datetime import datetime
import re
from bs4 import BeautifulSoup
import json
from selenium import webdriver


class Stock:
    def __init__(self, ticker) -> None:
        self.ticker=ticker
    def getprice(self):
        lower_ticker= self.ticker.lower()
        r= requests.get(f'https://afx.kwayisi.org/chart/ngx/{lower_ticker}')
        data= str(r.content)
        pattern = r'd\("(\d{4}-\d{2}-\d{2})"\),(\d+\.\d+)'
        matches = re.findall(pattern, data)
        date_price_list = []
        for match in matches:
            date_price_list.append((datetime.strptime(match[0], "%Y-%m-%d"), float(match[1])))
        df= pd.DataFrame(date_price_list, columns=['Date', 'Price'])
        return df
    
    def get_price_experimental(self, start, end):
        
        lower_ticker= self.ticker.lower()
        r= requests.get(f'https://www.investing.com/search/?q={lower_ticker}')
        soup= BeautifulSoup(r.content, features='html.parser')
        search_result= soup.find('div', {'class':'js-inner-all-results-quotes-wrapper newResultsContainer quatesTable'})
        for result in search_result:
            if result.find('i') !=-1 and result.find('i') != None:
                if 'Nigeria' in result.find('i')['class']:
                    link= 'https://www.investing.com'+result['href']
                    break
        r= requests.get(link+'-chart')

        soup= BeautifulSoup(r.content, features='html.parser')
        tv_link=soup.find('iframe', {'class': "undefined false"})['src']

        res = dict()
        trunc_tv_link=tv_link[tv_link.find('php?')+4:].split("&")
        
        for i in trunc_tv_link:
            a,b=i.split("=")
            res[a]=b

        # Convert the date string to a datetime object
        start = str(int(datetime.strptime(start, '%d-%m-%Y').timestamp() ))
        end = str(int(datetime.strptime(end, '%d-%m-%Y').timestamp()))

        data_link='https://tvc4.investing.com/'+res['carrier']+'/'+res['time']+'/'+res['domain_ID']+'/'+res['lang_ID']+'/'+res['timezone_ID']+'/'+'history'+'?'+'symbol='+res['pair_ID']+'&'+'resolution=D&from='+start+'&to='+end
        print(data_link)
        driver = webdriver.Chrome()
        driver.get(data_link)
        #https://chromedriver.storage.googleapis.com/index.html?path=79.0.3945.36/

        r= driver.page_source
        soup= BeautifulSoup(r, 'html.parser')

        '''
        print(data_link)
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                 'Cookie':"__cf_bm=vWFXMO.sZQjjMd_dcbHhr3BNG3J8oVMxL50SAp_J8gE-1708149530-1.0-AYR5232kdw5z8gcHkkUaaYLSMaZXh0RE4YGhiHb9gPmmUi8cXno4PnJQ2cPRfdWBEEK8kUDRnrOgSP9LAUJ+ieiCW6uRzYL/PAAjsaD08IQH"}
                          # __cf_bm=BB3aw1nXKOryR_xthtnENBKFcuC0MPJiLeGOmRC_ddE-1708563134-1.0-AU7GCRk9oXfCgW82NKYmRYTab3WO4QnxUGu5Wyz7qAG52kJm003Bqiz0RqS8tQS/bSNhaQG8q1+iZGb6yByG/X0NrXseAa7lGl4WsZG5pm0
        r= requests.get(data_link, headers=headers)
        '''
        
        data_dict= json.loads(soup.find('body').contents[0])
        data_dict.pop('s', None)
        df= pd.DataFrame(data_dict)
        return df
    
    def trading_info(self):
        upper_ticker= self.ticker.upper()
        url= f'https://ngxgroup.com/exchange/data/company-profile/?symbol={upper_ticker}&directory=companydirectory'
        df= pd.read_html(url, match='Market Cap')[0]
        return df
    
    def profile(self):
        upper_ticker= self.ticker.upper()
        url= f'https://ngxgroup.com/exchange/data/company-profile/?symbol={upper_ticker}&directory=companydirectory'
        df= pd.read_html(url, match='Telephone')[0]
        return df
    
    def last_7_days(self):
        upper_ticker= self.ticker.upper()
        url= f'https://ngxgroup.com/exchange/data/company-profile/?symbol={upper_ticker}&directory=companydirectory'
        df= pd.read_html(url, match='Volume')[0]
        return df