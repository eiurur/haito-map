import pprint
import pandas as pd
import os
import datetime
import yfinance as yf
import json
from yahooquery import Ticker


read_file = pd.read_excel(r"tosho.xls")
read_file.to_csv(r"tosho.csv", index = None, header=False)
codes = pd.read_csv(r"tosho.csv", usecols=[1,2])
stock_tickers = [f"{row[1]}.T" for row in codes.itertuples()]
stock_names = [f"{row[2]}" for row in codes.itertuples()]

today = datetime.date.today()
today_yyyymmdd = today.strftime('%Y%m%d')
db_dpath = f"./db/{today_yyyymmdd}"
os.makedirs(db_dpath, exist_ok=True)

# dump tickers
tickers_fpath = os.path.join(db_dpath, f"tickers.json")

sd = None
if os.path.exists(tickers_fpath):
    with open(tickers_fpath, 'r', encoding='utf-8') as f:
        sd = json.load(f)
else:
    tickers = Ticker(stock_tickers, progress=True)
    sd = tickers.summary_detail
    with open(tickers_fpath, 'w', encoding="utf-8") as f:
        json.dump(sd, f, indent = 4, ensure_ascii=False)

# dump stocks
data = [] 
for idx, (ticker, detail) in enumerate(sd.items()):
    if "dividendYield" not in detail:
        continue
    
    name = stock_names[idx]
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

stocks_fpath = os.path.join(db_dpath, f"stocks.json")
with open(stocks_fpath, 'w', encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

