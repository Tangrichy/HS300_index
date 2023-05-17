from Function import *

df_corr = pd.read_excel("./HS300_data_updated.xlsx", sheet_name="Sheet2")
df_corr = df_corr.set_index("Date")
price = df_corr[["close"]]
close = df_corr[['close']]
close = close[close.index >= "2018-01-01"].reset_index()

# crowded

std = np.std

rolling_window_ret = 20

## risk variance
log_ret= np.log(price["close"].pct_change() + 1)
log_ret = pd.DataFrame(log_ret)
ret_var = log_ret.rolling(rolling_window_ret).std(ddof=1).dropna() # window is 20 trading-days
window_ret = len(ret_var[ret_var.index < "2018-01-01"]) + 1
var_rank = variable_rank(data=ret_var, inital_window=window_ret)

### plot

dual_plot(price_data=close, factor_data=var_rank, title="Std and price", y_axis="std")


## momentum
### pct change

rolling_window_exp = 20

price = df_corr[["close"]]
exp_fun = np.log(price.pct_change()+1).rolling(rolling_window_exp).sum().dropna() ##### exp window 20

window_exp = len(exp_fun[exp_fun.index <= "2018-01-01"]) + 1


exp_rank = variable_rank(data = exp_fun, inital_window=window_exp)

dual_plot(price_data = close, factor_data = exp_rank, title="exp vol and price", y_axis="exp_vol")

## liq

rolling_window_liq = 10

vol = df_corr[["volume"]]
amt = df_corr[["amt"]]
turn = df_corr[["turn"]]

vol_mean = vol.rolling(rolling_window_liq).mean().dropna()
amt_mean = amt.rolling(rolling_window_liq).mean().dropna()
turn_mean = turn.rolling(rolling_window_liq).mean().dropna()

window_liq = len(vol_mean[vol_mean.index<= "2018-01-01"]) + 1

vol_rank = variable_rank(data = vol_mean, inital_window=window_liq)
amt_rank = variable_rank(data = amt_mean, inital_window=window_liq)
turn_rank = variable_rank(data = turn_mean, inital_window=window_liq)

dual_plot(price_data=close, factor_data=vol_rank, title="vol and price", y_axis= "Vol")
dual_plot(price_data=close, factor_data=amt_rank, title="amt and price", y_axis= "amt")
dual_plot(price_data=close, factor_data=turn_rank, title="turn and price", y_axis= "turn")


## correlation

rolling_window_corr = 20

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

close_volume_corr = corr_fun(data=close_volume, inital=rolling_window_corr) # window is 20
close_amt_corr = corr_fun(data=close_amt, inital=rolling_window_corr)
close_turn_corr = corr_fun(data=close_turn, inital=rolling_window_corr)

window_cor = len(close_volume_corr[close_volume_corr["Date"] <= "2018-01-01"]) + 1


close_volume_rank = variable_rank(data = close_volume_corr, inital_window=window_cor, sort=False,index = False)
close_amt_rank = variable_rank(data = close_amt_corr, inital_window=window_cor, sort=False,index = False)
close_turn_rank = variable_rank(data = close_turn_corr, inital_window=window_cor, sort=False,index = False)

dual_plot(price_data=close, factor_data=close_volume_rank, title = "Close volume and Price", y_axis="Volume")
dual_plot(price_data=close, factor_data=close_amt_rank, title = "Close amt and Price", y_axis="amt")
dual_plot(price_data=close, factor_data=close_turn_rank, title = "Close turn and Price", y_axis="turn")

## skew kurt

rolling_window_skew = 20

ret_skew = log_ret.rolling(rolling_window_skew).skew().dropna()
ret_kur = log_ret.rolling(rolling_window_skew).kurt().dropna()

window_skew = len(ret_skew[ret_skew.index <= "2018-01-01"]) + 1

ret_skew_rank = variable_rank(data = ret_skew, inital_window = window_skew)
ret_kur_rank = variable_rank(data = ret_kur, inital_window = window_skew)

dual_plot(price_data=close, factor_data=ret_skew_rank, title = "skew and Price", y_axis="skew")
dual_plot(price_data=close, factor_data=ret_kur_rank, title = "kur and Price", y_axis="kur")

##  bias

rolling_window_bais = 60

