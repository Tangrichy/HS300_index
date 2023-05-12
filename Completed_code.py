from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Some baisc defined function
## create signal
## Used with apply
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

# evaluation factor

df = pd.read_excel("./HS300_data_updated.xlsx")
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index('Date')

## Select data
pe = df[['HS300_pe']]
pb = df[['HS300_pb']]
close = df[['HS300_close']]
close = close[close.index >= "2018-01-01"]
roverrt = df[["HS300_risk"]]

## Rank

# obtain rank
pe_rank= pe.rolling(1216).rank(pct= True).dropna()
pb_rank = pb.rolling(1216).rank(pct= True).dropna()
roverrt_rank = roverrt.rolling(1216).rank(pct = True, ascending=False).dropna()

pbpe = (pe_rank["HS300_pe"] + pb_rank["HS300_pb"])/2
pbpe_rank = pd.DataFrame(pbpe, index=pbpe.index, columns= ["HS300_pbpe"])

pe_rank = pe_rank.reset_index()
pb_rank =pb_rank.reset_index()
roverrt_rank = roverrt_rank.reset_index()
pbpe_rank = pbpe_rank.reset_index()
close = close.reset_index()
## plot

##PB

fig, ax1 = plt.subplots(num = 1, figsize = (12,6))
plt.grid(1)
ax1.plot(pb_rank.Date, pb_rank['HS300_pb'], color = 'blue', label = "PB")
ax1.set_ylabel("PE")
ax2 = ax1.twinx()
ax2.plot(close.Date, close['HS300_close'], color = 'orange', label = "Close")
ax2.set_ylabel("Close")
ax1.set_xlabel("Date")
plt.title("PB and Close")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 +labels2, loc = "best")
plt.show()


## PE
fig, ax1 = plt.subplots(num = 1, figsize = (12,6))
plt.grid(1)
ax1.plot(pe_rank.Date, pe_rank['HS300_pe'], color = 'blue', label = "PE")
ax1.set_ylabel("PE")
ax2 = ax1.twinx()
ax2.plot(close.Date, close['HS300_close'], color = 'orange', label = "Close")
ax2.set_ylabel("Close")
ax1.set_xlabel("Date")
plt.title("PE and Close")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 +labels2, loc = "best")
plt.show()

## PBPE
fig, ax1 = plt.subplots(num = 1, figsize = (12,6))
plt.grid(1)
ax1.plot(pbpe_rank.Date, pbpe_rank['HS300_pbpe'], color = 'blue', label = "PBPE")
ax1.set_ylabel("PBPE")
ax2 = ax1.twinx()
ax2.plot(close.Date, close['HS300_close'], color = 'orange', label = "Close")
ax2.set_ylabel("Close")
ax1.set_xlabel("Date")
plt.title("PBPE and Close")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 +labels2, loc = "best")
plt.show()


## risk
fig, ax1 = plt.subplots(num = 1, figsize = (12,6))
plt.grid(1)
ax1.plot(roverrt_rank.Date, roverrt_rank['HS300_risk'], color = 'blue', label = "ROVERRT")
ax1.set_ylabel("roverrt")
ax2 = ax1.twinx()
ax2.plot(close.Date, close['HS300_close'], color = 'orange', label = "Close")
ax2.set_ylabel("Close")
ax1.set_xlabel("Date")
plt.title("ROVERRT and Close")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 +labels2, loc = "best")
plt.show()

## risk and pbpe

fig, ax1 = plt.subplots(num = 1, figsize = (12,6))
plt.grid(1)
ax1.plot(roverrt_rank.Date, roverrt_rank['HS300_risk'], color = 'blue', label = "ROVERRT")
ax1.plot(roverrt_rank.Date, pbpe_rank['HS300_pbpe'], color = 'green', label = "PBPE")
ax1.set_ylabel("roverrt")
ax2 = ax1.twinx()
ax2.plot(close.Date, close['HS300_close'], color = 'orange', label = "Close")
ax2.set_ylabel("Close")
ax1.set_xlabel("Date")
plt.title("ROVERRT and Close")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 +labels2, loc = "best")
plt.show()

### Note: Consider pbpe and risk at same time. PBPE or risk achieve the low 5% or high 95%
### it will relase long or short signal
### PBPE or risk achieve 60% or 40% after reach low bond or high bond

### back test for hold a constant period
## creat signal for each factor
pe_rank['Signal'] = pe_rank['HS300_pe'].apply(signal)
pb_rank['Signal'] = pb_rank['HS300_pb'].apply(signal)
pbpe_rank['Signal'] = pbpe_rank['HS300_pbpe'].apply(signal)
roverrt_rank['Signal'] = roverrt_rank['HS300_risk'].apply(signal)

