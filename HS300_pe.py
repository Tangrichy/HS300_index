from iFinDPy import *
from datetime import datetime
import pandas as pd
import numpy as np
#import datetimefrom threading import Thread,Lock,Semaphore
import matplotlib.pyplot as plt

# login 

sem = Semaphore(5) 
def thslogindemo():
    # 输入用户的帐号和密码
    thsLogin = THS_iFinDLogin("jyzc159","404426")
    print(thsLogin)
    if thsLogin != 0:
        print('登录失败')
    else:
        print('登录成功')

thslogindemo()

# df_pe = THS_DS('000300.SH','ths_pe_index','101,100','block:history','2013-01-01','2023-01-01')

# df_pe_ttm = THS_DS('000300.SH','ths_pe_ttm_index','100,100','block:history','2013-01-01','2023-01-01')

# input data
df = pd.read_excel("./HS300_wind_data.xlsx")
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index('Date')
#df['ROVERRT'] =   (1/df['HS300_pe_ttm'])*100 - df["yield"]
df["pepb"] = (df["HS300_pe_ttm"] + df["HS300_pb"])/2

# select data
pe_ttm = df[['HS300_pe_ttm']]
#pe = df[['HS300_pe']]
pb = df[['HS300_pb']]
close = df[['HS300_close']]
close = close[close.index >= "2018-01-01"]
roverrt = df[["ROVERRT"]]
df_pepb = df[["pepb"]]

# obtain rank
pe_rank = pe_ttm.rolling(1216).rank(pct= True).dropna()
pe_ttm_rank = pe_ttm.rolling(1216).rank(pct= True).dropna()
pe_rank = pe.rolling(1216).rank(pct= True).dropna()
pb_rank = pb.rolling(1216).rank(pct= True).dropna()
pbpe_rank = df_pepb.rolling(1216).rank(pct= True).dropna()
roverrt_rank = roverrt.rolling(1216).rank(pct = True, ascending=False).dropna()


pbpe = (pe_ttm_rank['HS300_pe_ttm'].values + pb_rank['HS300_pb'].values)/2

df_pepb = {"Date": close.index, "PBPE": pbpe}
df_pepb = pd.DataFrame(df_pepb)
df_pepb = df_pepb.set_index('Date')

# plot
## PE TTM
fig, ax1 = plt.subplots(num = 1, figsize = (12,6))
plt.grid(1)
ax1.plot(pe_ttm_rank.index, pe_ttm_rank['HS300_pe_ttm'], color = 'blue', label = "PE_ttm")
ax1.set_ylabel("PE TTM")
ax2 = ax1.twinx()
ax2.plot(close.index, close['HS300_close'], color = 'orange', label = "Close")
ax2.set_ylabel("Close")
ax1.set_xlabel("Date")
plt.title("PE TTM and Close")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 +labels2, loc = "best")
plt.show()


## PE
fig, ax1 = plt.subplots(num = 1, figsize = (12,6))
plt.grid(1)
ax1.plot(pe_rank.index, pe_rank['HS300_pe'], color = 'blue', label = "PE")
ax1.set_ylabel("PE")
ax2 = ax1.twinx()
ax2.plot(close.index, close['HS300_close'], color = 'orange', label = "Close")
ax2.set_ylabel("Close")
ax1.set_xlabel("Date")
plt.title("PE and Close")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 +labels2, loc = "best")
plt.show()

## PB
fig, ax1 = plt.subplots(num = 1, figsize = (12,6))
plt.grid(1)
ax1.plot(pb_rank.index, pb_rank['HS300_pb'], color = 'blue', label = "PB")
ax1.set_ylabel("PE")
ax2 = ax1.twinx()
ax2.plot(close.index, close['HS300_close'], color = 'orange', label = "Close")
ax2.set_ylabel("Close")
ax1.set_xlabel("Date")
plt.title("PB and Close")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 +labels2, loc = "best")
plt.show()

##PBPE
fig, ax1 = plt.subplots(num = 1, figsize = (12,6))
plt.grid(1)
ax1.plot(pbpe_rank.index, pbpe_rank['pepb'], color = 'blue', label = "PBPE")
ax1.set_ylabel("PBPE")
ax2 = ax1.twinx()
ax2.plot(close.index, close['HS300_close'], color = 'orange', label = "Close")
ax2.set_ylabel("Close")
ax1.set_xlabel("Date")
plt.title("PBPE and Close")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 +labels2, loc = "best")
plt.show()

