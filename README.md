# EarningsAnalyzer
The motivation of this project is to try and visualize the impact that quarterly earnings reports have on stock prices. This project aggregates and analyzes the data of stocks 
to generate concise tables of key financial metrics and historical price effects of earnings report on stocks. Moving forward, this project would seek to make predictions on stock 
prices post-earnings based on key financial metrics leading up to the earnings report. 

# Dependencies
- pip install yfinance
- pip install numpy
- pip install pandas
- pip install finnhub-python
- pip install bs4

# Instructions

Command: `python main.py <function> <ticker> <date_start (%Y-%M-%D)> <date_end (%Y-%M-%D)>`

Functions:
- `stock` (A table with key financial metrics of a given stock and a table with the post-earnings impact of the stock in the past 4 quarters)
- `earnings` (A table with post-earnings impact of the stocks with the top 5 market cap that has its earnings release for a given day)

Examples:

- `python main.py stock AAPL`
- `python main.py earnings none 2023-05-10 2023-05-15`