## Back test

pbpe_test = backtest(signal_data=pbpe_rank[["Signal"]],
         price_data=close,
         holding_period=90,
         direction= "long")



# date for crowded

df_corr = pd.read_excel("./HS300_data_updated.xlsx", sheet_name="Sheet2")
df_corr = df_corr.set_index("Date")
price = df_corr[["close"]]

# crowded

std = np.std

## risk variance
log_ret= np.log(price["close"].pct_change() + 1)
log_ret = pd.DataFrame(log_ret)
ret_var = log_ret.rolling(20).std(ddof=1).dropna()
var_rank = variable_rank(data=ret_var, inital_window=1196)

### plot

fig, ax1 = plt.subplots(num = 1, figsize = (12,6))
plt.grid(1)
ax1.plot(var_rank.Date, var_rank['close'], color = 'blue', label = "std")
ax1.set_ylabel("Var")
ax2 = ax1.twinx()
ax2.plot(close.Date, close['HS300_close'], color = 'orange', label = "Close")
ax2.set_ylabel("Close")
ax1.set_xlabel("Date")
plt.title("risk and Close")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 +labels2, loc = "best")
plt.show()

## momentum
### pct change

price = df_corr[["close"]]
exp_fun = np.log(price.pct_change()+1).rolling(20).sum() ##### exp 

exp_rank = variable_rank(data = exp_fun, inital_window=1215)
exp_rank["Signal"] = exp_rank["close"].apply(signal)

fig, ax1 = plt.subplots(num = 1, figsize = (12,6))
plt.grid(1)
ax1.plot(exp_rank.Date, exp_rank['close'], color = 'blue', label = "exp")
ax1.set_ylabel("Var")
ax2 = ax1.twinx()
ax2.plot(close.Date, close['HS300_close'], color = 'orange', label = "Close")
ax2.set_ylabel("Close")
ax1.set_xlabel("Date")
plt.title("exp and Close")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 +labels2, loc = "best")
plt.show()

## correlation
close_volume = df_corr[["close", "volume"]]
close_amt = df_corr[["close", "amt"]]
close_turn = df_corr[["close", "turn"]]

## generate correlation function
def corr_fun(data, inital):
    corr_matrix = data.rolling(inital).corr()
    corr_matrix = corr_matrix.reset_index()
    corr_matrix = corr_matrix[corr_matrix["level_1"] != 'close']
    output = {"Date":corr_matrix['Date'], "Corr": corr_matrix["close"]}
    output = pd.DataFrame(output)
    output = output.dropna()

    return(output)

close_volume_corr = corr_fun(data=close_volume, inital=1216)
close_amt_corr = corr_fun(data=close_amt, inital=1216)
close_turn_corr = corr_fun(data=close_turn, inital=1216)

## skew kurt
ret_skew = log_ret.rolling(20).skew()
ret_kur = log_ret.rolling(20).kurt()

##  bias

bais = (df_corr - df_corr.rolling(60).mean())/df_corr.rolling(60).mean()
bais = bais.dropna()
close_bais = bais[["close"]]
tradevol_bais = bais[["volume"]]
amt_bais = bais[["amt"]]
turn_bais = bais[["turn"]]

turn_rank = variable_rank(data = turn_bais, inital_window=1157)
turn_rank["Signal"] = turn_rank["turn"].apply(signal)

## generate signal with crowded variable
def low_singal_crowded(data, low_bond, low_clear, crowded_data, after_day):
    data = crowded_data.merge(data, on = "Date")

    singal_long = ["Keep"]
    long_position = [0]
    long = 0
    tagret_date = 0

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
        
        elif (crowded_data.loc[i,"Signal"] == True) & (long>0):
            tagret_date = i + after_day
            long_position.append(long)
            singal_long.append("Keep")
        
        elif (i == tagret_date) & (long>0):
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
            
signal_long = low_singal_crowded(data = pbpe_rank, low_bond = 0.05, low_clear = 0.6, crowded_data = var_rank, after_day=10)

close_amt_corr["Signal"]=close_amt_corr["Corr"].apply(signal)
close_volume_corr["Signal"]=close_volume_corr["Corr"].apply(signal)
close_turn_corr["Signal"] = close_turn_corr["Corr"].apply(signal)

signal_crowded=close_amt_corr.merge(close_volume_corr, on = "Date").merge(close_turn_corr, on = "Date").merge(turn_rank, on = "Date")
trading_crow =low_singal_crowded(data = pbpe_rank, low_bond = 0.05, low_clear = 0.6, crowded_data = signal_crowd, after_day=10)