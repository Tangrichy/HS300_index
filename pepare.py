# data prepare

## Evaluation

### Formate: Date, HS300_close, HS300_pe, HS300_pb HS300_risk

import requests
from jsonpath import jsonpath
import json
import pandas as pd

def updated_data(data, new_data, column = Null):

    if column == Null:
        new_data.columns = data.columns
        new_data.index.name = data.index.name
    else:
        new_data = new_data.loc[:, column]
        new_data.columns = data.columns
        new_data.index.name = data.index.name
    
    data = pd.contact([data, new_data])

    return data

# Evalustion through wind
# crowding throung ifund

def new_data(start_time, end_time, token, index_code= "000300.SH"):
    thsHeaders = {'Content-Type': 'application/json', 'access_token': token}
    index_url = "https://quantapi.51ifind.com/api/v1/cmd_history_quotation"
    para = {"codes":index_code,"indicators":"close,volume,amount,turnoverRatio","startdate":start_time,"enddate": end_time}
    index_df = requests.post(url=index_url,json=para,headers=thsHeaders)

    index_json = index_df.json()
    json_df = jsonpath(index_json, "$..tables")[0][0]

    Date = json_df['time']
    close = json_df['table']['close']
    volume = json_df['table']['volume']
    amt = json_df['table']['amount']
    turn = json_df['table']['turnoverRatio']

    output = {"Date": Date, "close": close, "volume": volume, "amt": amt, "turn": turn}
    output = pd.DataFrame(output)
    output['Date'] = pd.to_datetime(output['Date'])


    return output


def new_data(time, token, index_code= "000300.SH", date_range = 250, window = 1):
    thsHeaders = {'Content-Type': 'application/json', 'access_token': token}
    high_low_url = "https://quantapi.51ifind.com/api/v1/basic_data_service"
    para = {"codes":index_code,"indipara":[{"indicator":"ths_new_high_num_index","indiparams":[time,window,date_range,"101"]},{"indicator":"ths_new_low_num_index","indiparams":[time,window,date_range,"101"]}]}
    high_low = requests.post(url=high_low_url,json=para,headers=thsHeaders)

    index_json = index_df.json()
    json_df = jsonpath(index_json, "$..tables")[0][0]

    Date = json_df['time']
    close = json_df['table']['close']
    volume = json_df['table']['volume']
    amt = json_df['table']['amount']
    turn = json_df['table']['turnoverRatio']

    output = {"Date": Date, "close": close, "volume": volume, "amt": amt, "turn": turn}
    output = pd.DataFrame(output)
    output['Date'] = pd.to_datetime(output['Date'])