bais = (df_corr - df_corr.rolling(rolling_window_bais).mean())/(df_corr.rolling(rolling_window_bais).mean())
bais = bais.dropna()
close_bais = bais[["close"]]
tradevol_bais = bais[["volume"]]
amt_bais = bais[["amt"]]
turn_bais = bais[["turn"]]

window_bais = len(close_bais[close_bais.index <= "2018-01-01"]) + 1

close_bais_rank = variable_rank(data = close_bais, inital_window=window_bais)
amt_bais_rank = variable_rank(data = amt_bais, inital_window=window_bais)
turn_bais_rank = variable_rank(data = turn_bais, inital_window=window_bais)

dual_plot(price_data=close, factor_data=close_bais_rank, title = "close bais and Price", y_axis="close")
dual_plot(price_data=close, factor_data=amt_bais_rank, title = "amt bais and Price", y_axis="amt")
dual_plot(price_data=close, factor_data=turn_bais_rank, title = "turn and Price", y_axis="turn")

## combin
##
exp_rank["Signal_a"] = exp_rank["close"].apply(signal)
ret_skew_rank["Signal_b"] = ret_skew_rank['close'].apply(signal)
close_turn_rank['Signal_c'] = close_turn_rank["Corr"].apply(signal)
ret_kur_rank['Signal_d'] =ret_kur_rank['close'].apply(signal) 

crowding = exp_rank.merge(ret_skew_rank, on = "Date").merge(close_turn_rank, on = "Date").merge(ret_kur_rank, on = "Date")[["Date", "Signal_a", "Signal_b","Signal_c","Signal_d" ]]
crowding["Signal"] = crowding[["Signal_a", "Signal_b","Signal_c","Signal_d"]].sum(axis = 1)
crowding["Crowding"] = crowding["Signal"].apply(signal)

pbpe_crowding = low_singal_crowded(data = pbpe_rank, low_bond = 0.05, low_clear = 0.6, crowded_data = crowding, after_day = 20)
profit_long_pbpe_crowding = back_test_long(price_data = close, signal_data = pbpe_crowding)

profit_long_pbpe_crowding

plt.figure(num = 1, figsize = (12,6))
plt.grid()
plt.plot(close["Date"], close["HS300_close"], label = "Close")
plt.plot(profit_long_pbpe_crowding[profit_long_pbpe_crowding["Signal_long"] == 'Long'].Date, profit_long_pbpe_crowding[profit_long_pbpe_crowding["Signal_long"] == 'Long']["HS300_close"], "+", label = "Long")
plt.plot(profit_long_pbpe_crowding[profit_long_pbpe_crowding["Signal_long"] == 'Clear'].Date, profit_long_pbpe_crowding[profit_long_pbpe_crowding["Signal_long"] == 'Clear']["HS300_close"], "o", label = "Long_Clear")
leg = plt.legend(loc='upper left')
plt.title("PBPE crowding and Price")
plt.xlabel('Date')
plt.show()

fig, ax1 = plt.subplots(num = 1, figsize = (12,6))
plt.grid(1)
ax1.plot(close["Date"], close["HS300_close"], label = "Close")
ax1.plot(profit_long_pbpe_crowding[profit_long_pbpe_crowding["Signal_long"] == 'Long'].Date, profit_long_pbpe_crowding[profit_long_pbpe_crowding["Signal_long"] == 'Long']["HS300_close"], "+", label = "Long")
ax1.plot(profit_long_pbpe_crowding[profit_long_pbpe_crowding["Signal_long"] == 'Clear'].Date, profit_long_pbpe_crowding[profit_long_pbpe_crowding["Signal_long"] == 'Clear']["HS300_close"], "o", label = "Long_Clear")
ax1.set_ylabel("Close")
ax2 = ax1.twinx()
ax2.plot(profit_long_pbpe_crowding["Date"], profit_long_pbpe_crowding["Profit"], color = "orange",label = "Profit")
ax2.set_ylabel("Profit")
ax1.set_xlabel("Date")
plt.title("PBPE Profit with croding")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 +labels2, loc = "upper left")
plt.show()

roverrt_crowding = low_singal_crowded(data = roverrt_rank, low_bond = 0.05, low_clear = 0.6, crowded_data = crowding, after_day = 20)
profit_long_roverrt_crowding = back_test_long(price_data = close, signal_data = roverrt_crowding)

