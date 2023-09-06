import yfinance as yf
from createTable import *
from createEarningsImpactTable import *
from fetch import *

class Stock: 
    def __init__(self, symbol): 
        self.symbol = symbol 
        self.__ticker = yf.Ticker(symbol)
        self.price = getQuote(symbol)

    def createTable(self): 
        return createGeneralTable(self.symbol, self.__ticker)
    
    def createEarningsImpactTable(self): 
        return createEarningsImpactTable(self.__ticker,self.symbol)
