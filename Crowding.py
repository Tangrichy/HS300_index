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

## Hindenburg Omen

rolling_window_hindenburg = 10

new_high_low = df_corr[["High", "Low"]]

new_high_low["Hindenburgsqrt"] = (np.sqrt(new_high_low["High"]).values * np.sqrt(new_high_low['Low']).values)/300
new_high_low["HindenburgHigh"] = new_high_low["High"]/300
new_high_low["Hindenburgdelta"] = (new_high_low["High"] - new_high_low["Low"])/300

Hindenburgsqrt = new_high_low[["Hindenburgsqrt"]].rolling(rolling_window_hindenburg).mean().dropna().reset_index()
HindenburgHigh = new_high_low["HindenburgHigh"].rolling(rolling_window_hindenburg).mean().dropna().reset_index()
Hindenburgdelta = new_high_low["Hindenburgdelta"].rolling(rolling_window_hindenburg).mean().dropna().reset_index()

window_hind = len(Hindenburgsqrt[Hindenburgsqrt["Date"] <= "2018-01-01"]) + 1

Hindenburgsqrt_rank = variable_rank(data = Hindenburgsqrt, inital_window=window_hind, index = False)
HindenburgHigh_rank = variable_rank(data = HindenburgHigh, inital_window=window_hind, index = False)
Hindenburgdelta_rank = variable_rank(data = Hindenburgdelta, inital_window=window_hind, index = False)


dual_plot(price_data=close, factor_data=Hindenburgsqrt_rank, title="Hindenburgsqrt", y_axis= "High_Low")
dual_plot(price_data=close, factor_data=HindenburgHigh_rank, title="HindenburgHigh", y_axis= "High_Low")
dual_plot(price_data=close, factor_data=Hindenburgdelta_rank, title="Hindenburgdelta", y_axis= "High_Low")


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