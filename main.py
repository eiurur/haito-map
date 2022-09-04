import pprint
import pandas as pd
import os
import datetime
import yfinance as yf
import json
from yahooquery import Ticker

import pickle

read_file = pd.read_excel(r"data_j.xls")
read_file.to_csv(r"data_j.csv", index = None, header=False)
codes = pd.read_csv(r"data_j.csv", usecols=[1,2])
stock_tickers = [f"{row[1]}.T" for row in codes.itertuples()]
stock_names = [f"{row[2]}.T" for row in codes.itertuples()]


today = datetime.date.today()
start = datetime.datetime.now() - datetime.timedelta(days=7)
end = today

# tickers = yf.Tickers(" ".join(stock_tickers))

today_yyyymmdd = today.strftime('%Y%m%d')
tickers_fname = f"tickers_{today_yyyymmdd}.json"

sd = None
print(os.path.exists(tickers_fname))
if os.path.exists(tickers_fname):
    with open(tickers_fname, 'r', encoding='utf-8') as f:
        sd = json.load(f)
else:
    tickers = Ticker(stock_tickers, progress=True)
    sd = tickers.summary_detail
    print(sd)
    with open(tickers_fname, 'w', encoding="utf-8") as f:
        json.dump(sd, f, indent = 4, ensure_ascii=False)

# print("start")
data = [] # 終値
for idx, (ticker, detail) in enumerate(sd.items()):
    name = stock_names[idx]
    if "dividendYield" not in detail:
        continue
    dividendRate = detail["dividendRate"]
    dividendYield = detail["dividendYield"]
    previousClose = detail["previousClose"]
    data.append({
      "ticker": ticker,
      "name": name,
      "dividendRate": dividendRate,
      "dividendYield": dividendYield,
      "previousClose": previousClose,
    })
    print(ticker, name, dividendYield, previousClose)


# closes = pd.DataFrame(closes).T   # DataFrame化
# closes.columns = stocks           # カラム名の設定
# closes = closes.ffill()           # 欠損データの補完
# print(closes)

fname = f"stock_{today_yyyymmdd}.json"
with open(fname, 'w', encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

# 会社概要(info)を出力
# pprint.pprint(ticker_info.info)
