import finnhub
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
from createTable import *

def getWeekday(date_start, date_end):
    input_format = "%Y-%m-%d"
    date_start = datetime.strptime(date_start, input_format) 
    date_end = datetime.strptime(date_end, input_format) 
    
    weekdays = []
    current_date = date_start 
    
    while current_date <= date_end:
        if current_date.weekday() < 5:  # Monday to Friday have weekday numbers 0 to 4
            weekdays.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)

    return weekdays

def getEarningsDateTicker(days, date_start, date_end): 
    finalList = {}
    finnhub_client = finnhub.Client(api_key="cj2rpt9r01qr0f6fr99gcj2rpt9r01qr0f6fr9a0") 
    data = finnhub_client.earnings_calendar(_from=date_start, to=date_end, symbol="", international=False)
    for day in days:
        dayList = []
        data['earningsCalendar'] = [entry for entry in data['earningsCalendar'] if entry['revenueEstimate'] is not None]
        # Filter entries with the date
        entries = [entry for entry in data['earningsCalendar'] if entry['date'] == day]
        # Sort the filtered entries by revenueActual in descending order
        sorted_entries = sorted(entries, key=lambda x: x['revenueEstimate'], reverse=True)
        
        for i in range(5): 
            if sorted_entries[i] == None: 
                break
            dayList.append(sorted_entries[i]['symbol'] )
        finalList[day] = dayList
        
    return finalList

def createEarningsTables(date_start, date_end): 
    weekdays = getWeekday(date_start, date_end)
    tickerDates = getEarningsDateTicker(weekdays, date_start, date_end)
    
    regularTableFramesTotal = pd.DataFrame()
    for entry in tickerDates: 
        regularTableFramesDay = pd.DataFrame([[entry, '', '', '', '', '', '', '', '']], 
                                             columns=['Company Name', 
                                                    'Current Price', 
                                                    '52-Week Low', 
                                                    '52-Week High', 
                                                    'EPS', 
                                                    'Dividend Rate', 
                                                    'Price Change Week', 
                                                    'Price Change Month', 
                                                    'Price Change Quarter'])
        for symbol in tickerDates[entry]: 
            ticker = yf.Ticker(symbol)
            regularTableFramesDay = pd.concat([regularTableFramesDay, createGeneralTable(symbol, ticker)])

        regularTableFramesTotal = pd.concat([regularTableFramesTotal, regularTableFramesDay], ignore_index=True)
        
    return regularTableFramesTotal


