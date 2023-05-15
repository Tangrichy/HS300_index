df_corr = pd.read_excel("./HS300_data_updated.xlsx", sheet_name="Sheet2")
df_corr = df_corr.set_index("Date")
price = df_corr[["close"]]

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