## ROVERRT
fig, ax1 = plt.subplots(num = 1, figsize = (12,6))
plt.grid(1)
ax1.plot(roverrt_rank.index, roverrt_rank['ROVERRT'], color = 'blue', label = "ROVERRT")
ax1.set_ylabel("PBPE")
ax2 = ax1.twinx()
ax2.plot(close.index, close['HS300_close'], color = 'orange', label = "Close")
ax2.set_ylabel("Close")
ax1.set_xlabel("Date")
plt.title("ROVERRT and Close")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 +labels2, loc = "best")
plt.show()


def backtest(signal_data, price_data, holding_period):
    signal_data = signal_data.reset_index()
    price_data = price_data.reset_index()
    # Merge the signal and price data on the date column
    merged_data = signal_data.merge(price_data, on='Date')
    
    # Initialize the order book as an empty list
    order_book = []
    
    # Iterate over the merged data to simulate trades
    for i in range(len(merged_data)):
        # Check if the signal is 1 (buy signal)
        if merged_data.loc[i, 'Signal'] == (-1):
            # Calculate the date to sell the stock
            sell_date_index = i + holding_period
            if sell_date_index >= merged_data.shape[0]:
                sell_date_index = merged_data.shape[0] - 1
            else:
                pass
            
            # Calculate the profit from the trade
            buy_price = merged_data.iloc[i, 2]
            sell_price = merged_data.iloc[sell_date_index, 2]
            profit = sell_price - buy_price
            
            # Add the trade to the order book
            trade = {'date': merged_data.loc[i, 'Date'], 'buy_price': buy_price, 'sell_price': sell_price, 'profit': profit}
            order_book.append(trade)
    
    # Calculate the total profit from the trades
    total_profit = sum(trade['profit'] for trade in order_book)
    
    return order_book, total_profit


def protfoilo_return(signal_data, price_data, holding, direction, inital_captial = 0.01):
    signal_data = signal_data.reset_index()
    price_data = price_data.reset_index()
    # Merge the signal and price data on the date column
    merged_data = signal_data.merge(price_data, on='Date')

    order_book = []

    ## direct
    if direction == "long":
        trading_direction = -1
    elif direction == "short":
        trading_direction = 1

    total_asset = [inital_captial]
    asset = [inital_captial]
    borrow = 0
    protfolio_pct = []


    for i in range(len(merged_data)):

        temp_pct = asset[i]/total_asset[i]

        if merged_data.loc[i, 'Signal'] == trading_direction:
            sell_date_index = i + holding_period + 1

            if sell_date_index >= merged_data.shape[0]:
                sell_date_index = merged_data.shape[0] - 1
            else:
                pass

        buy_price = merged_data.iloc[(i+1), 2]
        sell_price = merged_data.iloc[sell_date_index, 2]
        profit = sell_price - buy_price

log_ret= np.log(close_risk.pct_change() + 1).dropna()
ret_var = log_ret.rolling(20).var().dropna()
var_rank = ret_var.rolling(1216).rank(pct = True).dropna()

var_rank[::5]

singal_long = [0]
singal_short = [0]
long_position = [0]
short_position = [0]
long = 0
short = 0
for i in range(0, (len(pb_rank)-1)):
    if pb_rank.iloc[i,0] >= 0.95:
        short += 1
        singal_short.append(1)
        short_position.append(short)
        print(f"Make short position at {pb_rank.index[(i+1)]}")
    
    elif pb_rank.iloc[i,0] <= 0.05:
        long += 1
        singal_long.append(1)
        long_position.append(long)
        print(f"Make long position at {pb_rank.index[(i+1)]}")
    
    elif pb_rank.iloc[i,0] <= 0.6 and short>0:
        short = 0
        singal_short.append(0)
        short_position.append("SELL")
    
    elif pb_rank.iloc[i,0] >= 0.4 and long >0:
        long = 0
        singal_long.append(0)
        long_position.append("SELL")
    
    else:
        singal_long.append(0)
        singal_short.append(0)
        short_position.append(short)
        long_position.append(long)


