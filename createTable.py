import yfinance as yf
from datetime import timedelta, date
import pandas as pd
from dateUtils import *
from fetch import *

def createGeneralTable(symbol, ticker): 
    percentChange = getPriceChange(symbol)
    dividendRate = ticker.info.get('dividendRate', None)
    basicData = [[f"{ticker.info['longName']} ({symbol})", 
             float(getQuote(symbol)), 
             ticker.info.get('fiftyTwoWeekLow', None), 
             ticker.info.get('fiftyTwoWeekHigh', None), 
             ticker.info.get('trailingEps', None), 
             f"{dividendRate}%" if dividendRate is not None else None, 
             percentChange[0], 
             percentChange[1], 
             percentChange[2]]]
    return pd.DataFrame(basicData, 
                        columns=['Company Name', 
                                 'Current Price', 
                                 '52-Week Low', 
                                 '52-Week High', 
                                 'EPS',
                                 'Dividend Rate', 
                                 'Price Change Week', 
                                 'Price Change Month', 
                                 'Price Change Quarter'])

def getPriceChange(symbol): 
    #Get valid date time
    dateWeek = find_previous_business_day(date.today() - timedelta(days=7))
    dateMonth = find_previous_business_day(date.today() - timedelta(days=30))
    dateQuarter = find_previous_business_day(date.today() - timedelta(days=90))

    #Get price at each date point
    currentPrice = float(getQuote(symbol))
    priceLastWeek = yf.download(symbol,dateWeek-timedelta(days=1))['Close']
    priceLastMonth = yf.download(symbol,dateMonth-timedelta(days=1))['Close']
    priceLastQuarter = yf.download(symbol,dateQuarter-timedelta(days=1))['Close']

    #Calculate percentage difference
    pastWeek = f"{round(((currentPrice - priceLastWeek[0])/priceLastWeek[0])*100, 2)}%"
    pastMonth = f"{round(((currentPrice - priceLastMonth[0])/priceLastMonth[0])*100, 2)}%"
    pastQuarter = f"{round(((currentPrice - priceLastQuarter[0])/priceLastQuarter[0])*100, 2)}%"

    return [pastＷeek, pastMonth, pastQuarter]