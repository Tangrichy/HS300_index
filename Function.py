from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def signal(x, up_bond = 0.95, low_bond= 0):
    if x > up_bond:
        return 1
    elif x< low_bond:
        return -1
    else:
        return 0
    


def backtest(signal_data, price_data, holding_period, direction):

    ## data process
    signal_data = signal_data.reset_index()
    price_data = price_data.reset_index()
    # Merge the signal and price data on the date column
    merged_data = signal_data.merge(price_data, on='Date')

    ## direct
    if direction == "long":
        trading_direction = -1
    elif direction == "short":
        trading_direction = 1

    # Initialize the order book as an empty list
    order_book = []
    
    # Iterate over the merged data to simulate trades
    for i in range(len(merged_data)):
        # Check if the signal is 1 (buy signal)
        if merged_data.loc[i, 'Signal'] == trading_direction:
            # Calculate the date to sell the stock
            sell_date_index = i + holding_period + 1
            if sell_date_index >= merged_data.shape[0]:
                sell_date_index = merged_data.shape[0] - 1
            else:
                pass
            
            # Calculate the profit from the trade
            buy_price = merged_data.iloc[(i+1), 2]
            sell_price = merged_data.iloc[sell_date_index, 2]
            profit = sell_price - buy_price
            
            # Add the trade to the order book
            trade = {'date': merged_data.loc[(i+1), 'Date'], 'buy_price': buy_price, 'sell_price': sell_price, 'profit': profit}
            order_book.append(trade)
    
    # Calculate the total profit from the trades
    total_profit = sum(trade['profit'] for trade in order_book)
    
    return order_book, total_profit

# generate rank

def variable_rank(data, inital_window, sort = True,index = True):
    # sort = False, ascending
    # index = True, if data has a date index
    if index == False:
        data = data.set_index("Date")
    else:
        pass

    data = data.rolling(inital_window).rank(pct = True, ascending = sort).dropna()


    data = data.reset_index()

    return data

# Generate signal for trade

def low_singal(data, low_bond, low_clear):

    singal_long = ["Keep"]
    long_position = [0]
    long = 0

    for i in range(0, (len(data)-2)):
        if data.iloc[i,1] <= low_bond:
            long +=1
            singal_long.append("Long")
            long_position.append(long)
            print(f"Make long position at {data.Date[(i+1)]}")
        
        elif (data.iloc[i,1] >= low_clear) &  (long>0):
            long_position.append(long)
            singal_long.append("Clear")
            long = 0
        
        else:
            singal_long.append("Keep")
            long_position.append(long)
    singal_long.append("Clear")
    long_position.append(long)
    output = {"Date": data.Date, 
              "Signal_long": singal_long, 
              "Long_position": long_position}
    output = pd.DataFrame(output)

    return output

def upper_singal(data, upper_bond, upper_clear):

    singal_short = ["Keep"]
    short_position = [0]
    short = 0

    for i in range(0, (len(data)-2)):
        if data.iloc[i,1] >= upper_bond:
            short +=1
            singal_short.append("Short")
            short_position.append(short)
            print(f"Make short position at {data.Date[(i+1)]}")
        
        elif (data.iloc[i,1] <= upper_clear) &  (short>0):
            short_position.append(short)
            singal_short.append("Clear")
            short = 0
        
        else:
            singal_short.append("Keep")
            short_position.append(short)
    
    short_position.append(short)
    singal_short.append("Clear")

    output = {"Date": data.Date, 
              "Signal_short": singal_short, 
              "Short_position": short_position}
    output = pd.DataFrame(output)

    return output

#######
def low_singal_two(data, low_bond, low_clear):

    singal_long = ["Keep"]
    long_position = [0]
    long = 0

    for i in range(0, (len(data)-2)):
        if data.iloc[i,1] <= low_bond or data.iloc[i,2] <= low_bond:
            long +=1
            singal_long.append("Long")
            long_position.append(long)
            print(f"Make long position at {data.Date[(i+1)]}")
        
        elif (data.iloc[i,1] >= low_clear or data.iloc[i,2]>=low_clear) &  (long>0):
            long_position.append(long)
            singal_long.append("Clear")
            long = 0
        
        else:
            singal_long.append("Keep")
            long_position.append(long)
    singal_long.append("Clear")
    long_position.append(long)
    output = {"Date": data.Date, 
              "Signal_long": singal_long, 
              "Long_position": long_position}
    output = pd.DataFrame(output)

    return output

def upper_singal_two(data, upper_bond, upper_clear):

    singal_short = ["Keep"]
    short_position = [0]
    short = 0

    for i in range(0, (len(data)-2)):
        if data.iloc[i,1] >= upper_bond or data.iloc[i,2] >= upper_bond:
            short +=1
            singal_short.append("Short")
            short_position.append(short)
            print(f"Make short position at {data.Date[(i+1)]}")
        
        elif (data.iloc[i,1] <= upper_clear or data.iloc[i,2] <= upper_clear) &  (short>0):
            short_position.append(short)
            singal_short.append("Clear")
            short = 0
        
        else:
            singal_short.append("Keep")
            short_position.append(short)
    
    short_position.append(short)
    singal_short.append("Clear")

    output = {"Date": data.Date, 
              "Signal_short": singal_short, 
              "Short_position": short_position}
    output = pd.DataFrame(output)

    return output

#######

pe_low_signal = low_singal(data = pbpe_rank, low_bond=0.05, low_clear=0.4)
pe_upper_signal = upper_singal(data = pbpe_rank, upper_bond=0.95, upper_clear=0.7)

## backtest for daily profit

def back_test_long(price_data, signal_data):
    data = price_data.merge(signal_data)
    
    data["Position_shift"] = data["Long_position"].shift()
    data["daily_Profit"] = (data["HS300_close"].diff() * data["Position_shift"]).fillna(0)
    data["Profit"] = data["daily_Profit"].cumsum()

    return data

def back_test_short(price_data, signal_data):
    data = price_data.merge(signal_data)
    
    data["Position_shift"] = data["Short_position"].shift()
    data["daily_Profit"] = (-(data["HS300_close"].diff()) * data["Position_shift"]).fillna(0)
    data["Profit"] = data["daily_Profit"].cumsum()

    return data

def dual_plot(price_data, factor_data):

    fig, ax1 = plt.subplots(num = 1, figsize = (12,6))
    plt.grid(1)
    ax1.plot(factor_data.Date, factor_data.iloc[:,1], color = 'blue', label = factor_data.iloc[:,1].name)
    ax1.set_ylabel(factor_data.iloc[:,1].name)
    ax2 = ax1.twinx()
    ax2.plot(price_data.Date, price_data.iloc[:,1], color = 'orange', label = "Close")
    ax2.set_ylabel("Close")
    ax1.set_xlabel("Date")
    plt.title(f"{factor_data.iloc[:,1].name} and Close")
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 +labels2, loc = "best")
    plt.show()