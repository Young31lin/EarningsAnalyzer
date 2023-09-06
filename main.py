import sys
from Stock import *
from EarningsCalendarMetadata import *

def main(function, symbol, date_start, date_end): 
    if function == "stock": 
        entry = Stock(symbol)
        return entry.createTable(), entry.createEarningsImpactTable()
    if function == "earnings": 
        entry = EarningsCalendarMetadata()
        return entry.getEarningsCalendarData(date_start, date_end)

    return



if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) < 3:
        print("Usage: python main.py <function> <ticker> <date_start> <date_end>")
        sys.exit(1)

    # Get the function from the command-line argument
    function = sys.argv[1]

    # Get the ticker from the command-line argument
    symbol = sys.argv[2]

    date_start = ""
    date_end = ""

    if len(sys.argv) > 3:
        date_start = sys.argv[3]
        date_end = sys.argv[4]

    # Call the createEarningsImpactTable function with the ticker input
    result_df = main(function, symbol, date_start, date_end)

    # Print the result DataFrame
    print(result_df)
