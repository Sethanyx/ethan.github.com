import requests

# +
import pandas as pd

# 处理数据，将其转换为适合 pandas 处理的格式
def convert_to_df(data, key):
    df = pd.DataFrame(data[key])
    df['ticker'] = key  # 添加股票代码作为一个新列
    return df



# -

purchase_data = pd.read_csv("purchase_data.csv")
ticker_list = list(set(purchase_data["Ticker"]))
for idx in range(len(ticker_list)):
    ticker_list[idx] = ticker_list[idx].lower()

name1_list = []
for stock in ticker_list:
    try:
        url = f'https://eodhd.com/api/sentiments?s={stock}&from=2023-10-01&to=2024-03-31&api_token=66185c246dda20.66795644&fmt=json'
        data = requests.get(url).json()
        # 处理数据，将其转换为适合 pandas 处理的格式并保存
        frames = [convert_to_df(data, key) for key in data]
        result_df = pd.concat(frames)
        sorted_df = result_df.sort_values(by='date')
        sorted_df.to_csv(f'stock_data_{stock}.csv', index=False)
        name1_list.append(stock)
    except Exception as e:
        print(e)

for idx in range(len(name1_list)):
    name1_list[idx] = name1_list[idx].lower()
name1_list

date = df["date"]
normalized = df["normalized"]
purchase_data = pd.read_csv("purchase_data.csv")
#purchase_data["ReportDate"][purchase_data["Ticker"].index()]
purchase_data_reportdate = list(purchase_data["ReportDate"])
purchase_data_ticker = list(purchase_data["Ticker"])
#for stock in 

import yfinance as yf

data_price = {}
for name in name1_list:
    try:
        name = name.upper()
        data_price[name] = yf.download(name, start="2023-10-01", end="2024-03-31")
    except Exception as e:
        print(e)

name_list = list(data_price.keys())
daily_price = {}
daily_date = {}
for name in name1_list:
    try:
        name1 = name.upper()
        stock_table = data_price[name1]
        daily_price[name] = list(stock_table["Close"]) #日度数据股票收盘价格
        daily_date[name] = [str(date)[:10] for date in list(stock_table.index.values)] #日度数据日期
    except Exception as e:
        print(e)

daily_price

daily_date

# data_price = yf.download("GTLS", start="2023-10-01", end="2024-03-31")
# price_date_list = {}
buy_price = []
sell_price = []
for name in name1_list:
    try:
        daily_trade = pd.DataFrame({"daily_price":daily_price[name], "date":daily_date[name]})
        data = pd.read_csv("stock_data_{}.csv".format(name.lower())) #敏感度每只股票的csv文件读入
        common_dates_df = daily_trade.merge(data, on='date')
        name1 = name.upper()
        price_date_list = list(common_dates_df["date"])
        indices = [i for i, x in enumerate(list(purchase_data["Ticker"])) if x == name1] #找到所有关于name购买记录的index
        
        date_stock = list(common_dates_df["date"]) #获取敏感度日期
        data_normalized = list(common_dates_df["normalized"]) #获取敏感度normalized数据
        
        for idx in indices: # 每一个idx代表一个购买记录
            date = purchase_data_reportdate[idx] #找到具体reportdate
            index = date_stock.index(date) #找到敏感度日期索引
            index_price = price_date_list.index(date) # 找到股票日度数据索引
            
            #while index < len(date_stock) - 1:
            flag = False
            while index < min((date_stock.index(date) + 2),(len(date_stock)-1)):
                if data_normalized[index] > 0.6:
                    index_price = price_date_list.index(date_stock[index])
                    buy_price.append(daily_price[name][index_price]) # 将那天的收盘价记录下来，作为买入价
                    flag = True
                    break
                index += 1
            # if index == len(date_stock) and flag == True: index = index - 1
            if flag == True:
                while index < len(date_stock)-1 and data_normalized[index] > 0.3:
                    index += 1
                index_price = price_date_list.index(date_stock[index])
                sell_price.append(daily_price[name][index_price])
            
    except Exception as e:
        print(e)

len(buy_price)

len(sell_price)

return_price = [(sell_price[i] - buy_price[i]) / buy_price[i] for i in range(len(buy_price))] 
return_price_mean = sum(return_price) / len(return_price)
return_price_mean

daily_trade = pd.DataFrame({"daily_price":daily_price["aapl"], "date":daily_date["aapl"]})
data = pd.read_csv("stock_data_aapl.csv".format(name.lower())) #敏感度每只股票的csv文件读入
common_dates_df = daily_trade.merge(data, on='date')
common_dates_df


