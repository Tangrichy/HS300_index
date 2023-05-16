from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_excel("./HS300_data_updated.xlsx")
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index('Date')

## Select data
pe = df[['HS300_pe']]
pb = df[['HS300_pb']]
close = df[['HS300_close']]
close = close[close.index >= "2018-01-01"]
roverrt = df[["HS300_risk"]]

# obtain the length of window
windwo_len = len(roverrt[roverrt.index <= '2017-12-31']) + 1

## Rank

# obtain rank
variable_rank(data = pe, inital_window = windwo_len)


pe_rank= pe.rolling(windwo_len).rank(pct= True).dropna()
pb_rank = pb.rolling(windwo_len).rank(pct= True).dropna()
roverrt_rank = roverrt.rolling(windwo_len).rank(pct = True, ascending=False).dropna()

pbpe = (pe_rank["HS300_pe"] + pb_rank["HS300_pb"])/2
pbpe_rank = pd.DataFrame(pbpe, index=pbpe.index, columns= ["HS300_pbpe"])

pe_rank = pe_rank.reset_index()
pb_rank =pb_rank.reset_index()
roverrt_rank = roverrt_rank.reset_index()
pbpe_rank = pbpe_rank.reset_index()
close = close.reset_index()

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

pbpe_low_signal = low_singal(data = pbpe_rank, low_bond=0.05, low_clear=0.4)
pbpe_upper_signal = upper_singal(data = pbpe_rank, upper_bond=0.95, upper_clear=0.7)

profit_long_pbpe = back_test_long(price_data = close, signal_data = pbpe_low_signal)
profit_short_pbpe = back_test_short(price_data = close, signal_data = pbpe_upper_signal)

plt.figure(num = 1, figsize = (12,6))
plt.grid()
plt.plot(close["Date"], close["HS300_close"], label = "Close")
plt.plot(profit_long_pbpe[profit_long_pbpe["Signal_long"] == 'Long'].Date, profit_long_pbpe[profit_long_pbpe["Signal_long"] == 'Long']["HS300_close"], "+", label = "Long")
plt.plot(profit_long_pbpe[profit_long_pbpe["Signal_long"] == 'Clear'].Date, profit_long_pbpe[profit_long_pbpe["Signal_long"] == 'Clear']["HS300_close"], "o", label = "Long_Clear")
plt.plot(profit_short_pbpe[profit_short_pbpe["Signal_short"] == 'Short'].Date, profit_short_pbpe[profit_short_pbpe["Signal_short"] == 'Short']["HS300_close"], "v", label = "Short")
plt.plot(profit_short_pbpe[profit_short_pbpe["Signal_short"] == 'Clear'].Date, profit_short_pbpe[profit_short_pbpe["Signal_short"] == 'Clear']["HS300_close"], "^", label = "Short_Clear")
leg = plt.legend(loc='upper left')
plt.title("PBPE and Price")
plt.xlabel('Date')
plt.show()



roverrt_low_signal = low_singal(data = roverrt_rank, low_bond=0.05, low_clear=0.4)
roverrt_signal = upper_singal(data = roverrt_rank, upper_bond=0.95, upper_clear=0.7)

