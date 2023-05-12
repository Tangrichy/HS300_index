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