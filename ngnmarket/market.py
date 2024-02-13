import requests
import pandas as pd
from datetime import datetime
import re


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


stock= Stock('ABCTRANS')
print(stock.last_7_days())
