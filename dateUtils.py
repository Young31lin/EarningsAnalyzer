import pandas as pd

def find_next_business_day(date):
    # Find the next business day after the given date
    next_business_day = pd.date_range(start=date, freq=pd.offsets.BDay(), periods=1)[0]
    return next_business_day

def find_previous_business_day(date):
    # Find the previous business day before the given date
    previous_business_day = pd.date_range(end=date, freq=pd.offsets.BDay(), periods=1)[0]
    return previous_business_day
