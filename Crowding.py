df_corr = pd.read_excel("./HS300_data_updated.xlsx", sheet_name="Sheet2")
df_corr = df_corr.set_index("Date")
price = df_corr[["close"]]

# crowded

std = np.std

## risk variance
log_ret= np.log(price["close"].pct_change() + 1)
log_ret = pd.DataFrame(log_ret)
window_ret = len(ret_var[ret_var.index <= "2018-01-01"]) + 1
ret_var = log_ret.rolling(20).std(ddof=1).dropna() # window is 20 trading-days
var_rank = variable_rank(data=ret_var, inital_window=window_ret)

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
exp_fun = np.log(price.pct_change()+1).rolling(20).sum() ##### exp window 20

window_exp = len(exp_fun[exp_fun.index <= "2018-01-01"]) + 1


exp_rank = variable_rank(data = exp_fun, inital_window=window_exp)

dual_plot(price_data = close, factor_data = exp_rank)

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

close_volume_corr = corr_fun(data=close_volume, inital=20) # window is 20
close_amt_corr = corr_fun(data=close_amt, inital=20)
close_turn_corr = corr_fun(data=close_turn, inital=20)

window_cor = len(close_volume_corr[close_volume_corr["Date"] <= "2018-01-01"]) + 1


close_volume_rank = variable_rank(data = close_volume_corr, inital_window=window_cor, index = False)
close_amt_rank = variable_rank(data = close_amt_corr, inital_window=window_cor, index = False)
close_turn_rank = variable_rank(data = close_turn_corr, inital_window=window_cor, index = False)

dual_plot(price_data=close, factor_data=close_volume_rank, title = "Close volume and Price", y_axis="Volume")
dual_plot(price_data=close, factor_data=close_amt_rank, title = "Close amt and Price", y_axis="amt")
dual_plot(price_data=close, factor_data=close_turn_rank, title = "Close turn and Price", y_axis="turn")

## skew kurt
ret_skew = log_ret.rolling(20).skew()
ret_kur = log_ret.rolling(20).kurt()

window_skew = len(ret_skew[ret_skew.index <= "2018-01-01"]) + 1

ret_skew_rank = variable_rank(data = ret_skew, inital_window = window_skew)
ret_kur_rank = variable_rank(data = ret_kur, inital_window = window_skew)

dual_plot(price_data=close, factor_data=ret_skew_rank, title = "skew and Price", y_axis="skew")
dual_plot(price_data=close, factor_data=ret_kur_rank, title = "kur and Price", y_axis="kur")

##  bias

bais = (df_corr - df_corr.rolling(20).mean())/(df_corr.rolling(20).mean())
bais = bais.dropna()
close_bais = bais[["close"]]
tradevol_bais = bais[["volume"]]
amt_bais = bais[["amt"]]
turn_bais = bais[["turn"]]

window_bais = len(close_bais[close_bais.index <= "2018-01-01"])

close_bais_rank = variable_rank(data = close_bais, inital_window=window_bais)
amt_bais_rank = variable_rank(data = amt_bais, inital_window=window_bais)
turn_bais_rank = variable_rank(data = turn_bais, inital_window=window_bais)

dual_plot(price_data=close, factor_data=close_bais_rank, title = "close bais and Price", y_axis="close")
dual_plot(price_data=close, factor_data=amt_bais_rank, title = "amt bais and Price", y_axis="amt")
dual_plot(price_data=close, factor_data=turn_bais_rank, title = "turn and Price", y_axis="turn")

# combin
##
exp_rank["Signal_a"] = exp_rank["close"].apply(signal)
ret_skew_rank["Signal_b"] = ret_skew_rank['close'].apply(signal)
close_turn_rank['Signal_c'] = close_turn_rank["Corr"].apply(signal)
ret_kur_rank['Signal_d'] =ret_kur_rank['close'].apply(signal) 

crowding = exp_rank.merge(ret_skew_rank, on = "Date").merge(close_turn_rank, on = "Date").merge(ret_kur_rank, on = "Date")[["Date", "Signal_a", "Signal_b","Signal_c","Signal_d" ]]
crowding["Signal"] = crowding[["Signal_a", "Signal_b","Signal_c","Signal_d"]].sum(axis = 1)
crowding["Crowding"] = crowding["Signal"].apply(signal)

pbpe_crowding = low_singal_crowded(data = pbpe_rank, low_bond = 0.05, low_clear = 0.6, crowded_data = crowding, after_day = 10)
profit_long_pbpe = back_test_long(price_data = close, signal_data = pbpe_crowding)

plt.figure(num = 1, figsize = (12,6))
plt.grid()
plt.plot(close["Date"], close["HS300_close"], label = "Close")
plt.plot(profit_long_pbpe[profit_long_pbpe["Signal_long"] == 'Long'].Date, profit_long_pbpe[profit_long_pbpe["Signal_long"] == 'Long']["HS300_close"], "+", label = "Long")
plt.plot(profit_long_pbpe[profit_long_pbpe["Signal_long"] == 'Clear'].Date, profit_long_pbpe[profit_long_pbpe["Signal_long"] == 'Clear']["HS300_close"], "o", label = "Long_Clear")
leg = plt.legend(loc='upper left')
plt.title("PBPE crowding and Price")
plt.xlabel('Date')
plt.show()

roverrt_crowding = low_singal_crowded(data = roverrt_rank, low_bond = 0.05, low_clear = 0.6, crowded_data = crowding, after_day = 10)
profit_long_pbpe = back_test_long(price_data = close, signal_data = roverrt_crowding)

plt.figure(num = 1, figsize = (12,6))
plt.grid()
plt.plot(close["Date"], close["HS300_close"], label = "Close")
plt.plot(profit_long_pbpe[profit_long_pbpe["Signal_long"] == 'Long'].Date, profit_long_pbpe[profit_long_pbpe["Signal_long"] == 'Long']["HS300_close"], "+", label = "Long")
plt.plot(profit_long_pbpe[profit_long_pbpe["Signal_long"] == 'Clear'].Date, profit_long_pbpe[profit_long_pbpe["Signal_long"] == 'Clear']["HS300_close"], "o", label = "Long_Clear")
leg = plt.legend(loc='upper left')
plt.title("Roverrt crowding and Price")
plt.xlabel('Date')
plt.show()

roverrt_crowdin = low_singal_crowded_two(data_1 = pbpe_rank ,data_2 = roverrt_rank, low_bond = 0.05, low_clear = 0.6, crowded_data = crowding, after_day = 10)
profit_long_pbpe = back_test_long(price_data = close, signal_data = roverrt_crowding)
plt.figure(num = 1, figsize = (12,6))
plt.grid()
plt.plot(close["Date"], close["HS300_close"], label = "Close")
plt.plot(profit_long_pbpe[profit_long_pbpe["Signal_long"] == 'Long'].Date, profit_long_pbpe[profit_long_pbpe["Signal_long"] == 'Long']["HS300_close"], "+", label = "Long")
plt.plot(profit_long_pbpe[profit_long_pbpe["Signal_long"] == 'Clear'].Date, profit_long_pbpe[profit_long_pbpe["Signal_long"] == 'Clear']["HS300_close"], "o", label = "Long_Clear")
leg = plt.legend(loc='upper left')
plt.title("PBPE Roverrt crowding and Price")
plt.xlabel('Date')
plt.show()