plt.figure(num = 1, figsize = (12,6))
plt.grid()
plt.plot(close["Date"], close["HS300_close"], label = "Close")
plt.plot(profit_long_roverrt_crowding[profit_long_roverrt_crowding["Signal_long"] == 'Long'].Date, profit_long_roverrt_crowding[profit_long_roverrt_crowding["Signal_long"] == 'Long']["HS300_close"], "+", label = "Long")
plt.plot(profit_long_roverrt_crowding[profit_long_roverrt_crowding["Signal_long"] == 'Clear'].Date, profit_long_roverrt_crowding[profit_long_roverrt_crowding["Signal_long"] == 'Clear']["HS300_close"], "o", label = "Long_Clear")
leg = plt.legend(loc='upper left')
plt.title("Roverrt crowding and Price")
plt.xlabel('Date')
plt.show()

fig, ax1 = plt.subplots(num = 1, figsize = (12,6))
plt.grid(1)
ax1.plot(close["Date"], close["HS300_close"], label = "Close")
ax1.plot(profit_long_roverrt_crowding[profit_long_roverrt_crowding["Signal_long"] == 'Long'].Date, profit_long_roverrt_crowding[profit_long_roverrt_crowding["Signal_long"] == 'Long']["HS300_close"], "+", label = "Long")
ax1.plot(profit_long_roverrt_crowding[profit_long_roverrt_crowding["Signal_long"] == 'Clear'].Date, profit_long_roverrt_crowding[profit_long_roverrt_crowding["Signal_long"] == 'Clear']["HS300_close"], "o", label = "Long_Clear")
ax1.set_ylabel("Close")
ax2 = ax1.twinx()
ax2.plot(profit_long_roverrt_crowding["Date"], profit_long_roverrt_crowding["Profit"], color = "orange",label = "Profit")
ax2.set_ylabel("Profit")
ax1.set_xlabel("Date")
plt.title("Roverrt Profit with croding")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 +labels2, loc = "upper left")
plt.show()


pbpe_roverrt_crowding = low_singal_crowded_two(data_1 = pbpe_rank ,data_2 = roverrt_rank, low_bond = 0.05, low_clear = 0.6, crowded_data = crowding, after_day = 20)
profit_crowding = back_test_long(price_data = close, signal_data = pbpe_roverrt_crowding)
plt.figure(num = 1, figsize = (12,6))
plt.grid()
plt.plot(close["Date"], close["HS300_close"], label = "Close")
plt.plot(profit_crowding[profit_crowding["Signal_long"] == 'Long'].Date, profit_crowding[profit_crowding["Signal_long"] == 'Long']["HS300_close"], "+", label = "Long")
plt.plot(profit_crowding[profit_crowding["Signal_long"] == 'Clear'].Date, profit_crowding[profit_crowding["Signal_long"] == 'Clear']["HS300_close"], "o", label = "Long_Clear")
leg = plt.legend(loc='upper left')
plt.title("PBPE Roverrt crowding and Price")
plt.xlabel('Date')
plt.show()

fig, ax1 = plt.subplots(num = 1, figsize = (12,6))
plt.grid(1)
ax1.plot(close["Date"], close["HS300_close"], label = "Close")
ax1.plot(profit_crowding[profit_crowding["Signal_long"] == 'Long'].Date, profit_crowding[profit_crowding["Signal_long"] == 'Long']["HS300_close"], "+", label = "Long")
ax1.plot(profit_crowding[profit_crowding["Signal_long"] == 'Clear'].Date, profit_crowding[profit_crowding["Signal_long"] == 'Clear']["HS300_close"], "o", label = "Long_Clear")
ax1.set_ylabel("Close")
ax2 = ax1.twinx()
ax2.plot(profit_crowding["Date"], profit_crowding["Profit"], color = "orange",label = "Profit")
ax2.set_ylabel("Profit")
ax1.set_xlabel("Date")
plt.title("Profit with croding")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 +labels2, loc = "upper left")
plt.show()

plt.figure(num = 1, figsize = (12,6))
plt.grid()
plt.plot(profit_long_pbpe_crowding["Date"], profit_long_pbpe_crowding["Profit"], label = "PBPE")
plt.plot(profit_long_roverrt_crowding["Date"], profit_long_roverrt_crowding["Profit"], label = "Roverrt")
plt.plot(profit_crowding["Date"], profit_crowding["Profit"], label = "Two")
leg = plt.legend(loc='upper left')
plt.title("PBPE Roverrt crowding and Price")
plt.xlabel('Date')
plt.show()