def low_singal(data, low_bond, low_clear):

    singal_long = ["Keep"]
    long_position = [0]
    long = 0

    for i in range(0, (len(data)-1)):
        if data.iloc[i,1] <= low_bond:
            long +=1
            singal_long.append("Long")
            long_position.append(long)
            print(f"Make long position at {data.index[(i+1)]}")
        
        elif (data.iloc[i,1] >= low_clear) &  (long>0):
            long_position.append(long)
            singal_long.append("Clear")
            long = 0
        
        else:
            singal_long.append("Keep")
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

    for i in range(0, (len(data)-1)):
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
    output = {"Date": data.Date, 
              "Signal_short": singal_short, 
              "Short_position": short_position}
    output = pd.DataFrame(output)

    return output


def backtest(price_data, long_data = None):
   
    signal_data = price_data.merge(long_data, on = "Date")
    
    cash_cost = [0]
    cash_live = [0]
    net_value = [1]
    profit = [0]

    temp_cost = 0
    temp_live = 0

    for i in range(1, len(signal_data)):
        if  signal_data.loc[i,"Signal_long"] == "Long":
            temp_cost = signal_data.loc[i,"HS300_close"] + cash_cost[(i-1)]
            cash_cost.append(temp_cost)
            temp_live = signal_data.loc[i,"Long_position"] * signal_data.loc[i,"HS300_close"]
            cash_live.append(temp_live)

        
        elif signal_data.loc[i, "Signal_long"] == "Clear":
            temp_live = signal_data.loc[i,"Long_position"] * signal_data.loc[i,"HS300_close"]
            cash_cost.append(temp_cost)
            cash_live.append(temp_live)
        
        elif (signal_data.loc[i, "Signal_long"] == "Keep") & (signal_data.loc[i, "Long_position"] != 0):
            temp_live = signal_data.loc[i,"Long_position"] * signal_data.loc[i,"HS300_close"]
            cash_live.append(temp_live)
            cash_cost.append(temp_cost)
        
        elif (signal_data.loc[i, "Signal_long"] == "Keep") & (signal_data.loc[i, "Long_position"] == 0):
            cash_cost.append(temp_cost)
            cash_live.append(temp_live)
        
        temp_net = (temp_live+0.000001)/(temp_cost+0.000001)
        net_value.append(temp_net)
        temp_profit = temp_live - temp_cost
        profit.append(temp_profit)
    
    output = {"Date": signal_data.Date,
              "Profit": profit,
              "Net_value": net_value}
    output = pd.DataFrame(output)
    
    return output

cash_cost = [0]
cash_live = [0]
net_value = [1]
temp_cost=0
temp_live = 0
for i in range(1, (len(signal_data))):
        if  signal_data.loc[i,"Signal_long"] == "Long":
            print("Long Position")
            temp_cost = signal_data.loc[i,"HS300_close"] + cash_cost[(i-1)]
            cash_cost.append(temp_cost)
            temp_live = signal_data.loc[i,"Long_position"] * signal_data.loc[i,"HS300_close"]
            cash_live.append(temp_live)

        
        elif signal_data.loc[i, "Signal_long"] == "Clear":
            print("Clear")
            temp_live = signal_data.loc[i,"Long_position"] * signal_data.loc[i,"HS300_close"]
            cash_cost.append(temp_cost)
            cash_live.append(temp_live)
        
        elif (signal_data.loc[i, "Signal_long"] == "Keep") & (signal_data.loc[i, "Long_position"] != 0):
            temp_live = signal_data.loc[i,"Long_position"] * signal_data.loc[i,"HS300_close"]
            cash_live.append(temp_live)
            cash_cost.append(temp_cost)
        
        elif (signal_data.loc[i, "Signal_long"] == "Keep") & (signal_data.loc[i, "Long_position"] == 0):
            cash_cost.append(temp_cost)
            cash_live.append(temp_live)
        
        temp_net = (temp_live+0.001)/(temp_cost+0.001)
        net_value.append(temp_net)

