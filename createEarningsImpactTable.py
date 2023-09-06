import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from dateUtils import *

def createEarningsImpactTable(ticker, symbol): 
    #Sort the earnings date in descending order
    earningsRaw = ticker.earnings_dates
    datesUnprocessed = sorted(list(earningsRaw.index), reverse = True)

    #Extract the four most recent earnings date and add it to a dates list
    dates = extractEarningDates(datesUnprocessed, earningsRaw)

    #Extract the price for the day before, the day of, and the day after
    price_list = extractPrice(dates, symbol)
    
    percentChange = computeChange(price_list, earningsRaw)

    return pd.DataFrame(percentChange, columns=['Year', 'Quarter', 'EPS Estimate Beat', 'Earnings Price Effects'])

def extractEarningDates(datesUnprocessed, earningsRaw): 
    dates = []
    for date in datesUnprocessed: 
        if len(dates) == 4: break
        dateProcessed = date.strftime('%Y-%m-%d')
        if not np.isnan(earningsRaw.loc[dateProcessed]['Surprise(%)'][0]): 
            dates.append(dateProcessed)
    return dates

def extractPrice(dates, symbol): 
    price_list = []
    for date in dates: 
        date = datetime.strptime(date, '%Y-%m-%d')
        dayBefore = find_previous_business_day(date.date()- pd.Timedelta(days=1))
        dayAfter = find_next_business_day(date.date()+timedelta(days=2))
        price = yf.download(symbol,dayBefore,dayAfter)
        price_list.append(price)
    return price_list

def computeChange(price_list, earningsRaw): 
    percentChange = []
    for price in price_list: 
        try:
            priceBefore = price.iloc[0, price.columns.get_loc('Close')]
        except (IndexError, KeyError):
            priceBefore = None

        try:
            priceAfter = price.iloc[2, price.columns.get_loc('Open')]
        except (IndexError, KeyError):
            priceAfter = None

        epsChange = earningsRaw.loc[price.index[1].strftime('%Y-%m-%d')]['Surprise(%)'][0]*100
        timestamp = price.index[1]
        year = timestamp.year
        quarter = (timestamp.month - 1) // 3 + 1
        if not priceAfter or not priceBefore: 
            percentChange.append([year, 
                                  f"Q{quarter}", 
                                  f"{epsChange}%", 
                                  None])
        else: 
            percentChange.append([year, 
                                  f"Q{quarter}", 
                                  f"{epsChange}%", 
                                  f"{round(((priceAfter - priceBefore)/priceBefore)*100, 2)}%"
                                ])
    return percentChange
        