def back_test(price_data, long_data):
    signal_data = price_data.merge(long_data, on = "Date")

    cash_cost = [0]
    cash_live = [0]
    net_value = [1]
    profit = [0]
    temp_cost=0
    temp_live = 0
    for i in range(1, (len(signal_data))):
        if  signal_data.loc[i,"Signal_long"] == "Long":
            #print(f"Long Position {signal_data.Date[i]}")
            temp_cost = signal_data.loc[i,"HS300_close"] + cash_cost[(i-1)]
            cash_cost.append(temp_cost)
            temp_live = signal_data.loc[i,"Long_position"] * signal_data.loc[i,"HS300_close"]
            cash_live.append(temp_live)

        
        elif signal_data.loc[i, "Signal_long"] == "Clear":
            #print(f"clear {signal_data.Date[i]}")
            temp_live = signal_data.loc[i,"Long_position"] * signal_data.loc[i,"HS300_close"]
            cash_cost.append(temp_cost)
            cash_live.append(temp_live)
        
        elif (signal_data.loc[i, "Signal_long"] == "Keep") & (signal_data.loc[i, "Long_position"] != 0):
            temp_live = signal_data.loc[i,"Long_position"] * signal_data.loc[i,"HS300_close"]
            cash_live.append(temp_live)
            cash_cost.append(temp_cost)
        
        elif (signal_data.loc[i, "Signal_long"] == "Keep") & (signal_data.loc[i, "Long_position"] == 0):
            cash_cost.append(temp_cost)
            cash_live.append(temp_live)
            temp_cost = 0
            temp_live = 0
        
        #temp_net = (temp_live+0.001)/(temp_cost+0.001)
        #print(f"Net return is {temp_net}")
        #net_value.append(temp_net)
        
        temp_profit = temp_live - temp_cost

        profit.append(temp_profit)
    output = {"Date": signal_data.Date,
              #"Profit": profit,
              "Net_value": profit,
              "Cost": cash_cost,
              "Live": cash_live}
    
    output = pd.DataFrame(output)

    return output


back_test_price = close[close["Date"] >= "2022-06-01"]
back_test_long = pe_low_signal[pe_low_signal["Date"]>="2022-06-01"]
back_test(price_data=back_test_price, long_data=back_test_long)
net_return= back_test(price_data=close, long_data=pe_low_signal)


df_corr = pd.read_excel("./HS300_data_updated.xlsx", sheet_name="Sheet2")
df_corr = df_corr.set_index("Date")
df_corrpe.rolling(1216).corr().dropna()

def variable_rank(data, inital_window, moving, sort = False,index = True):
    if index == False:
        data = data.set_index("Date")
    else:
        pass

    data = data.rolling(inital_window).rank(pct = True, ascending = sort).dropna()

    data = data[::moving]
    data = data.reset_index()

    return data

df_corr = df_corr.set_index("Date")
df_corr.pct_change()

plt.figure(num = 1, figsize = (12,6))
plt.grid()
plt.plot(close["Date"], close["HS300_close"], label = "Close")
plt.plot(signal_plot['Date'], signal_plot["HS300_close"], "+", label = "Quatil")
#plt.plot(date_long['Date'], date_long["HS300_close"], "ro", label = "Buy")
#plt.plot(date_clear['Date'], date_clear["HS300_close"], "+",label = "Sell")
leg = plt.legend(loc='upper left')
plt.title("YL and WD")
plt.xlabel('Date')
plt.show()


plt.figure(num = 1, figsize=(12,6))
plt.grid(1)
plt.plot(net_return["Date"], net_return["Net_value"], label = "Net")
leg = plt.legend(loc = "upper right")
plt.title("Back test")
plt.xlabel("Date")
plt.show()



df = close.merge(pe_low_signal, on = "Date")
df["Position_shift"] = df["Long_position"].shift()
df["Profit"] = (df["HS300_close"].diff() * df["Position_shift"]).fillna(0)

plt.figure(num = 1, figsize=(12,6))
plt.grid(1)
plt.plot(df["Date"], df["Profit"].cumsum(), label = "Net")
leg = plt.legend(loc = "upper right")
plt.title("Back test")
plt.xlabel("Date")
plt.show()

plt.figure(num = 1, figsize=(12,6))
plt.grid(1)
plt.plot(profit.Date, profit["daily_Profit"].cumsum(), label = "Profit")
leg = plt.legend(loc = "upper right")
plt.title("Back test")
plt.xlabel("Date")
plt.show()